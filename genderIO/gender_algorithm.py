from spacy.tokens import Token
import re
import spacy
import pandas as pd
from pymongo import MongoClient

class GenderInator:
    def __init__(self):
        Token.set_extension('gender', default=None)
        self.nlp = spacy.load("de_core_news_sm")
        self.client = MongoClient("mongodb+srv://admin:admin@genderinator.psfvydj.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["GenderInator"]
        self.gender_rules_collection = self.db["GenderRegeln"]
        self.suggestions_collection = self.db["GenderSuggestions"]

    def load_gender_dictionary(self, file_path):
        df = pd.read_excel(file_path)
        col1 = df['ungegenderte Begriffe']
        col2 = df['gendergerechte Alternativen']
        return dict(zip(col1, col2))

    def split_dict(self, string, dictionary):
        value = dictionary.get(string)
        return value.split(";") if value else []

    def check_dict(self, string, gender_dict):
        if string in gender_dict:
            array = self.split_dict(string, gender_dict)
            array.append(self.second_check(string))
            return {string: array}
        else:
            return None

    def check_database(self, string):
        word = self.find_word_database(string)
        if word:
            array = self.split_dict(string, word)
            array.append(self.second_check(string))
            return {string: array}
        else:
            return None

    def replace_words(self, file_path, word_list):
        with open(file_path, 'r') as file:
            content = file.read()

        for word in word_list:
            content = content.replace(word, f'//{word}//')

        with open(file_path, 'w') as file:
            file.write(content)

    def find_word_position_in_string(self, string, word):
        lines = string.split('\n')
        for line_number, line in enumerate(lines):
            if word in line:
                print(f"The word '{word}' was found on line {line_number + 1}.")
                return
        return f"The word '{word}' was not found in the string."

    def find_word_database(self, word):
        document = self.gender_rules_collection.find_one({"word": word})
        if document:
            definition = document["definition"]
            return {word: definition}
        else:
            return None

    def second_check(self, word):
        return self.replace_token_sg(word)

    def check_wordending(self, word):
        doc = self.nlp(word)
        if not doc:
            print("kein DOC")
            return None
        token = doc[0]
        print(word)
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
        except:
            pass

    def filter_non_letters(self, word):
        return re.sub(r'[^a-zA-ZüäöÜÄÖ-]+', '', word)

    def replace_token_sg(self, word):
        if word.endswith("er"):
            word = " " + word + "*in"
        elif word.endswith("en"):
            word = word[:-2] + "*in"
        else:
            return None
        return word

    def replace_token_pl(self, word):
        print(type(word))
        if word.endswith("er"):
            word = word + "*in"
        elif word.endswith("en"):
            word = word[:-2] + "*in"
        else:
            return None
        return word

    def detect_person(self, text):
        doc = self.nlp(text)
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
                print("Number:", token.tag_)
                if "PLURAL" in token.tag_:
                    print("NIEMALS")
            except:
                pass
            print("\n")
        for ent in doc.ents:
            if ent.label_ == "PERSON" or ent.label_ == "PROPN" or ent.label_ == "NOUN":
                return True
        return False

    def test_person(self, word):
        if self.detect_person(word):
            print("The text refers to a person")
        else:
            return

    def post_suggestion(self, text):
        self.suggestions_collection.insert_one(text)

    def main_function(self, text):
        gender_dict = self.load_gender_dictionary('gender_tabelle.xlsx')
        result = []
        for token in text.split():
            token = self.filter_non_letters(token)
            dict_element = self.check_database(token)
            if dict_element:
                result.append(dict_element)
            else:
                result_word = self.check_wordending(token)
                if result_word is not None:
                    result.append(result_word)

        print(result)
        return result

    def upload_excel(self, dict_array):
        documents = [{"word": key, "definition": value} for key, value in dict_array.items()]
        self.gender_rules_collection.insert_many(documents)
