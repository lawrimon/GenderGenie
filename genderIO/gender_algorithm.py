from spacy.tokens import Token
import re
import spacy
import pandas as pd
from pymongo import MongoClient


# Add 'gender' extension to Token with default value of None
Token.set_extension('gender', default=None)
nlp = spacy.load("de_core_news_sm")


import pandas as pd

def init_dict():
    # Load the Excel file into a DataFrame
    df = pd.read_excel('gender_tabelle.xlsx')

    # Extract the relevant columns
    col1 = df['ungegenderte Begriffe']
    col2 = df['gendergerechte Alternativen']

    # Create a dictionary from the two columns
    data = dict(zip(col1,col2))

    # Return the dictionary
    return data

def split_dict(string, dictionary):
    """
    Given a string and a dictionary, get the value of the string key in the dictionary and return a list of the split values
    """
    value = dictionary.get(string)
    return value.split(";")

def check_dict(string, my_dict):
    """
    Given a string and a dictionary, check if the string exists as a key in the dictionary.
    If it does, return a dictionary with the string key and the value being a list of the split values of the key in the original dictionary and the results of the second_check function.
    If it does not, return None.
    """
    if string in my_dict:
        array = split_dict(string, my_dict)
        star_sg, star_pl = second_check(string)
        array.append(star_sg)
        #array.append(star_pl)
        return {string:array}
    else:
        return None

def check_database(string, collection):
    word = find_word_database(string, collection)
    if word is not None:
        array = split_dict(string, word)
        star_sg = second_check(string)
        array.append(star_sg)
        return ({string: array})
    else:
        pass

def replace_words(file_path, word_list):
    with open(file_path, 'r') as file:
        content = file.read()

    for word in word_list:
        content = content.replace(word, f'//{word}//')

    with open(file_path, 'w') as file:
        file.write(content)

def find_word_position_in_string(string, word):
    lines = string.split('\n')
    for line_number, line in enumerate(lines):
        if word in line:
            print(f"The word '{word}' was found on line {line_number + 1}." )
            return
    return f"The word '{word}' was not found in the string."

def find_word_database(word, collection):
    document = collection.find_one({"word": word})
    # Check if the document was found
    try:
        if document:
            definition = document["definition"]
            return {word : definition}
        else:
            pass
    except:
        return document

def second_check(word):
    """
    Given a word, return the results of the replace_token_pl and replace_token_sg functions
    """
    word_sg = replace_token_sg(word)
    #word_pl = replace_token_pl(word)
    return word_sg

def check_wordending(word):
    doc = nlp(word)
    if not doc:
        print("kein DOC")
        return None
    token = doc[0]
    print(word)
    # Get the first token
    # Check if the first token is a noun
    if word == "Lügner":
        print("asahduh")
        try:
            print(token.pos_)
        except:
            pass
    try:
        if token.pos_ == "NOUN":
                if word.endswith("er") or word.endswith("en"):
                    return {word: word + "*in"}
        else:
            pass
    except:
        pass


def filter_non_letters(word):
  return re.sub(r'[^a-zA-ZüäöÜÄÖ-]+', '', word)

def replace_token_sg(word):
    """
    Given a token text, check if it ends with "er", "en", or "in".
    If it does, return a modified string by appending "*in" to it.
    If it does not, return None.
    """
    if word.endswith("er"):
        word= " "+ word + "*in"
    elif word.endswith("en"):
        word = word[:-2] + "*in"
    else:
        return None
    return word

def replace_token_pl(word):
    """
    Given a token text, check if it ends with "er", "en", or "in".
    If it does, return a modified string by appending "*in" to it.
    If it does not, return None.
    """
    print(type(word))
    if word.endswith("er"):
        word = word + "*in"
    elif word.endswith("en"):
        word = word[:-2] + "*in"
    else:
        return None
    return word

def mainfunction(text):
    client = MongoClient("mongodb+srv://admin:admin@genderinator.psfvydj.mongodb.net/?retryWrites=true&w=majority")
    db = client["GenderInator"]
    collection = db["GenderRegeln"]
    check_collection = db["Feedback"]

    #gender_dict = init_dict()
    result = []
    #upload_excel(gender_dict)
    for token in text.split():
        token = filter_non_letters(token)
        #find_word_position_in_string(text, token)
        #test_person(token)
        lol = find_word_database(token, check_collection)
        if(lol is not None):
            print("IM IFFFFF")
            continue

        else:
            dict_element = check_database(token, collection)

        if dict_element:
            result.append(dict_element)
        else:
            result_word = check_wordending(token)
            if result_word is not None:
                result.append(result_word)
        
    print(result)
    return result

def upload_excel(dict_array):

    print(dict_array)
    # Schritt 2: Verbinden Sie sich mit MongoDB
    client = MongoClient("mongodb+srv://admin:admin@genderinator.psfvydj.mongodb.net/?retryWrites=true&w=majority")
    db = client["GenderInator"]
    collection = db["GenderRegeln"]
    documents = [{"word": key, "definition": value} for key, value in dict_array.items()]

    # Schritt 3: Konvertieren und speichern Sie die Daten
    #collection.insert_many(documents)

def detect_person(text):
    doc = nlp(text)
    for token in doc:
        print("Token:", token)
        print("Text:", token.text)
        print("Lemma:", token.lemma_)
        print("POS:", token.pos_)
        print("Tag:", token.tag_)
        print("Dep:", token.dep_)
        print("Shape:", token.shape_)
        print("Alpha:", token.is_alpha)
        print("Stop:", token.is_stop)
        try:
           print("Number:",token.tag_)
           if "PLURAL" in token.tag_:
                print("NIEMALS")
        except:
            pass
        print("\n")
    for ent in doc.ents:
        if ent.label_ == "PERSON" or ent.label_ == "PROPN" or ent.label_ == "NOUN":
            return True
    return False

def test_person(word):
    if detect_person(word):
        print("The text refers to a person")
    else:
        return

def postSuggestion(text):
    client = MongoClient("mongodb+srv://admin:admin@genderinator.psfvydj.mongodb.net/?retryWrites=true&w=majority")
    db = client["GenderInator"]
    collection = db["GenderSuggestions"]
    print("this the text",text)
    #collection.insert_one(text)


def postFeedback(text):
    client = MongoClient("mongodb+srv://admin:admin@genderinator.psfvydj.mongodb.net/?retryWrites=true&w=majority")
    db = client["GenderInator"]
    collection = db["Feedback"]
    print("this the text",text)
    collection.insert_one(text)