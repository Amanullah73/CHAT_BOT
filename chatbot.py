from flask import Flask, request, jsonify, render_template
from nltk.chat.util import Chat, reflections
import os

app = Flask(__name__)

# Function to load pairs from a file with error handling
def load_pairs(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} was not found.")
    
    pairs = []
    with open(file_path, 'r') as file:
        for line in file:
            if '|' in line:
                pattern, response_str = line.strip().split('|')
                pattern = pattern.strip()
                responses = [response.strip() for response in response_str.split(';')]
                pairs.append([pattern, responses])
    return pairs

# Load pairs from the text file
try:
    pairs = load_pairs('pairs.txt')
except FileNotFoundError as e:
    print(e)
    pairs = []  # Fallback to an empty list if the file is not found

chatbot = Chat(pairs, reflections)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message', '').strip()
    
    if not user_message:
        return jsonify({'response': "Please ask something!"})
    
    bot_response = generate_response(user_message)
    return jsonify({'response': bot_response})

def generate_response(message):
    try:
        response = chatbot.respond(message)
        if response is None:
            response = "I'm not sure how to respond to that. Can you ask something else?"
    except Exception as e:
        response = "Oops! Something went wrong. Try asking again."
        print(f"Error: {e}")  # Debugging purposes
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
