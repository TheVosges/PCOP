from flask import Flask, request, jsonify
import torch
from transformers import GPT2Tokenizer, GPT2ForSequenceClassification
from PyPDF2 import PdfReader

app = Flask(__name__)

model_path = 'F:/PRACA MAGISTERSKA/analysis/PCOP/results-gpt2-polish/checkpoint-4000'
model = GPT2ForSequenceClassification.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained(model_path)

labels = ['ochrona przyrody', 'rolnictwo', 'pomoc finansowa', 'oświata i wychowanie', 'dokumenty', 'wynagrodzenia', 'opieka zdrowotna', 'podatki', 'ochrona zdrowia', 'ochrona środowiska', 'świadczenia lecznicze', 'inwestycje', 'umowy międzynarodowe', 'energetyka', 'kwalifikacje', 'szkolnictwo', 'rejestry', 'choroby zakaźne', 'kontrola', 'żołnierz zawodowy']

def pdf_to_text(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def classify_text(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(outputs.logits).squeeze().cpu().numpy()
    predictions = [labels[i] for i, prob in enumerate(probs) if prob > 0.5]  # Using 0.5 as threshold for multilabel classification
    return predictions

@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        text = pdf_to_text(file)
        categories = classify_text(text)
        return jsonify({'categories': categories}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)