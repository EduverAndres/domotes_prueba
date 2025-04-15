0.0 PROGRAMAR EJECUCION SCRIPT SQL
{
    "name": "ReporteUsuarios",  --> Nombre del reporte
    "query": "SELECT * FROM usuarios",
    "hour": 23,
    "minute": 59,
    "recipients": ["proyectodomotes@gmail.com", "eduverjimenez07@gmail.com", "puede agregar aqui el usuario que desee"]
}

usuario gmail = proyectodomotes@gmail.com
password = Domotes.123

Ejecute esto en la raiz para ejecutar el proyecto

1. Esquema de base de datos
Tablas principales
query_templates (Plantillas de consulta) Almacena las plantillas de las consultas SQL que los usuarios desean programar.

query_results (Resultados de consulta) Guarda los resultados generados después de ejecutar una consulta programada.

usuarios (Usuarios) Almacena la información de los usuarios registrados.

2. Especificación de endpoints
1. POST /templates
Descripción: Crear una nueva plantilla de consulta.

Parámetros (JSON):
{
    "name": "ReporteUsuariosActivos",
    "query": "SELECT * FROM usuarios WHERE fecha_registro > NOW() - INTERVAL 30 DAY"
}
Respuesta exitosa (201):
{
    "id": 1,
    "name": "ReporteUsuariosActivos",
    "query": "SELECT * FROM usuarios WHERE fecha_registro > NOW() - INTERVAL 30 DAY",
    "created_at": "2023-04-06T23:00:00"
}
--------------------------------------------------------------------------------------
2. GET /templates
Descripción: Obtener todas las plantillas creadas.

Parámetros: Ninguno.

Respuesta exitosa (200):
[
    {
        "id": 1,
        "name": "ReporteUsuariosActivos",
        "query": "SELECT * FROM usuarios WHERE fecha_registro > NOW() - INTERVAL 30 DAY",
        "created_at": "2023-04-06T23:00:00"
    },
    {
        "id": 2,
        "name": "ReporteUsuariosInactivos",
        "query": "SELECT * FROM usuarios WHERE fecha_registro <= NOW() - INTERVAL 30 DAY",
        "created_at": "2023-04-06T23:30:00"
    }
]
--------------------------------------------------------------------------------------
3. GET /templates/{template_id}
Descripción: Obtener una plantilla específica por su ID.

Parámetros:

URL: template_id (entero).

Respuesta exitosa (200):
{
    "id": 1,
    "name": "ReporteUsuariosActivos",
    "query": "SELECT * FROM usuarios WHERE fecha_registro > NOW() - INTERVAL 30 DAY",
    "created_at": "2023-04-06T23:00:00"
}
--------------------------------------------------------------------------------------
4. PUT /templates/{template_id}
Descripción: Actualizar una plantilla existente.

Parámetros:

URL: template_id (entero).

JSON:
{
    "name": "ReporteUsuariosInactivos",
    "query": "SELECT * FROM usuarios WHERE fecha_registro <= NOW() - INTERVAL 30 DAY"
}
Respuesta exitosa (200):
{
    "id": 1,
    "name": "ReporteUsuariosInactivos",
    "query": "SELECT * FROM usuarios WHERE fecha_registro <= NOW() - INTERVAL 30 DAY",
    "created_at": "2023-04-06T23:00:00"
}
--------------------------------------------------------------------------------------
5. DELETE /templates/{template_id}
Descripción: Eliminar una plantilla por su ID.

Parámetros:

URL: template_id (entero).

Respuesta exitosa (200):
{
    "message": "Plantilla con ID 1 eliminada exitosamente."
}
--------------------------------------------------------------------------------------
6. POST /schedule-query/
Descripción: Programar una consulta para ser ejecutada en el futuro.

Parámetros (JSON):
{
    "name": "ReporteUsuarios",
    "query": "SELECT * FROM usuarios",
    "hour": 23,
    "minute": 28,
    "recipients": ["proyectodomotes@gmail.com", "usuario@example.com"]
}
Respuesta exitosa (201):
{
    "message": "Consulta 'ReporteUsuarios' programada exitosamente.",
    "job_id": "job_ReporteUsuarios_23_28"
}
--------------------------------------------------------------------------------------
7. POST /create-user/
Descripción: Crear un nuevo usuario en la base de datos.

Parámetros (JSON):
{
    "nombre": "Juan Pérez",
    "correo": "juan.perez@example.com",
    "telefono": "123456789",
    "fecha_registro": "2023-04-06T23:00:00"
}
Respuesta exitosa (201):
{
    "id": 1,
    "nombre": "Juan Pérez",
    "correo": "juan.perez@example.com",
    "telefono": "123456789",
    "fecha_registro": "2023-04-06T23:00:00"
}
--------------------------------------------------------------------------------------


3. Diagrama de entidad-relación
Descripción
El diagrama relaciona las plantillas de consulta (query_templates), los resultados generados (query_results), y los usuarios (usuarios), mostrando las claves primarias, claves foráneas y sus asociaciones.

Relaciones clave
query_templates está relacionada con query_results en una relación de uno a muchos (una plantilla puede generar múltiples resultados).

La tabla usuarios no tiene relación directa con las otras tablas; se utiliza para datos de usuario.

diagrama:
usuarios
---------
| id       | PK
| nombre   |
| correo   |
| telefono |
| fecha_registro |

query_templates
---------
| id        | PK
| name      |
| query     |
| created_at|

query_results
---------
| id         | PK
| template_id| FK -> query_templates.id
| result     |
| executed_at|

Relaciones:
- query_templates.id -> query_results.template_id (1:N)


