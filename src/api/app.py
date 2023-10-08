from flask import Flask, render_template, request
from chatbot import Chatbot
from llama_index import StorageContext, load_index_from_storage
import os


# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir='src/api')
# load index
index = load_index_from_storage(storage_context)

app = Flask(__name__)

@app.route('/')
def chatUI():

    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    bot = Chatbot(os.environ.get("OPENAI_API_KEY"), index=index, user_id=1)
    bot.load_chat_history()
    msg = request.form["msg"]
    input = msg
    return get_Chat_response(input, bot)

def get_Chat_response(text, bot):
    
    response = bot.generate_response(text)

    return response['content']

def test_response(text):
    return "Hello!"

if __name__ == '__main__':
    app.run(debug=True)
