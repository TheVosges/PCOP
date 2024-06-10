import os
import PyPDF2
from transformers import HerbertTokenizer
import json
import pandas as pd
from tqdm import tqdm
from transformers import RobertaModel
import datasets
import ast
from sklearn.preprocessing import MultiLabelBinarizer
import warnings
import numpy as np

warnings.filterwarnings("ignore")

# Config
script_dir = os.path.dirname(__file__)
dataset_folder = os.path.join(script_dir, "../../datasets/PCOP/data")
annotations_folder = os.path.join(script_dir, "../../datasets/PCOP")
output_folder = os.path.join(script_dir, "../../datasets/PCOP/top20")
output_csv = os.path.join(output_folder, "tokenized_data.csv")
extracted_texts = []
extracted_texts = []
labels_list = []
ids = []
annotations = {}
all_labels = ['ochrona przyrody', 'rolnictwo', 'pomoc finansowa', 'oświata i wychowanie', 'dokumenty', 'wynagrodzenia', 'opieka zdrowotna', 'podatki', 'ochrona zdrowia', 'ochrona środowiska', 'świadczenia lecznicze', 'inwestycje', 'umowy międzynarodowe', 'energetyka', 'kwalifikacje', 'szkolnictwo', 'rejestry', 'choroby zakaźne', 'kontrola', 'żołnierz zawodowy']
with open(annotations_folder + "/anns.json") as json_file:
    annotations = json.load(json_file)

mlb = MultiLabelBinarizer(classes=all_labels)
# tokenizer = HerbertTokenizer.from_pretrained("allegro/herbert-klej-cased-tokenizer-v1")

# Extract text from PDFs
def extract_text_from_pdf_and_label(pdf_path, annotations):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        labels = annotations.get(os.path.splitext(os.path.basename(pdf_path))[0])
        return text, ast.literal_eval(labels)


data = {"text": [], "labels": []}
file = 2
total_files = sum(1 for filename in os.listdir(dataset_folder) if filename.endswith(".pdf"))
for filename in tqdm(os.listdir(dataset_folder), total=total_files, desc="Processing PDFs"):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(dataset_folder, filename)
        labels = ast.literal_eval(annotations.get(os.path.splitext(os.path.basename(pdf_path))[0]))
        if labels and any(item in labels for item in all_labels):
            text, labels = extract_text_from_pdf_and_label(pdf_path, annotations)
            one_hot_encoding = mlb.fit_transform([labels])
            if np.any(one_hot_encoding == 1):
                extracted_texts.append(text)
                labels_list.append(one_hot_encoding)

data["text"] = extracted_texts
data["labels"] = labels_list

dataset = datasets.Dataset.from_dict(data)
dataset.save_to_disk(output_folder)