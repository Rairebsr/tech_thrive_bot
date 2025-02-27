import os
from flask import Flask, request, jsonify, render_template
import pymysql
import fitz  # PyMuPDF for reading PDFs
import google.generativeai as genai

GENAI_API_KEY = "AIzaSyA497inZcjE1HLcQ18TJbGc894S8c2VmTw"  # Replace with your actual API key
genai.configure(api_key=GENAI_API_KEY)

app = Flask(__name__)

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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM faq WHERE question=%s", (question,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "Sorry, I don't have an answer for that."

# Function to fetch and format the canteen menu
def get_canteen_menu():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT item_name, price FROM canteen")  
    menu = cursor.fetchall()
    conn.close()
    
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

def generate_gemini_response(query):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(query)
        return response.text.strip() if response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"Error generating AI response: {str(e)}"


@app.route("/")
def home():
    return render_template("index.html")  # Loads chatbot UI



@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message").lower()

        if "hello" in user_message:
            bot_response = "Hi there! How can I assist you?"
        elif "events" in user_message:
            bot_response = "Upcoming events: Hackathon, TechFest, and Workshops!"
        elif "canteen menu" in user_message or "food items" in user_message or 'canteen'in user_message:  # Fixed condition
            bot_response = get_canteen_menu()  # Call the function properly
        elif "bus schedule for" in user_message:
            area_name = user_message.replace("bus schedule for", "").strip()
            if area_name:
                bot_response = extract_bus_schedule(area_name)
            else:
                bot_response = "Please specify the area name (e.g., 'bus schedule for Alappuzha')."
        else:
            #Check if the question is in the FAQ database
            db_response = get_answer_from_db(user_message)
            if db_response:
                bot_response = db_response
            else:
                # If not found in database, use Gemini AI
                bot_response = generate_gemini_response(user_message)

        return jsonify({"response": bot_response})
    except Exception as e:
        print("Error",e)
        return jsonify({"response":"An error occured"}),500


if __name__ == "__main__":
    app.run(debug=True)
