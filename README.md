# Studienarbeit_Gender_Programm

I understand, you want to analyze a German text and then determine the gender of the people mentioned in it, and then adjust the word accordingly, for example, making "Arbeiter" to "Arbeiter*innen".

Here's an example of how you could do this using Python:

Start by installing the necessary libraries such as spaCy, which is a library for advanced natural language processing in Python. You can install it by running pip install spacy in your command prompt.
Next, you'll need to download the German language model for spaCy using the following command: python -m spacy download de_core_news_sm
Once you have the libraries and the language model installed, you can start by loading the German language model in your Python script using the following code:
Copy code
import spacy
nlp = spacy.load("de_core_news_sm")
Next, you'll need to define the text you want to analyze. You can either define it as a string variable or read it from a file:
Copy code
text = "Das ist ein Beispieltext mit verschiedenen Personen. Der Arbeiter heißt Max Mustermann und die Arbeiterin heißt Lisa Musterfrau."
Now, you can use spaCy's nlp function to process the text and create a Doc object that contains all the information about the text's structure, entities and more:
Copy code
doc = nlp(text)
Next, you can iterate through the Doc object to extract all the named entities that are persons and determine their gender, then you can replace the word by it's gender-corrected version:
Copy code
for token in doc:
    if token.text in ["Arbeiter", "Arbeiterin"]:
        if token.text == "Arbeiter":
            if token.gender == "MALE":
                token.text = "Arbeiter*innen"
        elif token.text == "Arbeiterin":
            token.text = "Arbeiter*innen"

print(doc.text)
This code first loops through all the words in the text, and checks if the word is "Arbeiter" or "Arbeiterin", then based on the gender of the word, it replaces the word with "Arbeiter*innen", then it prints the text after modification.

Please keep in mind that this is just an example and it's possible that it may not work as expected for your specific use case, also the grammatical tags may vary
