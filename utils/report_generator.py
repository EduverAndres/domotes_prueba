from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

def generate_report(query: str, report_name: str):
    try:
        # Crear el motor de conexión con SQLAlchemy
        database_url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)

        # Crear una sesión para ejecutar la consulta
        with Session() as session:
            result = session.execute(text(query))  # Ejecutar la consulta usando SQLAlchemy
            
            # Transformar el resultado en un DataFrame de pandas
            rows = result.fetchall()
            columns = result.keys()
            df = pd.DataFrame(rows, columns=columns)

        # Generar el archivo CSV
        report_path = f"./reports/{report_name}"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)  # Crear la carpeta si no existe
        df.to_csv(report_path, index=False)
        print(f"✅ Reporte generado en: {report_path}")

        return report_path  # Devolver la ruta del archivo generado
    except Exception as e:
        print(f"❌ Error al generar el reporte: {e}")
        return None
