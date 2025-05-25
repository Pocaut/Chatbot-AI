import requests

frases = [
    "Quais são os jogadores da FURIA CS?",
    "Quando a Furia vai jogar?",
    "A Furia tem loja oficial?",
    "Como está o KD da equipe?",
    "Quem são os parceiros da Furia?"
]

for frase in frases:
    res = requests.post("http://127.0.0.1:8000/predict_intent", json={"text": frase})
    print(f"\nFrase: {frase}")
    print(f"Resposta: {res.json()}")
