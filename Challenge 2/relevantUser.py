import json
import time
import random
import os

try:

    caminho_json = r"CAMINHO_UPLOAD_TESSERACSCRIPT"

    with open(caminho_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    palavras_chave = ["furia", "cs2", "guerri", "kscerato", "yuurih", "fallen"]

    usuarios_relevantes = {}

    for palavra, mensagens in dados.items():
        for mensagem in mensagens:
            mensagem_lower = mensagem.lower()
            palavras_encontradas = []

            for palavra_busca in palavras_chave:
                if palavra_busca in mensagem_lower:
                    palavras_encontradas.append(palavra_busca)

            if palavras_encontradas:

                if "@" in mensagem:
                    inicio = mensagem.find("@") + 1
                    fim = mensagem.find(" ", inicio)
                    if fim == -1:
                        fim = len(mensagem)
                    usuario = mensagem[inicio:fim]
                else:
                    usuario = "desconhecido"

                if usuario not in usuarios_relevantes:
                    usuarios_relevantes[usuario] = {}

                for palavra_encontrada in palavras_encontradas:
                    if palavra_encontrada not in usuarios_relevantes[usuario]:
                        usuarios_relevantes[usuario][palavra_encontrada] = 0
                    usuarios_relevantes[usuario][palavra_encontrada] += 1

                print(f"Usuário @{usuario} é relevante! Palavras-chave: {palavras_encontradas}")

        tempo = random.uniform(2, 4)
        print(f"Aguardando {tempo:.2f} segundos...")
        time.sleep(tempo)

    saida_json = r"CAMINHO_OUTPUT"
    os.makedirs(os.path.dirname(saida_json), exist_ok=True)

    with open(saida_json, "w", encoding="utf-8") as f:
        json.dump(usuarios_relevantes, f, ensure_ascii=False, indent=4)

    print("\nProcesso concluído! Resultado salvo em usuarios_relevantes.json.")

except Exception as e:
    print(f"Ocorreu um erro: {e}")
