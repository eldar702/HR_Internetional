import spacy
from spacy import displacy
import pandas as pd
import chardet
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

nlp = spacy.load("en_core_web_sm")
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

def highlight_important_words(filename):
    with open('uploads/' + filename + '.csv', 'rb') as f:
        result = chardet.detect(f.read())

    text = pd.read_csv('uploads/' + filename + '.csv', encoding=result['encoding'], header=None)
    text = map(str, text.values[0])
    # Flatten the DataFrame into a single string
    raw_text = ' '.join(text)

    # Apply the regex expression and convert to lower case
    raw_text = re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?"', " ", raw_text)
    raw_text = raw_text.lower()

    # Tokenize, lemmatize and remove stop words
    tokens = raw_text.split()
    lm = WordNetLemmatizer()
    clean_text = ' '.join(lm.lemmatize(token) for token in tokens if token not in set(stopwords.words("english")))

    # Process the clean text with nlp to extract entities
    doc = nlp(clean_text)

    # Extract entities (words) from the doc and return them
    entities = [ent.text for ent in doc.ents]
    return entities
