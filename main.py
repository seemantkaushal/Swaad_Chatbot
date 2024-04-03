from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper
import generic_helper
app = FastAPI()
inprogress_orders=dict()

@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    # based on the structures of the WebhookRequest from Dialogflow
    intent = payload['queryResult']['intent']['displayName']

    parameters = payload['queryResult']['parameters']
    output_Context= payload['queryResult']["outputContexts"]
    # if intent == "track.order context: ongoing-tracking":
    #     return track_order(parameters)
    # elif intent == "add.order":
    #     add_order_db(parameters)

    session_id=generic_helper.extract_session_id(output_Context[0]["name"])


    intent_handler_dict={
        "track.order context: ongoing-tracking":track_order,
        "Add.order":add_order,
        "complete-order context:ongoing-order": complete_order
    }
    return intent_handler_dict[intent](parameters,session_id)


def track_order(parameters: dict):
    order_id = int(parameters['number'])
    order_status = db_helper.get_order_status(order_id)
    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def add_order(parameters:dict ,session_id:str):
    item_name=parameters["food-name"]
    quantity=parameters['number']
    if len(quantity)!=len(item_name):
        fulfillment_text="sorry i did not understant the Quantity specified , please specify correctly and try Again .."
    else:
        new_food_dict=dict(zip(item_name,quantity))
        if session_id in inprogress_orders:
            current_food_item=inprogress_orders[session_id]
            current_food_item.update(new_food_dict)
            inprogress_orders[session_id]=current_food_item
        else:
            inprogress_orders[session_id]=new_food_dict
        print("****************")
        print("session id:",session_id)

        order_str = generic_helper.str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text=f"so far we have recieved: {order_str} Do you need any thing else "

    return JSONResponse(content={
        'fulfillment_text':fulfillment_text
    })



def complete_order(parameters:dict,session_id :str):
    if session_id not in inprogress_orders:
        fulfillment_text="Something went wrong , please try again !!!"
    else:
        order= inprogress_orders[session_id]
        order_id=save_to_db(order)
        order_total=db_helper.get_total_order_price(order_id)
        if order_id==-1:
            fulfillment_text="sorry We could not place your order due to some error Please try again.."
        else:
            fulfillment_text = (f"Awsome , we have placed your order "
                                f"Your order id :#{order_id}"
                                f"your Total Amount:Rs{order_total}")

    del inprogress_orders[session_id]
    return JSONResponse(content={
        'fulfillment_text':"Thank you for placing order ,your order id is :###"
    })
def save_to_db(order: dict):
    next_order_id=db_helper.get_next_order_id()
    for food_item , quantity in order.items():
        rcode=db_helper.insert_order_item(food_item,
                                    quantity,
                                    next_order_id)
        if rcode==-1:
            return -1

    db_helper.insert_order_tracking(next_order_id,"in-progress")
    return next_order_id

# def add_order_db(parameters: dict):
#     # food_item
#     food_item = parameters["food-name"]

#     # Quantity
#     quantity = parameters['number']
#     item_id = fooditem_id(food_item)
#     # insert into db
#     for A, B, C in food_item, quantity, item_id:
#         db_helper.add_order(A, B, C)
#
#
# def fooditem_id(food_item: list):
#     item_id = []
#     for A in food_item:
#         if A == "Pav Bhaji":
#             item_id.append(1)
#         elif A == "Chole Bhature":
#             item_id.append(2)
#         elif A == "Pizza":
#             item_id.append(3)
#         elif A == "Mango Lassi":
#             item_id.append(4)
#         elif A == "Masala Dosa":
#             item_id.append(5)
#         elif A == "Vegetable Biryani":
#             item_id.append(6)
#         elif A == "Vada Pav":
#             item_id.append(7)
#         elif A == "Rava Dosa":
#             item_id.append(8)
#         elif A == "Samosa":
#             item_id.append(9)
#     return item_id
