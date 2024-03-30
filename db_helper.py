
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



