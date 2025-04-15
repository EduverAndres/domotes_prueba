CREATE TABLE automation_db;


CREATE TABLE query_templates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    query TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE query_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    template_id INT,
    result TEXT NOT NULL,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (template_id) REFERENCES query_templates(id)
);

INSERT INTO usuarios (nombre, correo, telefono, fecha_registro)
VALUES 
('Juan Pérez', 'juan.perez@example.com', '123456789', '2023-04-06 23:00:00'),
('Eduver Jiménez', 'eduverjimenez07@gmail.com', '987654321', '2023-04-06 23:15:00'),
('Danna Martínez', 'danna.martinez@example.com', '321654987', '2023-04-06 23:30:00');

