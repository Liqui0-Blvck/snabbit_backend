# En un archivo como read_emails.py
import imaplib
import email

def read_emails():
    # Configuración de acceso al servidor IMAP
    mail = imaplib.IMAP4_SSL('outlook.office365.com')
    mail.login('ncortes@snabb-it.cl', 'Nos20204')
    mail.select('inbox')

    # Búsqueda de correos electrónicos no leídos
    result, data = mail.search(None, 'UNSEEN')

    # Iteración sobre los correos electrónicos encontrados
    for num in data[0].split():
        result, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Extraer el asunto, cuerpo y remitente del correo
        subject = msg['subject']
        body = ''
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if "attachment" not in content_disposition:
                    body += part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()
        sender = msg['from']

        # Crear un objeto Ticket y guardar en la base de datos

    # Cerrar la conexión
    mail.close()
    mail.logout()

# Llamar a la función para leer correos electrónicos
read_emails()
