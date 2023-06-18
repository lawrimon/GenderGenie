from flask import Flask, jsonify, request
from flask_cors import CORS
from gender_algorithm import GenderInator

app = Flask(__name__)
CORS(app)

gender_inator = GenderInator()

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to my API!'})

@app.route('/postText', methods=['POST'])
def process():
    text = request.json['text']
    # Do something with the text
    returned_text = gender_inator.main_function(text)
    return jsonify({'message': returned_text})

@app.route('/postSuggestion', methods=['POST'])
def suggestion():
    text = request.get_json()
    print(text)
    gender_inator.post_suggestion(text)
    return jsonify({'message': 'Suggestion received'})

@app.route('/automaticConversion', methods=['POST'])
def conversion():
    text = request.get_json()
    text = request.json['text']
    # Do something with the text
    returned_text = gender_inator.instant_conversion(text)
    print(type(returned_text))
    return jsonify(returned_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
