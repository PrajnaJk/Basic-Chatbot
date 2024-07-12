from flask import Flask, render_template, request, jsonify
import spacy
from datetime import datetime


app = Flask(__name__)


nlp = spacy.load('en_core_web_sm')


responses = {
    "greet": ["Hello! How can I help you today?", "Hi there! What can I do for you?", "Hey!"],
    "name": ["I am a chatbot created by you. You can call me Chatbot."],
    "how are you": ["I'm just a chatbot, but I'm here to help you!"],
    "bye": ["Goodbye! Have a great day!", "See you later!", "Take care!"],
    "time": [f"The current time is {datetime.now().strftime('%H:%M:%S')}."],
    "date": [f"Today's date is {datetime.now().strftime('%Y-%m-%d')}."],
    "weather": ["I can't check the weather right now, but you can try asking a weather service!"],
    "joke": ["Why don't scientists trust atoms? Because they make up everything!", "Why did the scarecrow win an award? Because he was outstanding in his field!"],
    "help": ["I'm here to assist you. How can I help you?", "What do you need help with?"],
}

def get_intent(user_input):
    doc = nlp(user_input)
    for token in doc:
        if token.lemma_ in ["hi", "hello", "hey"]:
            return "greet"
        if "name" in user_input.lower():
            return "name"
        if "bye" in user_input.lower() or "goodbye" in user_input.lower():
            return "bye"
        if "time" in user_input.lower():
            return "time"
        if "date" in user_input.lower():
            return "date"
        if "weather" in user_input.lower():
            return "weather"
        if "joke" in user_input.lower():
            return "joke"
        if "help" in user_input.lower():
            return "help"
        if "how are you" in user_input.lower():
            return "how are you"
    return None

def get_response(user_input):
    intent = get_intent(user_input)
    if intent and intent in responses:
        return responses[intent][0]
    else:
        return "I'm sorry, I don't understand that. Can you please rephrase?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response_route():
    user_input = request.form['user_input']
    response = get_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
