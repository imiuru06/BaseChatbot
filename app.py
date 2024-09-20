from flask import Flask, request, jsonify
from flask_cors import CORS
from src.config import config
from src.langchain_setup import get_chatbot_response

app = Flask(__name__)
CORS(app)

predefined_responses = config.get('predefined_responses', {})

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get('message', '').lower()
    response = predefined_responses.get(user_message)
    
    if not response:
        response = get_chatbot_response(user_message)
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)