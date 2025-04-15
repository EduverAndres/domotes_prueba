import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os

# Cargar variables del entorno
load_dotenv()

def send_email(subject: str, body: str, recipients: list[str], file_path: str, is_html: bool = False):
    try:
        # Cargar remitente y credenciales del archivo de entorno
        sender_email = os.getenv('EMAIL_USER')
        sender_password = os.getenv('EMAIL_PASSWORD')

        # Validar destinatarios
        if not recipients or not all(isinstance(r, str) and "@" in r and "." in r for r in recipients):
            raise ValueError(f"Las direcciones de correo electrónico no son válidas: {recipients}")

        # Crear el mensaje de correo electrónico
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = ", ".join(recipients)  # Combinar la lista de correos en una cadena
        message['Subject'] = subject

        # Agregar el cuerpo del mensaje
        if is_html:
            message.attach(MIMEText(body, 'html'))
        else:
            message.attach(MIMEText(body, 'plain'))

        # Adjuntar el archivo al mensaje
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(file_path)}'
            )
            message.attach(part)

        # Enviar el correo a través de SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, message.as_string())
        print(f"✅ Correo enviado a: {', '.join(recipients)}")

    except ValueError as ve:
        print(f"❌ Error de validación de correos: {ve}")
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")
