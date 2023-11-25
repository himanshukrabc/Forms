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

def execute_query(query,flag=False):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    print(query)
    cursor.execute(query)
    result = cursor.fetchall()
    if(flag):
        cursor.execute("SELECT LAST_INSERT_ID()")
        result = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return result