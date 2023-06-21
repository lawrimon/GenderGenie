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

@app.route('/postFeedback', methods=['POST'])
def feedback():
     text = request.get_json()
     print(text)
     returned_text = gender_inator.post_feedback(text)
     return jsonify({'message': 'Feedback received!'})

# New endpoint to fetch all data of a specific collection
@app.route('/collection/<collection_name>', methods=['GET'])
def get_collection(collection_name):
    # Fetch the data from the specified collection
    data = gender_inator.get_collection_data(collection_name)

    return jsonify({'data': data})

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

@app.route('/<collection_name>/approve', methods=['POST'])
def approve(collection_name):
    text = request.get_json()
    word = text["word"]
    gender_inator.approve_document(collection_name,word)

    return jsonify("Succesfully approved")

@app.route('/<collection_name>/delete', methods=['POST'])
def delete(collection_name):
    print("in delte")
    text = request.get_json()
    word = text["word"]
    print(word)
    gender_inator.delete_document(collection_name, word)
    
    return jsonify("Succesfully deleted")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
