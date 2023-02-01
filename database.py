import mysql.connector

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="sanket",
            passwd="sanket",
            database="lineup",
            auth_plugin='mysql_native_password'
        )
    except Exception as e:
        print(e)
        return None

    return connection
