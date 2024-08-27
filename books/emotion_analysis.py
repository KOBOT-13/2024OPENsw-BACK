from transformers import pipeline, BertForSequenceClassification, BertTokenizer
import os

def emotion_analysis(input_post):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    model_path = os.path.join(BASE_DIR, 'books/kobert_fine_tuning_weight')

    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)
    
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    
    text = [input_post]
    
    result = nlp(text)[0]
    
    label = result['label']
    score = result['score']
    
    if label == 'LABEL_0':
        score = 0 - score
    
    return score
