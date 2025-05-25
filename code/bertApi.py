from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from fastapi import FastAPI
from pydantic import BaseModel

model_path = "C:/projetoFuria/app/appchatbotclube/bert/bertimbau_furia_intent"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
id2label = model.config.id2label

app = FastAPI()

class Item(BaseModel):
    text: str

@app.post("/predict_intent")
def predict_intent(item: Item):
    inputs = tokenizer(item.text, return_tensors="pt", truncation=True, padding=True, max_length=64)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_id = torch.argmax(logits, dim=1).item()
    intent_label = id2label[predicted_id]
    return {"intent": intent_label}
