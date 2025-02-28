# Ritonix - RIT Chatbot

## 📌 Project Overview
**Ritonix** is an AI-powered chatbot designed to assist students with queries related to **canteen menus, bus schedules, KTU results, library access, and more** at Rajiv Gandhi Institute of Technology (RIT). The chatbot integrates with **Google Fit, Apple Health, and Samsung Health** to track users' steps and reward them with coins, which can be redeemed for premium chatbot access.

## 🚀 Features
- **FAQ Assistance**: Answers frequently asked questions from a MySQL database.
- **Canteen Menu**: Displays daily food items with prices.
- **Bus Schedule Lookup**: Extracts bus timings from a PDF.
- **KTU Results & ETLab Login Links**: Provides easy access to student portals.
- **Library Information**: Quick access to the Central Library website.
- **Google Fit Integration**: Tracks steps and rewards users with coins.
- **Gemini AI Integration**: Uses Google's Gemini AI to answer general queries.

## 🛠️ Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Database**: MySQL (pymysql)
- **APIs & Integrations**:
  - Google Fit API
  - Google OAuth 2.0 Authentication
  - Gemini AI (Generative AI)
  - PyMuPDF (for extracting text from PDFs)

## 📂 Project Structure
```
ritonix/
├── src/
│   ├── app.py          # Flask backend
│   ├── templates/
│   │   ├── index.html  # Chatbot UI
│   ├── static/
│   │   ├── styles.css  # CSS styles
│   │   ├── script.js   # Frontend logic
├── data/
│   ├── bus_schedule.pdf  # Bus schedules stored in PDFs
├── README.md          # Project documentation
```

## 🔧 Setup & Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/ritonix.git
cd ritonix
```
### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Set Up MySQL Database
- Create a MySQL database named `rit_chatbot`
- Import the required tables (`faq`, `users`, `canteen`, etc.)
- Update `app.py` with your **MySQL credentials**

### 4️⃣ Configure Google OAuth & Fit API
- Set up **OAuth 2.0 Client ID** in [Google Cloud Console](https://console.cloud.google.com/)
- Add `http://127.0.0.1:5000` to **Authorized JavaScript origins**
- Update `GENAI_API_KEY` in `app.py` with your **Gemini AI API key**

### 5️⃣ Run the Application
```bash
python app.py
```
Visit **http://127.0.0.1:5000** in your browser to chat with Ritonix!

## 📜 API Endpoints
| Endpoint          | Method | Description |
|------------------|--------|-------------|
| `/chat`         | POST   | Chat with the bot |
| `/google-fit`   | POST   | Fetch steps from Google Fit |
| `/canteen`      | GET    | Get the daily canteen menu |
| `/bus-schedule` | GET    | Retrieve bus timings by area |

## 🤝 Contributing
1. **Fork** the repository
2. **Create a feature branch** (`git checkout -b feature-name`)
3. **Commit changes** (`git commit -m "Added new feature"`)
4. **Push to GitHub** (`git push origin feature-name`)
5. **Open a Pull Request** 🚀

👨‍💻 Developed by **[Hogwarts Hackerdemy]** 🚀 
    Fidha Naisam-S6 CSE
    Raina Susan Ranjith-S6 CSE
    Emy Ann Ninan-S6 EEE
#REFERENCES
   OPENAI
   GEMINI API
   STACK OVERFLOW
