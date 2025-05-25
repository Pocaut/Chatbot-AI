import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset

# Carregando dados
df = pd.read_csv("chatbot_intencoes_furia.csv")
labels = sorted(df['intent'].unique())
label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for label, i in label2id.items()}
df['label'] = df['intent'].map(label2id)

# Tokenização
tokenizer = BertTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")

class IntentDataset(Dataset):
    def __init__(self, texts, labels):
        self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=64)
        self.labels = labels

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()} | {'labels': torch.tensor(self.labels[idx])}

    def __len__(self):
        return len(self.labels)

train_texts, val_texts, train_labels, val_labels = train_test_split(df["text"], df["label"], test_size=0.1)

train_dataset = IntentDataset(train_texts.tolist(), train_labels.tolist())
val_dataset = IntentDataset(val_texts.tolist(), val_labels.tolist())

# Modelo
model = BertForSequenceClassification.from_pretrained(
    "neuralmind/bert-base-portuguese-cased",
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id
)

# Treinamento
training_args = TrainingArguments(
    output_dir="./bertimbau_furia_intent",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    save_strategy="epoch"
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

trainer.train()
trainer.save_model("./bertimbau_furia_intent")
tokenizer.save_pretrained("./bertimbau_furia_intent")
