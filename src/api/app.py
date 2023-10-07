from flask import Flask, render_template, request
from chatbot import Chatbot

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    bot = Chatbot(os.environ.get("OPENAI_API_KEY"), index=index)
    bot.load_chat_history("chat_history.json")
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user_input = request.form.get('user_input')
        response = bot.generate_response(user_input)
    
        return render_template('chat.html', bot_response=response['content'])

    return render_template('chat.html')


if __name__ == '__main__':
    app.run(debug=True)
