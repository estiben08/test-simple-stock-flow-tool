import mysql.connector
import os

def connect():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'stock_user'),
        password=os.getenv('DB_PASS', 'stock_password'),
        database=os.getenv('DB_NAME', 'simple_stock_flow')
    )

def close_month(year, month):
    print(f"Cerrando mes {year}-{month} (Solo lectura)")
    # Logic to generate historical report would go here directly querying DB.
    
if __name__ == '__main__':
    print("Stock Flow CLI Tool")
