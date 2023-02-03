from spacy.tokens import Token
import re

# Add 'gender' extension to Token with default value of None
Token.set_extension('gender', default=None)

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

def replace_words(file_path, word_list):
    with open(file_path, 'r') as file:
        content = file.read()

    for word in word_list:
        content = content.replace(word, f'//{word}//')

    with open(file_path, 'w') as file:
        file.write(content)





def second_check(word):
    """
    Given a word, return the results of the replace_token_pl and replace_token_sg functions
    """
    word_sg = replace_token_sg(word)
    word_pl = replace_token_pl(word)
    return word_sg, word_pl


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
    gender_dict = init_dict()
    result = []
    for token in text.split():
        token = filter_non_letters(token)
        dict_element = check_dict(token, gender_dict)
        if dict_element:
            result.append(dict_element)
    print(result)
    return result

