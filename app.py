from flask import Flask, request, jsonify
from flask_cors import CORS
from scripts.query_handler import ChatSession
import uuid
import json

app = Flask(__name__)
CORS(app)  # Only CORS, no async

sessions = {}

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    session_id = data.get('session_id') or str(uuid.uuid4())
    query = data.get('query', '')
    
    if session_id not in sessions:
        sessions[session_id] = ChatSession(session_id)
    
    response = sessions[session_id].ask(query)
    return jsonify({
        'session_id': session_id,
        'response': response
    })

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    with open('../data/feedback.jsonl', 'a') as f:
        f.write(json.dumps(data) + '\n')
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
