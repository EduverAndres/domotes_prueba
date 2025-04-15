from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import QueryTemplate
from utils.report_generator import generate_report
from utils.email_sender import send_email
from utils.scheduler_tasks import schedule_queries, scheduler
from routers.templates import router as templates_router
from logging_config import logger  # Importa el logger desde logging_config.py




# Crear instancia de FastAPI
app = FastAPI()


# Registrar logs en los eventos de inicio y cierre
@app.on_event("startup")
def startup_event():
    logger.info("La aplicación ha iniciado correctamente.")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("La aplicación se ha detenido.")

class ReportRequest(BaseModel):
    query: str
    report_name: str
    recipients: list[str]

# Registrar el router de templates
app.include_router(templates_router, prefix="/templates", tags=["Templates"])

# Método POST: Generar y enviar reporte
@app.post("/generate-and-send-report/")
def generate_and_send_report(request: ReportRequest):
    try:
        # Generar el reporte CSV
        report_path = generate_report(request.query, request.report_name)
        if not report_path:
            raise HTTPException(status_code=500, detail="Error al generar el reporte.")
        
        # Enviar el reporte por correo electrónico
        send_email(
            subject="Reporte generado",
            body="Adjunto encontrarás el reporte solicitado.",
            recipients=request.recipients,
            file_path=report_path
        )

        return {"message": "Reporte generado y enviado exitosamente."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error durante el proceso: {e}")

# Eventos de inicio y cierre para el scheduler
@app.on_event("startup")
def start_scheduler():
    schedule_queries()  # Programar consultas desde el JSON
    scheduler.start()  # Iniciar el scheduler

@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()  # Detener el scheduler al cerrar la app
