# 📞 Automated Call Answering Bot

An automated call answering system built with **Python (Flask)** and **Twilio Voice API**.  
This bot answers customer calls, plays a predefined greeting, records their concern, converts the recording to text using **Google Cloud Speech-to-Text**, and sends the transcript to the business owner via email.  

---

## 🚀 Features
- 📞 **Automated Call Handling** – Answers incoming calls without human intervention.  
- 🎙 **Dual Input** – Supports DTMF keypad input and voice input.  
- 📝 **Voice Recording & Transcription** – Records caller’s message and converts speech to text.  
- 📧 **Email Notifications** – Sends transcripts directly to the owner’s email inbox.  
- ⚡ **Asynchronous Processing** – Uses threading for smooth background tasks.  

---

## 🛠 Tech Stack
- **Backend Framework**: Python, Flask  
- **Telephony**: Twilio Voice API  
- **Speech Processing**: Google Cloud Speech-to-Text  
- **Email Service**: SMTP (Gmail)  
- **Utilities**: `dotenv`, `threading`, `requests`, `ngrok`  

---

## 📂 Project Flow
1. Customer calls the office number.  
2. Bot greets them and gives options (e.g., *Press 1 to record your concern*).  
3. Caller records their message and presses `#` to save.  
4. Recording is uploaded to Twilio and fetched by the Flask app.  
5. Google Speech-to-Text transcribes the audio into text.  
6. The transcript is emailed to the business owner automatically.  

---

## ⚙️ Setup & Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/automated-call-bot.git
   cd automated-call-bot
Create and activate a virtual environment:



python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
Install dependencies:


pip install -r requirements.txt
Configure environment variables in .env:

env
Copy code
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth
GMAIL_USER=your_email@gmail.com
GMAIL_PASS=your_app_password
Add Google Cloud credentials:

Download credentials.json from Google Cloud Console.

Save it in the project root.

Set the path:


export GOOGLE_APPLICATION_CREDENTIALS="credentials.json"
Run the Flask server:


python src/index.py
Expose with ngrok:


ngrok http 5000
Update your Twilio webhook with the ngrok URL.

📧 Email Sample
When a customer leaves a message, the owner receives an email like:


Subject: Customer Complaint from Auto Bot
Body:
New Customer Message:

"I need help with my recent order. It hasn’t arrived yet."

------

🚀 Future Improvements
Add support for multiple languages.

Store transcripts in a database (MongoDB/PostgreSQL).

Integrate with AI (OpenAI/LLMs) for intelligent auto-replies.

Add a web dashboard for transcript management.

👤 Author
Aditya
📧 Adicanada.1088@gmail.com


