
import mysql.connector
# global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Seemant4aug",
    database="pandeyji_eatery"
)
def get_order_status(order_id):
    cursor = cnx.cursor()

    # Executing the SQL query to fetch the order status
    query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()

    # Closing the cursor
    cursor.close()

    # Returning the order status
    if result:
        return result[0]
    else:
        return None

def add_order(A,B,C):
    cursor = cnx.cursor()
    querry = "insert into orders(order_id,item_id,quantity,total_price) VALUES({},{},{},{})".format(A, B, C)
    cursor.execute(querry)



def get_next_order_id():
    cursor = cnx.cursor()
    querry = "select MAX(order_id) from orders"
    cursor.execute(querry)

    result = cursor.fetchone()
    if (result is None):
        return 1
    else:
        return result + 1
def insert_order_item(food_item,quantity,next_order_id):
    try :
        cursor = cnx.cursor()
        cursor.callproc('insert_order_item', (food_item, quantity, next_order_id))
        cnx.commit()
        cursor.close()
        print("order item inserted sucessfully")
        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item :{err}")
        cnx.rollback()
        return -1
    except Exception as e :
        print(f"Error occured : {e}")
        cnx.rollback()
        return -1

def get_total_order_price(order_id):
    cursor=cnx.cursor()
    querry=f"select get_total_order_price({order_id})"
    cursor.execute(querry)
    result=cursor.fetchone()[0]
    cursor.close()
    return result

def insert_order_tracking(order_id,text):
    cursor = cnx.cursor()
    querry = f"insert into order_tracking(order_id,status) values(%s,%s)"

    cursor.execute(querry,(order_id,text))
    # result = cursor.fetchone()[0]
    cursor.close()
    # return result