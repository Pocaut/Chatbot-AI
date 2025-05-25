# Challenge-Furia

O projeto abaixo foi realizado como desafio para uma vaga de Assistente de Software. O primeiro desafio foi a elaboração de um Chatbot, no qual treinei um modelo de IA para identificar palavras chave e responder o usuário, e o segundo foi uma solução para captar informações dos fãs da FURIA através de redes sociais.

Os arquivos com modelo de IA treinado e a interface do chatbot feita em Flutter/Dart foram enviados direto para a FURIA e não estão disponíveis aqui devido ao tamanho dos arquivos.
Abaixo seguem as instruçoes de como usar o projeto.

Segue abaixo instruções para teste dos projetos elaborados para o Desafio. Optei por não compilar o aplicativo para que vocês tenham acesso ao codigo fonte e ajustem de acordo.
----

Requisitos e Instalações
1. Ambiente de Desenvolvimento

    VSCode com as extensões:

        Flutter (Dart code support)

        Python

    Android Studio (necessário para o emulador e SDKs Android)

    Git (opcional para clonar o repositório)

2. Flutter

    Instale o SDK do Flutter:
      https://docs.flutter.dev/get-started/install

    Verifique a instalação no VSCode executando no terminal: flutter doctor (Quando todos os campos do doctor estiverem verdes o programa deverá rodar normalmente)

3. Python e Bibliotecas

    Python 3.12+ (Pessoalmente tenho o 3.13 instalado)

Instalar bibliotecas no CMD:

pip install fastapi uvicorn transformers torch pytesseract pillow tweepy

4. Tesseract OCR

    Instale o Tesseract:

        Windows: https://github.com/tesseract-ocr/tesseract/wiki#windows

        Linux: sudo apt install tesseract-ocr

    Após instalar, adicione o caminho do executável ao código:
     " pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' "

▶ Execução do Projeto
1. Rodar a API BERT

Navegue até a pasta do projeto no CMD e execute:
  "uvicorn bertApi:app --reload --port 8000"

2. Rodar a API OCR (Tesseract)

Em outro terminal:
  "uvicorn tesseractScript:app --reload --port 8001"

3. Abrir o App Flutter

  Com a pasta do projeto aberta no VSCode, execute no terminal "flutter run", e selecione a opção 1 quando pedida pelo terminal.

Integração API no Flutter

Garanta que o código Dart esteja com os endpoints corretos, fiz questão de encasular as APIs em um Try para caso elas exibissem erros.

final response = await http.post(
  Uri.parse('http://localhost:8000/predict_intent'), // BERT API
);

final response = await http.post(
  Uri.parse('http://localhost:8001/ocr'), // Tesseract API
);

Observações Finais

    As APIs não podem usar a mesma porta. Use --port ao subir com uvicorn.
    
