from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import QueryTemplate
from schemas import ScheduleQuery, TemplateCreate, TemplateRead
from database import get_db
from utils.scheduler_tasks import add_query_job


router = APIRouter()

# Ruta POST: Crear una nueva plantilla de consulta
@router.post("/templates", response_model=TemplateRead)
def create_template(template: TemplateCreate, db: Session = Depends(get_db)):
    try:
        new_template = QueryTemplate(name=template.name, query=template.query)
        db.add(new_template)
        db.commit()
        db.refresh(new_template)
        return new_template
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la plantilla: {e}")

# Ruta GET: Obtener todas las plantillas
@router.get("/templates", response_model=list[TemplateRead])
def get_templates(db: Session = Depends(get_db)):
    try:
        templates = db.query(QueryTemplate).all()
        if not templates:
            raise HTTPException(status_code=404, detail="No se encontraron plantillas en la base de datos.")
        return templates
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las plantillas: {e}")

# Ruta GET: Obtener una plantilla específica por ID
@router.get("/templates/{template_id}", response_model=TemplateRead)
def get_template(template_id: int, db: Session = Depends(get_db)):
    try:
        template = db.query(QueryTemplate).filter(QueryTemplate.id == template_id).first()
        if not template:
            raise HTTPException(status_code=404, detail=f"No se encontró la plantilla con ID {template_id}.")
        return template
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la plantilla: {e}")

# Ruta DELETE: Eliminar una plantilla por ID
@router.delete("/templates/{template_id}")
def delete_template(template_id: int, db: Session = Depends(get_db)):
    try:
        template = db.query(QueryTemplate).filter(QueryTemplate.id == template_id).first()
        if not template:
            raise HTTPException(status_code=404, detail=f"No se encontró la plantilla con ID {template_id}.")
        db.delete(template)
        db.commit()
        return {"message": f"Plantilla con ID {template_id} eliminada exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la plantilla: {e}")

# Ruta PUT: Actualizar una plantilla por ID
@router.put("/templates/{template_id}", response_model=TemplateRead)
def update_template(template_id: int, template: TemplateCreate, db: Session = Depends(get_db)):
    try:
        existing_template = db.query(QueryTemplate).filter(QueryTemplate.id == template_id).first()
        if not existing_template:
            raise HTTPException(status_code=404, detail=f"No se encontró la plantilla con ID {template_id}.")
        existing_template.name = template.name
        existing_template.query = template.query
        db.commit()
        db.refresh(existing_template)
        return existing_template
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la plantilla: {e}")

# Nuevo endpoint: Programar consulta
@router.post("/schedule-query/")
def schedule_query(request: ScheduleQuery):  # Usar el esquema para validar el cuerpo de la solicitud
    try:
        job_id = add_query_job(
            name=request.name,
            query=request.query,
            hour=request.hour,
            minute=request.minute,
            recipients=request.recipients
        )
        return {"message": f"Consulta '{request.name}' programada exitosamente.", "job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al programar la consulta: {e}")
