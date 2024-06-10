import os
import PyPDF2
from transformers import AutoTokenizer
import json
import pandas as pd
from tqdm import tqdm


# tokenizer = AutoTokenizer.from_pretrained("allegro/herbert-klej-cased-tokenizer-v1")

# Extract text from PDFs
def extract_text_from_pdf_and_save(pdf_path, output_csv, annotations):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        label = annotations.get(os.path.splitext(os.path.basename(pdf_path))[0])
        data = {"id": os.path.splitext(os.path.basename(pdf_path))[0], "tokens": tokenizer.tokenize(text), "label": label}
        df = pd.DataFrame(data, index=[0])
        if os.path.exists(output_csv):
            df.to_csv(output_csv, mode='a', header=False, index=False, sep=';')
        else:
            df.to_csv(output_csv, index=False, sep=';')

script_dir = os.path.dirname(__file__)
dataset_folder = os.path.join(script_dir, "../../datasets/PCOP/data")
annotations_folder = os.path.join(script_dir, "../../datasets/PCOP")
output_folder = os.path.join(script_dir, "../../datasets/PCOP")
output_csv = os.path.join(output_folder, "tokenized_data.csv")
extracted_texts = []
labels = []
ids = []
annotations = {}
with open(annotations_folder + "/anns.json") as json_file:
    annotations = json.load(json_file)


files = 1
# Count total number of PDF files
total_files = sum(1 for filename in os.listdir(dataset_folder) if filename.endswith(".pdf"))
for filename in tqdm(os.listdir(dataset_folder), total=total_files, desc="Processing PDFs"):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(dataset_folder, filename)
        extract_text_from_pdf_and_save(pdf_path, output_csv, annotations)

# Tokenization using BERT tokenizer

#
# # Tokenize each text
# tokenized_texts = [tokenizer.tokenize(text) for text in extracted_texts]

# Print tokenized text of the first document
# print(extracted_texts)