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

# Session state for email generation
if "email_generated" not in st.session_state:
    st.session_state.email_generated = False
if "subject" not in st.session_state:
    st.session_state.subject = ""
if "body" not in st.session_state:
    st.session_state.body = ""

# Upload resume before form
uploaded_cv = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"], key="cv_upload")

# --- Form ---
with st.form("email_form"):
    st.subheader("Email Details")

    user_email = st.text_input("Enter Your Email Address")
    app_password = st.text_input("App Password (not your real password)", type="password")
    job_title = st.text_input("Job Title")
    company = st.text_input("Company Name")
    recipients_input = st.text_area("Recipient Email Addresses (comma-separated)", height=100)

    generate_clicked = st.form_submit_button("Generate Email")

# Handle email generation
if generate_clicked:
    if not all([uploaded_cv, job_title, company]):
        st.error("Please upload your resume and enter Job Title & Company Name.")
    else:
        uploaded_cv.seek(0)
        st.session_state.body = generate_emailbody(uploaded_cv, job_title=job_title, company=company)
        st.session_state.subject = f"Job Application for {job_title} at {company}"
        st.session_state.email_generated = True
        st.success("Email generated! You can now review and send it.")

# Show editable fields if email is generated
if st.session_state.email_generated:
    st.subheader("📧 Review and Edit Email")

    subject = st.text_input("Email Subject", value=st.session_state.subject)
    body = st.text_area("Email Body", value=st.session_state.body, height=300)

    send_now = st.button("Send Emails")

    if send_now:
        if not all([user_email, app_password, recipients_input, uploaded_cv, subject, body]):
            st.error("Please fill in all fields before sending.")
        else:
            recipients = [email.strip() for email in recipients_input.split(",") if email.strip()]
            uploaded_cv.seek(0)
            file_bytes = uploaded_cv.read()
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
                st.write(f"{email}: {status}")
