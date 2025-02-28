import os
from flask import Flask, request, jsonify, render_template
import pymysql
import fitz  # PyMuPDF for reading PDFs
import google.generativeai as genai
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from google.auth.exceptions import GoogleAuthError
from datetime import datetime, timedelta
import csv
import requests
from bs4 import BeautifulSoup

academic_calender_csv='Academic_calender-1.csv'

GENAI_API_KEY = "AIzaSyA497inZcjE1HLcQ18TJbGc894S8c2VmTw"  # Replace with your actual API key
genai.configure(api_key=GENAI_API_KEY)

app = Flask(__name__)
GOOGLE_FIT_ENDPOINT = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"

# Connect to MySQL Database
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",  # Change if needed
        password="Fidha@27",  # Add your MySQL password
        database="rit_chatbot",
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to fetch FAQ answer
def get_answer_from_db(question):
    '''conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM faq WHERE question=%s", (question,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None'''
    print("remove coments from get_answer_from_db function")

# Function to fetch and format the canteen menu
def get_canteen_menu():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT item_name, price FROM canteen;")  
    menu = cursor.fetchall()
    conn.close()
    
    print("DEBUG: Menu Data ->", menu)


    if not menu:
        return "<b>No menu available today.</b>"

    # Format as an HTML table
    formatted_menu = """
    <table border='1' style='border-collapse: collapse; width: 100%; text-align: center;'>
        <tr>
            <th style='padding: 8px; background-color: #f2f2f2;'>Item</th>
            <th style='padding: 8px; background-color: #f2f2f2;'>Price (₹)</th>
        </tr>
    """
    for item, price in menu:
        price = str(price)  # Convert Decimal to string
        formatted_menu += f"<tr><td style='padding: 8px;'>{item}</td><td style='padding: 8px;'>{price}</td></tr>"


    formatted_menu += "</table>"
    return formatted_menu

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def read_academic_calendar(csv_path):
    events = {}  # Dictionary to store events and their dates
    try:
        with open(csv_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                event = row[0].strip().lower()  # Convert event name to lowercase
                date = row[1].strip()
                events[event] = date  # Store event & corresponding date
    except Exception as e:
        return f"Error reading CSV: {str(e)}"
    
    return events  # Return the dictionary


def search_academic_event(query):
    events = read_academic_calendar(academic_calender_csv)  # Read CSV data


    # Define keyword mappings for different queries
    keywords = {
        "class start": ["commencement of", "class starts", "semester enrollment begins"],
        "exam date": ["exam", "examination", "series test", "end semester"],
        "holidays": ["holiday", "republic day", "deepavali", "christmas", "mahanavami", "good friday", "eid"],
        "semester end": ["class ends", "semester ends", "last date"]
    }

    

# Function to extract bus schedule for a specific area
def extract_bus_schedule(area_name, pdf_path="bus_schedule.pdf"):
    doc = fitz.open(pdf_path)  # Open the PDF
    extracted_data = ""

    for page in doc:
        text = page.get_text()
        lines = text.split("\n")  # Split text into lines
        
        # Search for the area in the extracted lines
        for i, line in enumerate(lines):
            if area_name.lower() in line.lower():
                extracted_data += f"🚌 **Bus Timings for {area_name.capitalize()}** 🕒\n"
                extracted_data += "--------------------------------------\n"

                # Collect the next few lines (assumed to contain bus timings)
                for j in range(i, min(i+3, len(lines))):  # Adjust range as needed
                    extracted_data += lines[j] + "\n"

                return extracted_data.strip()  # Return formatted results

    return f"❌ No bus schedule found for '{area_name}'. Please try another location."

# Function to provide the KTU results clickable link
def get_ktu_results_link():
    return "📢 Check KTU results here: <a href='https://t.me/ktu_results_bot' target='_blank'>KTU Results Bot</a>"

def get_ktu_site_link():
    return "📢 Check KTU page here: <a href='https://app.ktu.edu.in/eu/anon/refferError.htm' target='_blank'>KTU Official Page</a>"

'''def generate_gemini_response(query):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(query)
        return response.text.strip() if response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"Error generating AI response: {str(e)}" '''
    
def get_central_lib():
    return "📢 Check Central Library: <a href='https://www.rit.ac.in/central-library.php' target='_blank'> RIT Central Library</a>"

def get_etlab():
     return "📢 Check etlab student login: <a href='https://rit.etlab.in/user/login/' target='_blank'> ETLab Login</a>"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message").lower()

    if "hello" in user_message:
        bot_response = "Hi there! How can I assist you?"
    elif "events" in user_message:
        bot_response = "Upcoming events: Hackathon, TechFest, and Workshops!"
    elif "canteen menu" in user_message or "food items" in user_message or 'canteen'in user_message:  # Fixed condition
        bot_response = get_canteen_menu()  # Call the function properly
    elif "ktu result" in user_message or "ktu results" in user_message:  
        bot_response = get_ktu_results_link()
    elif "etlab login" in user_message or "etlab" in user_message:
        bot_response=get_etlab()
    elif "ktu site" in user_message or "ktu official site" in user_message:
        bot_response=get_ktu_site_link()  
    elif "library" in user_message or "books" in user_message or 'central library' in user_message:
        bot_response= get_central_lib()
    elif "bus schedule for" in user_message:
        area_name = user_message.replace("bus schedule for", "").strip()
        if area_name:
            bot_response = extract_bus_schedule(area_name)
        else:
            bot_response = "Please specify the area name (e.g., 'bus schedule for Alappuzha')."

    elif "class start" in user_message:
        bot_response = search_academic_event("class start")
    elif "exam date" in user_message or "exam" in user_message:
        bot_response = search_academic_event("exam date")
    elif "holidays" in user_message:
        bot_response = search_academic_event("holidays")
    elif "semester end" in user_message:
        bot_response = search_academic_event("semester end")
    else:
        #Check if the question is in the FAQ database
        db_response = get_answer_from_db(user_message)
        if db_response:
            bot_response = db_response
        else:
            # If not found in database, use Gemini AI
            bot_response = generate_enhanced_response(user_message)
    

    return jsonify({"response": bot_response})


# Fetch steps from Google Fit
def get_steps_from_google_fit(access_token, last_login):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Convert last login time to milliseconds
    start_time = int(last_login.timestamp() * 1000)
    end_time = int(datetime.utcnow().timestamp() * 1000)

    data = {
        "aggregateBy": [{"dataTypeName": "com.google.step_count.delta"}],
        "bucketByTime": {"durationMillis": 86400000},
        "startTimeMillis": start_time,
        "endTimeMillis": end_time,
    }
    response = requests.post(GOOGLE_FIT_ENDPOINT, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        total_steps = sum(
            bucket["dataset"][0]["point"][0]["value"][0]["intVal"]
            for bucket in result.get("bucket", [])
            if bucket["dataset"] and bucket["dataset"][0]["point"]
        )
        return total_steps
    return 0

@app.route("/google-fit", methods=["POST"])
def google_fit():
    data = request.json
    token = data.get("token")

    if not token:
        return jsonify({"error": "Missing token"}), 400

    try:
        # Verify Google Sign-In token
        user_info = id_token.verify_oauth2_token(token, Request())

        user_id = user_info["sub"]  # Unique Google ID
        access_token = token  # Temporary access token

        # Get last login time from DB
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT last_login FROM users WHERE user_id=%s", (user_id,))
        user = cursor.fetchone()
        last_login = user["last_login"] if user else datetime.utcnow() - timedelta(days=1)
# Get steps from Google Fit
        steps = get_steps_from_google_fit(access_token, last_login)
        coins_earned = steps // 1000  # 1 coin per 1000 steps

        # Update user data
        cursor.execute("""
            INSERT INTO users (user_id, last_login, coins)
            VALUES (%s, NOW(), %s)
            ON DUPLICATE KEY UPDATE last_login=NOW(), coins=coins+%s
        """, (user_id, coins_earned, coins_earned))
        conn.commit()
        conn.close()
        return jsonify({"steps": steps, "coins_earned": coins_earned})

    except GoogleAuthError as e:
            return jsonify({"error": "Google authentication failed", "message": str(e)}), 401

@app.route("/google-login", methods=["POST"])
def google_login():
    data = request.json
    token = data.get("token")

    if not token:
        return jsonify({"success": False, "message": "Missing token"}), 400

    try:
        # Verify Google OAuth Token
        user_info = id_token.verify_oauth2_token(token, Request())

        user_id = user_info["sub"]  # Unique Google ID
        user_email = user_info["email"]
        user_name = user_info.get("name", "Unknown")

        # Check if user exists in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
        user = cursor.fetchone()

        if not user:
            # New user: Insert into database
            cursor.execute("INSERT INTO users (user_id, email, name, last_login, coins) VALUES (%s, %s, %s, NOW(), 0)", 
                           (user_id, user_email, user_name))
        else:
            # Existing user: Update last login
            cursor.execute("UPDATE users SET last_login=NOW() WHERE user_id=%s", (user_id,))

        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Login successful", "user_id": user_id})

    except GoogleAuthError as e:
        return jsonify({"success": False, "message": "Google authentication failed", "error": str(e)}), 401


def generate_gemini_response(query):
    try:
        # Initialize model with specific configuration
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]

        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",  # Updated model name
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        prompt = f"""As an indian college engineering student, living in kerala, studing in Rajiv Gandhi Institute of Technology (RIT) located at Nedumkuzhy, Velloor, Pampady, Kerala 686501, please provide information about: {query}
        Keep the response concise, informative and relevant to academic context."""

        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text.strip()
        return "I apologize, but I couldn't generate a specific response for that query."
    
    except Exception as e:
        print(f"Gemini Error Details: {str(e)}")
        return "I'm currently experiencing technical difficulties. Please try asking about specific college-related topics or check our FAQ section."

def scrape_answer(query):
    try:
        # Clean and format the query for search
        search_query = query.replace(' ', '+')
        
        # Try to get answer from Wikipedia first
        wiki_url = f"https://en.wikipedia.org/wiki/{search_query}"
        response = requests.get(wiki_url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Get the first paragraph that's not empty
            paragraphs = soup.find_all('p')
            for para in paragraphs:
                if len(para.text.strip()) > 50:  # Ensure paragraph has substantial content
                    return para.text.strip()
        
        # If Wikipedia fails, try a Google search
        google_url = f"https://www.google.com/search?q={search_query}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(google_url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for featured snippets or direct answers
            snippet = soup.find('div', {'class': 'ILfuVd'})
            if snippet:
                return snippet.text.strip()
                
        return None
    except Exception as e:
        print(f"Scraping error: {str(e)}")
        return None

def generate_enhanced_response(query):
    try:
        # First try web scraping
        scraped_answer = scrape_answer(query)
        
        if scraped_answer:
            # Combine scraped answer with Gemini's response
            model = genai.GenerativeModel('gemini-pro')
            enhanced_prompt = f"""
            Based on this information: {scraped_answer}
            
            Please provide a clear and concise answer to: {query}
            Keep the response relevant and factual.
            """
            response = model.generate_content(enhanced_prompt)
            return response.text.strip() if response.text else scraped_answer
        
        # If scraping fails, fall back to regular Gemini response
        return generate_gemini_response(query)
        
    except Exception as e:
        print(f"Enhanced response error: {str(e)}")
        return generate_gemini_response(query)    

if __name__ == "__main__":
    app.run(debug=True)
