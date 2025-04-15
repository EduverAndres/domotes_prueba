from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from utils.report_generator import generate_report
from utils.email_sender import send_email
from logging_config import logger

scheduler = BackgroundScheduler()

def execute_query(name: str, query: str, recipients: list[str]):
    try:
        logger.info(f"Ejecutando consulta programada: {name}")
        report_name = f"{name}.csv"
        report_path = generate_report(query, report_name)

        if report_path:
            logger.info(f"Reporte generado correctamente: {report_path}")
            send_email(
                subject=f"Reporte programado: {name}",
                body="Adjunto encontrarás el reporte solicitado.",
                recipients=recipients,
                file_path=report_path
            )
            logger.info(f"Correo enviado con reporte adjunto: {report_path}")
        else:
            logger.warning(f"Error al generar el reporte para la consulta: {name}")
    except Exception as e:
        logger.error(f"Error crítico en 'execute_query': {e}")

# Función para programar consultas desde la configuración inicial
def schedule_queries():
    try:
        import json
        with open("queries_config.json", "r") as file:
            queries = json.load(file)
        for query in queries:
            trigger = CronTrigger(hour=query["schedule"]["hour"], minute=query["schedule"]["minute"])
            scheduler.add_job(
                execute_query,
                trigger,
                args=[query["name"], query["query"], query.get("recipients", ["proyectodomotes@gmail.com"])]
            )
        print("✅ Consultas programadas correctamente.")
    except Exception as e:
        print(f"❌ Error al programar consultas desde el archivo JSON: {e}")

# Función para agregar un trabajo dinámico al scheduler
def add_query_job(name: str, query: str, hour: int, minute: int, recipients: list[str]):
    try:
        trigger = CronTrigger(hour=hour, minute=minute)
        job = scheduler.add_job(
            execute_query, 
            trigger, 
            args=[name, query, recipients],
            id=f"job_{name}_{hour}_{minute}"
        )
        return job.id
    except Exception as e:
        print(f"❌ Error al agregar el trabajo al scheduler: {e}")
        return None

# Función para ejecutar la consulta programada
def execute_query(name: str, query: str, recipients: list[str]):
    try:
        report_name = f"{name}.csv"
        report_path = generate_report(query, report_name)
        if report_path:
            send_email(
                subject=f"Reporte programado: {name}",
                body="Adjunto encontrarás el reporte solicitado.",
                recipients=recipients,
                file_path=report_path
            )
            print(f"✅ Reporte enviado: {report_path}")
        else:
            print(f"❌ Error al generar el reporte: {name}")
    except Exception as e:
        print(f"❌ Error al ejecutar la consulta '{name}': {e}")
    