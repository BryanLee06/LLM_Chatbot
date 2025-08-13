from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from mistral_model import generate_response
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Ensure the secret key is set
if not app.config['SECRET_KEY']:
    raise RuntimeError("SECRET_KEY is not set. Please set it in your .env file or environment variables.")

@app.route('/')
def home():
    if 'initial_prompt' not in session:
        return redirect(url_for('initial_setup'))
    
    # Initialize chat_history in session if it doesn't exist for a new session
    if 'chat_history' not in session:
        session['chat_history'] = []

    return render_template('chat.html', initial_prompt=session['initial_prompt'])

@app.route('/initial_setup', methods=['GET', 'POST'])
def initial_setup():
    if request.method == 'POST':
        initial_prompt_text = request.form['initial_prompt']
        session['initial_prompt'] = initial_prompt_text
        session.pop('chat_history', None) 
        return redirect(url_for('home'))
    return render_template('initial_prompt.html')

@app.route('/reset_prompt', methods=['POST'])
def reset_prompt():
    session.pop('initial_prompt', None)
    session.pop('chat_history', None)
    return jsonify(success=True)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    
    initial_prompt = session.get('initial_prompt')
    current_chat_history = session.get('chat_history', [])

    response_text = generate_response(user_input, initial_prompt, current_chat_history)

    current_chat_history.append({"role": "user", "parts": [{"text": user_input}]})
    current_chat_history.append({"role": "assistant", "parts": [{"text": response_text}]})
    
    session['chat_history'] = current_chat_history
    
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)