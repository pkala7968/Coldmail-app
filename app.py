import streamlit as st
from BulkEmail import send_bulk_emails

st.title("Bulk Email Sender")

with st.expander("🔐 How to enable 2FA and get an App Password (Gmail Help)"):
    st.markdown("""
    **Step 1: Enable 2-Step Verification**
    
    - Go to your Google Account: [myaccount.google.com/security](https://myaccount.google.com/security)
    - Under **“Signing in to Google”**, click **2-Step Verification**.
    - Follow the steps to turn it on.

    **Step 2: Generate an App Password**
    
    - Once 2FA is on, go to: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
    - Sign in if prompted.
    - Under **"Select app"**, choose **Mail**.
    - Under **"Select device"**, choose **Other**, name it something like *ColdMail*.
    - Click **Generate**, and copy the 16-character password shown.

    🔒 **Your account stays safe!** This password only works for sending emails — you can revoke it anytime from the same page.
    """, unsafe_allow_html=True)

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
            st.write(f"{email.strip()}: {status}")