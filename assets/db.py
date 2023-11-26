import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}

class DatabaseTransaction:
    def __init__(self):
        self.connection = pymysql.connect(**db_config)
        self.cursor = self.connection.cursor()

    def start_transaction(self):
        try:
            self.cursor.execute("START TRANSACTION")
            print("Transaction started.")
        except pymysql.Error as e:
            print(f"Error starting transaction: {str(e)}")

    def execute_query(self, query, flag):
        try:
            print(query)
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            if(flag):
                self.cursor.execute("SELECT LAST_INSERT_ID()")
                result = self.cursor.fetchone()[0]
            return result
        except pymysql.Error as e:
            print(f"Error executing query: {str(e)}")
            return None  

    def commit_transaction(self):
        try:
            self.connection.commit()
            print("Transaction committed successfully.")
        except pymysql.Error as e:
            self.connection.rollback()
            print(f"Transaction rolled back due to error: {str(e)}")
        finally:
            self.cursor.close()
            self.connection.close()
