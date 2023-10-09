import os

os.environ["OPENAI_API_KEY"] = "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"



from llama_index import StorageContext, load_index_from_storage

# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir='/Users/manasadepu/Documents/GitHub/SASEHACK-Mental-Health-Real/FlaskTemplate/Flask_template/flaskShell/chatbot')
# load index
index = load_index_from_storage(storage_context)


import openai
import json

class Chatbot:
    def __init__(self, api_key, index, user_id):
        self.index = index
        openai.api_key = api_key
        self.user_id = user_id
        self.chat_history = []
        self.filename = f"{self.user_id}_chat_history.json"

    def generate_response(self, user_input):
        prompt = "\n".join([f"{message['role']}: {message['content']}" 
                           for message in self.chat_history[-5:]])
        prompt += f"\nUser: {user_input}"
        query_engine = index.as_query_engine()
        response = query_engine.query(user_input)

        message = {"role": "assistant", "content": response.response}
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append(message)
        return message
    
    def load_chat_history(self):
        try:
            with open(self.filename, 'r') as f:
                self.chat_history = json.load(f)
        except FileNotFoundError:
            pass

    def save_chat_history(self):
        with open(self.filename, 'w') as f:
            json.dump(self.chat_history, f)

