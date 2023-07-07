import PyPDF2
import docx2txt
import csv

import highlight
import visualization


def process_file(filename):
    parse_to_csv(filename)
    # highlight.highlight_important_words(filename)
    # visualization.create_visualization(filename)

def parse_to_csv(filename):
    if filename.endswith('.pdf'):
        pdf_file_obj = open('uploads/' + filename, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
        num_pages = pdf_reader.numPages
        all_text = ''
        for page in range(num_pages):
            page_obj = pdf_reader.getPage(page)
            all_text += page_obj.extract_text()
        pdf_file_obj.close()
    elif filename.endswith('.docx'):
        all_text = docx2txt.process('uploads/' + filename)

    with open('uploads/' + filename + '.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(all_text.split())