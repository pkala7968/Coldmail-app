#  ColdMail: Job Applications Made Easy

So I am currently on the lookout for internships, and one thing I've learnt so far is that finding a good internship is really hard.  
I've tried several apps (Internshala, LinkedIn, JobsDB etc.) but it’s hard even getting a reply from employers.

So I thought **cold-mailing is the way**...  
But then again, you need to send multiple application emails to have a chance to be noticed, and copy-pasting the same ChatGPT-generated email again and again is also a chore...

### So I decided to automate it for us 😎

---

##  What is ColdMail?

ColdMail is a simple **Streamlit** web app that allows users to send personalized job application emails (using details from you resume/CV) to **Multiple Companies** in just a few clicks. The email is sent from Gmail account using a secure **App Password**.

---

##  Features

-  Upload your resume (PDF, DOCX, or TXT)
-  Uses Google Gemini AI to generate tailored email bodies
-  Send emails to multiple recipients using your Gmail account
-  Using a secure Gmail App Password (2FA required)
-  Review each email before sending
-  A clean and minimal UI

### Note: 
Your Gmail account is never stored anywhere.
You authenticate securely using a Gmail App Password (with 2FA enabled), so your credentials stay safe.

---

##  How to Run Locally

### 1. **Clone the repo**

```bash
git clone https://github.com/yourusername/ColdMail.git
cd ColdMail
```
### 2. **Install dependencies**

```bash
pip install -r requirements.txt
```
### 3. **Set up your API key**
Create a file named keys.env in the root directory:
```ini
API_KEY=your_gemini_api_key_here
```
### 4. **Fix the LLMemail code**
It has been changed for deployment. To run locally you need to go to [Modules/LLMemail.py](Modules/LLMemail.py) and un-comment the following:
```ini
# from dotenv import load_dotenv
# import os
## Load API key from keys.env file
# load_dotenv(dotenv_path="keys.env")
# api_key = os.getenv("API_KEY")
```
and comment out the api key used in deployment:
```ini
api_key = st.secrets["API_KEY"]
```
### 5. **Run the app**
```bash
streamlit run app.py
```

---

## Use the deployed tool

The project has been deployed using streamlit and can be used at: https://coldmail-v1.streamlit.app/

---

## Check it out!

![Input Body](images/Coldmail.png)
![Output Body](images/Action.png)

**Check out the demo 👉** [here](https://youtu.be/sr_B3sEyF5U)

---

## ⚠️ Note

This project is just a tool, it's an early deployment of a proper web application im working on...
(yeah I know I have too many projects on the shelf waiting for me 😭) — *pls be patient tho :)*
