import streamlit as st
from BulkEmail import send_bulk_emails

st.title("Bulk Email Sender")

with st.form("email_form"):
    st.subheader("📝 Email Details")
    user_email = st.text_input("Your Gmail Address")
    app_password = st.text_input("App Password (not your real password)", type="password")
    subject = st.text_input("Email Subject")
    body = st.text_area("Email Body", height=200)
    recipients_input = st.text_area("Recipient Email Addresses (comma-separated)", height=100)

    submitted = st.form_submit_button("Send Emails")

if submitted:
    if not all([user_email, app_password, subject, body, recipients_input]):
        st.error("Please fill in all fields.")
    else:
        recipients = recipients_input.split(",")
        st.info("Sending emails, please wait...")
        result = send_bulk_emails(user_email, app_password, subject, body, recipients)
        st.success("Done! Here are the results:")
        for email, status in result.items():
            st.write(f"📧 {email.strip()}: {status}")