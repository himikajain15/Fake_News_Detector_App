import pickle
from transformers import pipeline

# Load pre-trained BERT model
bert_classifier = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Save model
with open("bert_model.pkl", "wb") as f:
    pickle.dump(bert_classifier, f)

print("BERT model saved successfully!")
