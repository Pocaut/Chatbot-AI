import tweepy
import time
import json
import os

# BEARER TOKEN REFERENTE À API DO TWITTER
bearer_token = "SEU_BEARER_TOKEN"

client = tweepy.Client(bearer_token=bearer_token)

def buscar_tweets(query, max_tentativas=5):
    tentativas = 0
    while tentativas < max_tentativas:
        try:
            print(f"Buscando tweets para: '{query}' (tentativa {tentativas+1})")
            response = client.search_recent_tweets(query=query, max_results=10)

            if response.data:
                return [tweet.text for tweet in response.data]
            else:
                return []

        except tweepy.errors.TooManyRequests:
            print("429 recebido. Aguardando 60 segundos...")
            time.sleep(60)
            tentativas += 1

        except Exception as e:
            print(f"Erro inesperado: {e}")
            break

    return []

def salvar_json(dados, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    print(f"Dados salvos em {caminho}")

if __name__ == "__main__":
    termos = ["FURIA", "FURIA CS2", "Guerri", "KSCERATO", "yuurih", "FalleN"] 

    todos_tweets = {}

    for termo in termos:
        tweets = buscar_tweets(termo)
        todos_tweets[termo] = tweets
        time.sleep(2)

    os.makedirs("SEU_CAMINHO_DESEJADO", exist_ok=True)

    salvar_json(todos_tweets, "SEU_CAMINHO_DESEJADO\\NOME_ARQUIVO.JSON")

    input("\nPressione Enter para sair...")
