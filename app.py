import streamlit as st
from Modules.BulkEmail import send_bulk_emails
from Modules.LLMemail import generate_emailbody
from Modules.Extraction import extract_text

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

# Initialization
if "email_list" not in st.session_state:
    st.session_state.email_list = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "ready_to_review" not in st.session_state:
    st.session_state.ready_to_review = False

# Input from user
uploaded_cv = st.file_uploader("Upload your resume :red[*]", type=["pdf", "docx", "txt"])

job_title = st.text_input("Job Title :red[*]", placeholder="Enter the job title you are applying for")

recipient_company_input = st.text_area(
    "Enter one company & recipient per line (format: Company Name, recipient@example.com) :red[*] :",
    height=150,
    placeholder="ABC Corp, hr@abc.com\nXYZ Ltd, jobs@xyz.com"
)

portfolio_links = st.text_area(
    "Enter you portfolio Links (comma-separated)",
    placeholder="https://linkedin.com/..., https://github.com/... etc.",
    height=50
)

user_email = st.text_input("Sender Email :red[*]",placeholder="Enter the email you want to send from")
app_password = st.text_input("App Password :red[*]", type="password",placeholder="Enter your Gmail App Password (Not your regular password!)")

if st.button("Generate Emails"):
    if not all([uploaded_cv, job_title, recipient_company_input]):
        st.error("Please upload your resume and enter Job Title & Company Name.")
        st.session_state.ready_to_review = False
    else:
        lines = recipient_company_input.strip().split("\n")
        st.session_state.email_list = []

        for line in lines:
            if "," in line:
                company, email = [x.strip() for x in line.split(",", 1)]
                uploaded_cv.seek(0)
                cv_text = extract_text(uploaded_cv)
                body = generate_emailbody(cv_text, job_title=job_title, company=company)
                if portfolio_links:
                    body += f"\n\n{portfolio_links.replace(',', '\n')}"
                subject = f"Job Application for {job_title} at {company}"
                st.session_state.email_list.append({
                    "company": company,
                    "email": email,
                    "subject": subject,
                    "body": body
                })

        st.session_state.ready_to_review = True
        st.session_state.current_index = 0

# Review & Send One by One
if st.session_state.ready_to_review and st.session_state.current_index < len(st.session_state.email_list):
    idx = st.session_state.current_index
    email_data = st.session_state.email_list[idx]

    st.subheader(f"Email {idx + 1} of {len(st.session_state.email_list)} - {email_data['company']}")
    subject = st.text_input("Subject", value=email_data["subject"], key=f"subject_{idx}")
    body = st.text_area("Body", value=email_data["body"], height=300, key=f"body_{idx}")

    if st.button("Send This Email"):
        uploaded_cv.seek(0)
        file_bytes = uploaded_cv.read()

        result = send_bulk_emails(
            user_email, app_password,
            subject, body,
            [email_data["email"]],
            attachment_file=file_bytes,
            filename=uploaded_cv.name
        )

        st.success(f"Sent to {email_data['email']}: {result[email_data['email']]}")
        
        # Advance to the next email
        st.session_state.current_index += 1

        # Force rerun so Streamlit re-renders next email
        st.rerun()

elif st.session_state.ready_to_review:
    st.success("✅ All emails sent!")
    st.session_state.ready_to_review = False
    st.session_state.email_list = []
    st.session_state.current_index = 0

