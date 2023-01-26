from spacy.tokens import Token

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
        array.append(star_pl)
        return {string:array}
    else:
        return None

def second_check(word):
    """
    Given a word, return the results of the replace_token_pl and replace_token_sg functions
    """
    word_sg = replace_token_sg(word)
    word_pl = replace_token_pl(word)
    return word_sg, word_pl

def replace_token_sg(word):
    """
    Given a token text, check if it ends with "er", "en", or "in".
    If it does, return a modified string by appending "*in" to it.
    If it does not, return None.
    """
    if word.endswith("er"):
        word= word + "*in"
    elif word.endswith("en"):
        word = word[:-2] + "*in"
    elif word.endswith("in"):
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
    elif word.endswith("in"):
        word = word[:-2] + "*in"
    else:
        return None
    return word

def main():
    gender_dict = init_dict()
    text = "Die Software wurde für Manager und Geschäftsführer von großen Institutionen (mehr als 300 Mitarbeiter) erstellt und ist besonders für Anfänger sehr benutzerfreundlich. Jeder, der die Software zum ersten mal verwendet, wird erstaunt sein, wie leicht sie zu bedienen ist. Durch die beiliegende CD können Anwender die Software unkompliziert installieren. Bei Problemen stehen den Firmen außerdem unsere Techniker rund um die Uhr zur Verfügung: der jeweils zuständige IT-Experte schaltet sich sofort online zu. Außerdem ist innerhalb von 24 Stunden ein Vertreter unserer Firma vor Ort. (Verfasser: Firma SoftManagement)"
    result = []
    for token in text.split():
        dict_element = check_dict(token, gender_dict)
        if dict_element:
            result.append(dict_element)
    print(result)

    
main()