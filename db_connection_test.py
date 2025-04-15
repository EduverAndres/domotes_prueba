import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def test_db_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        print("✅ Conexión exitosa a la base de datos")
        return True
    except pymysql.MySQLError as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

# Ejecutar la prueba
if __name__ == "__main__":
    test_db_connection()
