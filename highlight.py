import spacy
from spacy import displacy
import pandas as pd
import chardet
nlp = spacy.load("en_core_web_sm")



def highlight_important_words(filename):
    with open('uploads/' + filename + '.csv', 'rb') as f:
        result = chardet.detect(f.read())  # or readline if the file is large

    text = pd.read_csv('uploads/' + filename + '.csv', encoding=result['encoding'])
    text_str = text.iloc[:, 0].str.cat(sep=' ')  # convert first column to string
    doc = nlp(text_str)
    html = displacy.render(doc, style="ent")
    return html

highlight_important_words('Eldar_Shlomi_-_CV.docx')