from flask import Flask, jsonify
from flask import request
from flask_cors import CORS
from gender_algorithm import postSuggestion
from gender_algorithm import mainfunction


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to my API!'})

@app.route('/postText', methods=['POST'])
def process():
    text = request.json['text']
    # Do something with the text
    returned_text = mainfunction(text)
    return jsonify({'message': returned_text})

@app.route('/postSuggestion', methods=['POST'])
def suggestion():
    text = request.get_json()
    print(text)
    returned_text = postSuggestion(text)
    return jsonify({'message': returned_text})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)