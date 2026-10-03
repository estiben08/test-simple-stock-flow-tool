import mysql.connector
import os
import argparse

def connect():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'stock_user'),
        password=os.getenv('DB_PASS', 'stock_password'),
        database=os.getenv('DB_NAME', 'simple_stock_flow')
    )

def close_month(year, month):
    print(f"Generando reporte inmutable para el periodo {year}-{month}...")
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    
    query = '''
    SELECT 
        si.product_id,
        si.product_name,
        SUM(si.quantity) as total_quantity,
        SUM(si.quantity * si.unit_price) as total_revenue
    FROM sale s
    JOIN sale_item si ON s.id = si.sale_id
    WHERE YEAR(s.created_at) = %s AND MONTH(s.created_at) = %s
    GROUP BY si.product_id, si.product_name
    '''
    cursor.execute(query, (year, month))
    rows = cursor.fetchall()
    
    print("-" * 50)
    print(f"REPORTE DE VENTAS CERRADO ({year}-{month})")
    print("-" * 50)
    for r in rows:
        print(f"Producto: {r['product_name']} | Unidades: {r['total_quantity']} | Ingresos: {r['total_revenue']}")
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple Stock Flow CLI Tool')
    parser.add_argument('--year', type=int, help='Año del reporte', required=True)
    parser.add_argument('--month', type=int, help='Mes del reporte', required=True)
    args = parser.parse_args()
    
    close_month(args.year, args.month)
