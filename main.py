import markdown
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, render_template, url_for, redirect
import google.generativeai as genai


load_dotenv("./keys.env")

app = Flask(__name__)
app.secret_key = os.environ.get("APP_PASSWORD")


def init_model():
    # Set the API key
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)

        # initialize the model
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    conversations = model.start_chat(history=[])
    return conversations

conversations_history = []

conversations = init_model()

# print(response.text)
def to_mark(text):
    return markdown.markdown(text)

@app.route("/", methods=["GET"])
def home():
    # Get the user's message from the request body

    # Return the response to the user
    return render_template('chat-bot-welcome.html')


@app.route("/home", methods=["GET"])
def chat():
    # Get the user's prompt from the request body    
    return render_template('chat-bot.html',conversations=conversations_history)

@app.route("/process", methods=["POST"])
def processchat():
    # Get the user's message from the request body
    if request.method == 'POST':
        # print('seennnnnnnn')
        user_input = request.form['user_input']
        chat = conversations.send_message(
            user_input,
            safety_settings={
                'HATE': 'BLOCK_NONE',
                'HARASSMENT': 'BLOCK_NONE',
                'SEXUAL' : 'BLOCK_NONE',
                'DANGEROUS' : 'BLOCK_NONE'}
            )

        conversations_history.append({'role': 'user','text': user_input})
        conversations_history.append({'role': 'model','text': to_mark(chat.text)})
        # Return the response to the user
        return redirect(url_for('chat'))

@app.route("/login", methods=["GET","POST"])
def login():
    # Get the user's message from the request body

    # Return the response to the user
    return render_template('login.html')

@app.route("/register", methods=["GET","POST"])
def register():
    # Get the user's message from the request body

    # Return the response to the user
    return render_template('register.html')

@app.route("/forgot", methods=["GET","POST"])
def forgot():
    # Get the user's message from the request body

    # Return the response to the user
    return render_template('forgot.html')


# @app.route("/logout", methods=["GET"])
# def conversation():
#     # Get the user's message from the request body

#     # Return the response to the user
#     return render_template('chat-bot-welcome.html')

if __name__ == "__main__":
    app.run()

