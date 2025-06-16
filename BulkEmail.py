import emails

def send_bulk_emails(user_email, app_password, subject, body, recipients):
    message = emails.html(
        subject=subject,
        html=f"<p>{body}</p>",
        text=body,
        mail_from=user_email
    )

    smtp_config = {
        "host": "smtp.gmail.com",
        "port": 587,
        "timeout": 10,
        "tls": True,
        "user": user_email,
        "password": app_password
    }

    status = {}

    for recipient in recipients:
        recipient = recipient.strip()
        print(f"Sending to {recipient}...")
        try:
            r = message.send(to=recipient, smtp=smtp_config)
            if r.status_code == 250:
                status[recipient] = "✅ Sent"
            else:
                status[recipient] = f"❌ Failed (Code: {r.status_code})"
        except Exception as e:
            status[recipient] = f"❌ Error: {str(e)}"

    return status