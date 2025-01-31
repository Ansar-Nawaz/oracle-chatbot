from flask import Flask, request, jsonify
from scripts.query_handler import get_answer

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('query', '')
    response = get_answer(user_query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

