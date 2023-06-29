import spacy
from spacy import displacy
import pandas as pd

nlp = spacy.load("en_core_web_sm")

def highlight_important_words(filename):
    text = pd.read_csv('uploads/' + filename + '.csv')
    doc = nlp(text)
    html = displacy.render(doc, style="ent")
    return html