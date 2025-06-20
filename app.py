import streamlit as st
from Modules.BulkEmail import send_bulk_emails
from Modules.LLMemail import generate_emailbody

st.set_page_config(page_title="ColdMail", layout="centered")
st.title("ColdMail: email job applications with AI")

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
    """)

# form
uploaded_cv = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])
with st.form("email_form"):
    st.subheader("Email Details")

    #uploaded_cv = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])

    user_email = st.text_input("Enter Your Email Address")
    app_password = st.text_input("App Password (not your real password)", type="password")
    job_title = st.text_input("Job Title")
    company = st.text_input("Company Name")
    recipients_input = st.text_area("Recipient Email Addresses (comma-separated)", height=100)

    submitted = st.form_submit_button("Send Emails")

# Do everything AFTER submit
if submitted:
    if not all([user_email, app_password, job_title, company, recipients_input, uploaded_cv]):
        st.error("Please fill in all fields and upload your resume.")
    else:
        recipients = recipients_input.split(",")
        uploaded_cv.seek(0)
        file_bytes = uploaded_cv.read()
        uploaded_cv.seek(0)

        subject = f"Job Application for {job_title} at {company}"
        body = generate_emailbody(uploaded_cv, job_title=job_title, company=company)
        uploaded_cv.seek(0)

        st.info("Sending emails, please wait...")
        result = send_bulk_emails(
            user_email, app_password, subject, body,
            recipients,
            attachment_file=file_bytes,
            filename=uploaded_cv.name
        )

        st.success("Done! Here are the results:")
        for email, status in result.items():
            st.write(f"{email.strip()}: {status}")