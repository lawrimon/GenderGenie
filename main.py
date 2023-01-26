import spacy
from nltk.stem.snowball import SnowballStemmer
from spacy.tokens import Token
from HanTa import HanoverTagger as ht
Token.set_extension('gender', default=None)
import pandas as pd

def init_dictionary():
    df = pd.read_excel('gender_tabelle.xlsx')
   
    # Extract the relevant columns by index
    #data = df.iloc[:, [0,1]].set_index(0).to_dict()
    #data = df[['ungegenderte Begriffe', 'gendergerechte Alternativen']].to_dict()
    data = df.iloc[:, [0,1]].to_dict()
    print(df.iloc[:, [0]])
    #print(df)

    # Print the dictionary
    #print(data)

    return data

def init_dict():
    import pandas as pd

    # Load the Excel file into a DataFrame
    df = pd.read_excel('gender_tabelle.xlsx')

    # Extract the relevant columns
    col1 = df['ungegenderte Begriffe']
    col2 = df['gendergerechte Alternativen']

    # Create a dictionary from the two columns
    data = dict(zip(col1,col2))

    # Print the dictionary
    #print(data)
    return data

def split_dict(str, dict):
    x = dict.get(str)
    return x.split(";")

def check_dict(str, my_dict):
    if str in my_dict:
        #print("Key ", str, " exists in the dictionary.")
        array = split_dict(str, my_dict)
        #print("This are the coresponding values: ", array)
        star_sg, star_pl = second_check(str)
        array.append(star_sg)
        array.append(star_pl)
        '''
        Insert *in function here
        '''
        return {str:array}
    else:
        #print("Key ", str, " does not exist in the dictionary.")
        pass

# Load the German language model in Spacy
nlp = spacy.load("de_core_news_sm")
# Initialize the stemmer
tagger = ht.HanoverTagger('morphmodel_ger.pgz')

# Initialize the stemmer
stemmer = SnowballStemmer("german")

# Define the word to stem
word = "Fußballspielern"

# Load the German language model
nlp = spacy.load("de_core_news_sm")

def GenderAlgorithm(text):
    """
    Function that takes in a text and applies the gender algorithm to it.
    """
    word_list = []
    # Process the text with spaCy
    doc = nlp(text)

    # Call the function to update the text
    for token in doc:
        word = second_check(token)
        if word is not None:
            word_list.append(word)
    

    # Make a spaCy Doc from the updated tokens
    #doc = nlp.make_doc(' '.join(updated_tokens))

    # Print the modified text
    #print(token_list)
    print("Der GenderCounter hat", len(word_list), "Stellen gendert")

def second_check(word):
    #token_text = token.text
    # Check if the word is a noun
    #if token.pos_ == "NOUN" and token.tag_ == "NN" and token_text.endswith("er"):
    word_pl = replace_token_pl(word)
    word_sg = replace_token_sg(word)
    return word_sg, word_pl
    #else: return None

def check_gender_list(gender_list, word):
    for i in gender_list:
        if word in i:
            i.get(word)


def update_text(doc):
    """
    Function that takes in a spaCy Doc, updates the text, and returns the updated tokens and a gender counter.
    """
    updated_tokens = []
    token_list = []

    # Iterate through the words in the text
    for token in doc:
        token_text = token.text
        # Check if the word is a noun
        if token.pos_ == "NOUN" and token.tag_ == "NN" and token_text.endswith("er"):
            print(token)
            if token.ent_type_ == "PER":
                print("2")
                tokenText = token.lemma_
                
                # Check the gender of the noun
                token_list = create_tokenList(token_text, token_list)
        #updated_tokens.append(token_text)
    return token_list

def replace_token_sg(tokenText):
    if tokenText.endswith("er"):
        token_text = tokenText + "*in"
    elif tokenText.endswith("en"):
        token_text = tokenText[:-2] + "*in"
    elif tokenText.endswith("in"):
        token_text = tokenText[:-2] + "*in"
    else:
        return None
    return token_text

def replace_token_pl(tokenText):
    if tokenText.endswith("er"):
        token_text = tokenText + "*innen"
    elif tokenText.endswith("en"):
        token_text = tokenText[:-2] + "*innen"
    elif tokenText.endswith("in"):
        token_text = tokenText[:-2] + "*innen"
    else:
        return None
    return token_text

def create_tokenList(token_text,token_list):
    token_dict = {token_text: replace_token(token_text)}
    if token_dict.get(token_text) is not None:
        token_list.append(token_dict)
    return token_list

def test_text():
    import stanfordnlp

    # Download and load the German model
    nlp = stanfordnlp.Pipeline(lang='de')

    # Process the text
    text = "Ich bin Freund von der Firma und mein Kollege ist auch Freund und ein IT-Experte"
    doc = nlp(text)

    # Iterate through the tokens
    for sent in doc.sentences:
        for word in sent.words:
            try:
                #print(word)
                print(word.upos)
                feats = word.feats
                feats_list = feats.split("|")
                gender = [x.split("=")[-1] for x in feats_list if x.startswith("Gender=")][0]
                print(f"{word.text} - Gender: {gender}")
            except Exception as Error:
                print(Error)
                
            #if token.words.upos == 'NOUN' and token.Gender == "Masc":
            #       print(f"'{token.text}' is a noun that refers to a person.")

def main():
    result = []
    # Init dict
    gender_dict = init_dict()
    # Insert Text
    text = "Die Software wurde für Manager und Geschäftsführer von großen Institutionen (mehr als 300 Mitarbeiter) erstellt und ist besonders für Anfänger sehr benutzerfreundlich. Jeder, der die Software zum ersten mal verwendet, wird erstaunt sein, wie leicht sie zu bedienen ist. Durch die beiliegende CD können Anwender die Software unkompliziert installieren. Bei Problemen stehen den Firmen außerdem unsere Techniker rund um die Uhr zur Verfügung: der jeweils zuständige IT-Experte schaltet sich sofort online zu. Außerdem ist innerhalb von 24 Stunden ein Vertreter unserer Firma vor Ort. (Verfasser: Firma SoftManagement)"

    # Search for specific Words in the dictionary
    for i in text.split():
        dict_element = check_dict(i,gender_dict)
        if dict_element is not None:
            result.append(dict_element)

    print(result)
    # Search Text for words that are a Person + Noun
    #GenderAlgorithm(text)

    # Create an array where all the first elements are the key values and the following are the Empfehlungen or a dictionary

    # Return All the words that have to be gendered

    pass

#test_text()
main()