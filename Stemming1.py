
'''
import spacy

from HanTa import HanoverTagger as ht

tagger = ht.HanoverTagger('morphmodel_ger.pgz')

#lemmata = tagger.tag_sent(words,taglevel= 1)

# Lade das deutsche spacy-Modell
nlp = spacy.load("de_core_news_sm")

# Gebe den Satz ein, in dem du die Nomen suchen möchtest
sentence = "Der Mann ist ein Fußballspieler und ein Mülltrennerin"


# Verwende das spacy-Modell, um den Satz zu analysieren
doc = nlp(sentence)

# Gehe durch alle Wörter im Satz
for token in doc:
    # Überprüfe, ob das Wort ein Nomen ist
    if token.pos_ == "NOUN":
        print("this the Token", token)
        #tags = tagger.tag_sent(str(token), taglevel= 1)
        print(f"{token.text} ist ein Nomen.")
        #print("das sind die tags",tags)
        
        lemma = tagger.makelemma(str(token), pos="NN", upcase=True)
        print(lemma)
        #lemma = tagger.lemmatize(token, "NN")
        #print(f"Der Wortstamm von {token} ist {lemma}.")
'''

import spacy
from spacy.tokens import Token
Token.set_extension('gender', default=None)
#import korpora
#from pymorfologik import Morfologik

from pyMorfologik import Morfologik
from pyMorfologik.parsing import ListParser

import nltk
from HanTa import HanoverTagger as ht

import re

# Load the German language model in Spacy
nlp = spacy.load("de_core_news_sm")
# Initialize the stemmer
tagger = ht.HanoverTagger('morphmodel_ger.pgz')

# Process a German sentence
sent = "Das ist schon sehr schön mit den Expertinnen und Experten."
words = nltk.word_tokenize(sent)
lemmata = tagger.tag_sent(words,taglevel= 1)


def try0(lemmata):
    # Load the German language model in Spacy
    nlp = spacy.load("de_core_news_sm")
    # Initialize the stemmer
    tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    # Process a German sentence
    sent = "Das ist schon sehr schön mit den Expertinnen und Experten. Mann Frau Arbeiter Fußballer Handballerin"
    words = nltk.word_tokenize(sent)
    doc = nlp(' '.join(words))

    for token in doc:
        if token.pos_ == "NOUN" and token._.gender == "PER":
            new_word = token.text
            if new_word.endswith("in") or new_word.endswith("e"):
                new_word = new_word[:-2] + '*innen'
            print(f'{new_word} is a person')
        else:
            print(f'{token.text} is not a person')


    dereko = korpora.get_corpus("DeReKo")

    # Check if the word "Experte" refers to a person
    lemma = dereko.lookup("Experte", pos="NN")[0]
    if "person" in lemma["semantic_fields"]:
        print("'Experte' is a person")
    else:
        print("'Experte' is not a person")

def try2():

    # Initialize the stemmer
    m = Morfologik()

    # Analyze the word "Experte"
    analysis = m.analyze("Experte")

    # Check if the word is a noun and if the semantic field includes "person"
    if any(tag.startswith('subst:') and 'person' in sem for tag, sem in analysis):
        print("'Experte' is a person")
    else:
        print("'Experte' is not a person")

def try3():
    from transformers import AutoModelForTokenClassification, AutoTokenizer

    # Load the pre-trained BERT model
    model = AutoModelForTokenClassification.from_pretrained("bert-base-german-cased")
    tokenizer = AutoTokenizer.from_pretrained("bert-base-german-cased")

    # Define the word to classify
    word = "Experte"

    # Encode the word as input for BERT
    encoded_input = tokenizer.encode_plus(word, add_special_tokens=True, return_tensors='pt')
    input_ids = encoded_input['input_ids']

    # Get the logits from the model
    logits = model(input_ids)[0]

    # Get the predicted labels for the word
    predicted_labels = logits.argmax(1)
    print(predicted_labels)
    # Get the label for "B-PER"
    #per_label_id = model.config.id2label[predicted_labels[0]]
    if predicted_labels.argmax().item() in model.config.id2label:
        per_label_id = model.config.id2label[predicted_labels.argmax().item()]

    if "PER" in per_label_id:
        print(f"'{word}' is a person")
    else:
        print(f"'{word}' is not a person")

