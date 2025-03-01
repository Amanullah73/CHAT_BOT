from flask import Flask, request, jsonify, render_template
import re
import json
import os
import random
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load intents from JSON file
def load_intents(file_path):
    if not os.path.exists(file_path):
        logging.warning(f"Warning: {file_path} not found. Chatbot will start with no predefined responses.")
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data.get("intents", [])
    except json.JSONDecodeError:
        logging.error("Error: Could not decode JSON. Please check the format of intents.json.")
        return []

# Load intents
intents = load_intents('intents.json')

if not intents:
    logging.warning("Chatbot has no predefined responses. Please check intents.json.")

def generate_response(message):
    try:
        for intent in intents:
            pattern = intent.get("pattern", "")
            if re.search(pattern, message, re.IGNORECASE):  
                responses = intent.get("responses", [])
                if responses:
                    return random.choice(responses)  # Choose a random response
                else:
                    return "I recognize that, but I don’t have a response yet!"
        
        return "I'm not sure how to respond to that. Can you ask something else?"
    except Exception as e:
        logging.error(f"Error in generate_response: {e}")
        return "Oops! Something went wrong. Try asking again."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message', '').strip()
    
    if not user_message:
        return jsonify({'response': "Please enter a message!"})
    
    bot_response = generate_response(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
