import pymysql

# Define the MySQL connection function
def get_mysql_connection():
    ssl_config = {
        'ca': 'DigiCertGlobalRootCA.crt.pem',  # Path to your CA certificate file
    }

    connection = pymysql.connect(
        host='swaad-mysql-server.mysql.database.azure.com',  # Azure MySQL server hostname
        user='admin_seemant',  # Username with server name
        password='Seemant@4aug',  # MySQL password
        database='kaushal_swaad',  # Database name
        port=3306,
        ssl=ssl_config
    )
    return connection

def get_order_status(order_id,connection):
    cursor = connection.cursor()

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


# def add_order(A,B,C):
#     cursor = cnx.cursor()
#     query = "insert into orders(order_id,item_id,quantity,total_price) VALUES({},{},{},{})".format(A, B, C)
#     cursor.execute(query)


def get_next_order_id(connection):
    cursor = connection.cursor()
    query = "select MAX(order_id) from orders"
    cursor.execute(query)

    result = cursor.fetchone()[0]
    if (result is None):
        return 1
    else:
        return result + 1


def insert_order_item(food_item, quantity, next_order_id,connection):
    try:
        cursor = connection.cursor()
        cursor.callproc('insert_order_item', (food_item, quantity, next_order_id))
        connection.commit()
        cursor.close()
        print("order item inserted sucessfully")
        return 1

    except pymysql.MySQLError as err:
        print("Something went wrong: {err}")
        connection.rollback()
        return -1
    except Exception as e:
        print(f"Error occured : {e}")
        connection.rollback()
        return -1


def get_total_order_price(order_id,connection):
    cursor = connection.cursor()
    query = f"select get_total_order_price({order_id})"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return result


def insert_order_tracking(order_id, text,connection):
    cursor = connection.cursor()
    query = f"insert into order_tracking(order_id,status) values(%s,%s)"

    cursor.execute(query, (int(order_id), text))
    connection.commit()
    # result = cursor.fetchone()[0]
    cursor.close()
