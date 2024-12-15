from dotenv import load_dotenv
import os
from flask import Flask, render_template, request
import google.generativeai as genai

# Load environment variables from the .env file
load_dotenv()

# Get the GEMINI_API_KEY from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if GEMINI_API_KEY is set
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set.")

# Configure the API key for Google Generative AI
genai.configure(api_key=gemini_api_key)

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-exp-1121",
    generation_config=generation_config,
)

# Start the chat session with predefined history
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "Please only answer about Introduction to Game Design & Development. Don't answer outside this scope.",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Okay, I understand. I will only answer questions related to **Introduction to Game Design & Development**. Ask me anything within that scope!\n",
            ],
        },
        # Add more predefined history here as needed
    ]
)

# Initialize Flask app
app = Flask(__name__)

# Define route for the index page
@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    
    # Handle POST request to send user input to the chatbot
    if request.method == "POST":
        user_input = request.form.get("user_input")
        
        if user_input:
            # Send user input to the chatbot
            response = chat_session.send_message(user_input)
            response_text = response.text
    
    # Render the index.html template with the response text
    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)
