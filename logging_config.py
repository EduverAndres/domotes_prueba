import logging

# Configuración básica del logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Formato del mensaje
    handlers=[
        logging.FileHandler("app.log"),  # Guardar logs en un archivo llamado app.log
        logging.StreamHandler()         # Mostrar logs en la consola
    ]
)

# Crear un logger específico para tu aplicación
logger = logging.getLogger("domotes-app")  # Nombre de tu logger, único para el proyecto
