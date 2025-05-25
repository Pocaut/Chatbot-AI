from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Baixar modelo e tokenizer do BERTimbau
model_name = 'pierreguillou/bert-base-cased-pt-intent-classification'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

model.eval()

def predict_intent(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_id = torch.argmax(logits, dim=1).item()
    
    labels = [
        "agenda", "jogadores", "parceiros", "apoio", "estatisticas", "desconhecido"
    ]
    
    return labels[predicted_class_id]

respostas = {
    "agenda": "A equipe de CS da Furia estará participando dos eventos:\n\n🏆 PGL Astana 2025 - 10/05/25 à 18/05/25\n🏆 IEM Dallas 2025 - 19/05/25 à 25/05/25\n🏆 BLAST.tv Austin Major 2025 - 03/06/25 à 22/06/25",
    "jogadores": "Nossa equipe atual conta com os titulares Molodoy, Yekindar, FalleN, KSCERATO e yuurih. Nossos reservas são o skullz e chelo.",
    "parceiros": "Atualmente os parceiros da FURIA são a Adidas, Faculdade Cruzeiro do Sul Virtual, Lenovo, Pokerstars, Redbull e Hellmann's.",
    "apoio": "Para apoiar a nossa equipe, acompanhe os jogos, compartilhe nossos posts no Instagram e X, e vista nossa marca!\nVeja produtos em: https://www.furia.gg/",
    "estatisticas": "Temporada 2025\nEquipe Furia: 54 mapas jogados, 23 vitórias, 0 empates, 31 derrotas, 3888 kills, 3845 mortes, 1190 rounds jogados, K/D ratio 1.01\n\nFalleN: 54 mapas, 758 kills, 36.1% HS, 765 mortes, K/D 0.99\n...",
    "desconhecido": "Desculpe, não entendi sua pergunta. Pode tentar de outro jeito?"
}

def gerar_resposta(texto_usuario):
    intent = predict_intent(texto_usuario)
    return respostas.get(intent, respostas["desconhecido"])