def try4():


    # Initialize the morphological analyzer
    analyzer = Morfologik()

    # Define the word to check
    word = "Experte"

    # Analyze the word
    #analysis = analyzer.analyze(word)
    analysis = analyzer.lookup(word)

    # Check if the word is a person
    is_person = False
    for a in analysis:
        if 'subst:sg:nom:m1' in a[1]:
            is_person = True
            break

    if is_person:
        print(word + " references to a person")
    else:
        print(word + " does not reference to a person")

def try5():
    import spacy

    # Load the German language model
    nlp = spacy.load("de_core_news_sm")

    # Define the sentence to check
    sentence = "Das ist schon sehr schön mit den Experten und Expertinnen"

    # Process the sentence
    doc = nlp(sentence)

    # Check if any of the words are persons
    for token in doc:
        # Check if the word is a person
        if token.pos_ == "NOUN" and token.tag_ == "NN":
            print(token.text + " references to a person")
        else:
            print(token.text + " does not reference to a person")

def try6():
    import spacy
    from nltk.stem.snowball import SnowballStemmer

    # Initialize the stemmer
    stemmer = SnowballStemmer("german")

    # Define the word to stem
    word = "Fußballspielern"

    # Load the German language model
    nlp = spacy.load("de_core_news_sm")

    # Define the text to analyze
    text = "Das ist ein Beispieltext mit verschiedenen Personen. Der Arbeiter heißt Max Mustermann und die Lehrerin heißt Lisa Musterfrau."
    text2 = "Die Arbeiter der Firma haben sich bei den Chefen der Firma beschwerrt. Danach hat der Kollege Andreas Probleme gehabt mit den Fußballspielern den Nationalmannschaft"
    text3 = "Die Software wurde für Manager und Geschäftsführer von großen Institutionen (mehr als 300 Mitarbeiter) erstellt und ist besonders für Anfänger sehr benutzerfreundlich. Jeder, der die Software zum ersten mal verwendet, wird erstaunt sein, wie leicht sie zu bedienen ist. Durch die beiliegende CD können Anwender die Software unkompliziert installieren. Bei Problemen stehen den Firmen außerdem unsere Techniker rund um die Uhr zur Verfügung: der jeweils zuständige IT-Experte schaltet sich sofort online zu. Außerdem ist innerhalb von 24 Stunden ein Vertreter unserer Firma vor Ort. (Verfasser: Firma SoftManagement)"

    # Process the text with spaCy
    doc = nlp(text3)

    indefinite_pronouns = ["jeder", "jede", "jedes", "man", "alle", "andere", "keiner", "niemand", "wenige", "viele"]
    updated_tokens = []
    genderCounter = 0

       


# Print the modified text
    print(doc.text)
    # Iterate through the words in the text
    for token in doc:
        # Check if the word is a noun
        token_text = token.text
        if token.pos_ == "NOUN" and token.tag_ == "NN" or token_text.lower() in indefinite_pronouns:
            print(token.text)
            print(token.lemma_)            
            tokenText = token.lemma_
            # Check the gender of the noun
            if tokenText in indefinite_pronouns:
                token_text = "Jeder und Jede"
                genderCounter = genderCounter +1
            elif tokenText.endswith("er"):
                token_text = tokenText + "*innen"
                genderCounter = genderCounter + 1
            elif tokenText.endswith("en"):
                token_text = tokenText[:-2] + "*innen"
                genderCounter = genderCounter + 1
            elif tokenText.endswith("in"):
                token_text = tokenText[:-2] + "*innen"
                genderCounter = genderCounter + 1
            else:
                token_text = tokenText
        updated_tokens.append(token_text)

    doc = nlp.make_doc(' '.join(updated_tokens))
    # Print the modified text
    print(doc.text)
    print("Der GenderCounter hat",genderCounter,"Stellen gendert")




try6()


def try1(lemmata):
    # Go through each word and lemma pair
    for word in lemmata:
        print("this word",word)
        for lemma in lemmata:
            print("this lemma",lemma)
        # Check if the word is a noun
            if 'NN' in lemma:
                # Check if the word ends with 'in' or 'e'
                if word.endswith("in") or word.endswith("e"):
                    # Replace the last two characters with '*innen'
                    new_word = word[:-2] + '*innen'
                    print(new_word)
                else:
                    print(word)
            else:
                print(word)
