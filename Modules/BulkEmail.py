from email.message import EmailMessage
import smtplib

def send_bulk_emails(user_email, app_password, subject, body, recipients, attachment_file=None, filename=None):
    results = {}
    for recipient in recipients:
        # Create a new message for each recipient
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = user_email
        message["To"] = recipient.strip()
        message.set_content(body)
        if attachment_file and filename:
            message.add_attachment(
                attachment_file,
                maintype="application",
                subtype="octet-stream",
                filename=filename
            )
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(user_email, app_password)
                smtp.send_message(message)
            results[recipient] = "✅ Sent"
        except Exception as e:
            results[recipient] = f"❌ Error: {str(e)}"
    return results