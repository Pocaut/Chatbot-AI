from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
import pytesseract
from PIL import Image
import shutil
import os
import json
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r"CAMINHO_DO_TESSERACT.EXE"

UPLOAD_FOLDER = r"SEU_CAMINHO_DESEJADO_UPLOAD"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def main():
    return """
    <html>
    <head><title>Upload</title></head>
    <body style="background-color:black; color:white; text-align:center; font-family:Times New Roman;">
        <h1>Clube de Fãs Oficial da FURIA</h1>
        <form action="/documento/" enctype="multipart/form-data" method="post">
            <input name="nome" placeholder="Nome"><br>
            <input name="cpf" placeholder="CPF"><br>
            <input name="endereco" placeholder="Endereço"><br>
            <input name="email" placeholder="Email"><br>
            <input name="interesses" placeholder="Interesses"><br>
            <input name="atividades" placeholder="Atividades"><br>
            <input name="compras" placeholder="Compras"><br>
            <input name="link" placeholder="Link de perfil"><br>
            <input type="file" name="file"><br><br>
            <input type="submit" value="Enviar">
        </form>
    </body>
    </html>
    """

@app.post("/documento/", response_class=HTMLResponse)
async def upload_documento(
    nome: str = Form(...),
    cpf: str = Form(...),
    endereco: str = Form(...),
    email: str = Form(...),
    interesses: str = Form(None),
    atividades: str = Form(None),
    compras: str = Form(None),
    link: str = Form(None),
    file: UploadFile = File(...)
):

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{nome.replace(' ', '_')}_{timestamp}.{file.filename.split('.')[-1]}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    img = Image.open(file_path)
    texto_extraido = pytesseract.image_to_string(img)

    data = {
        "nome": nome,
        "cpf": cpf,
        "endereco": endereco,
        "email": email,
        "interesses": interesses,
        "atividades": atividades,
        "compras": compras,
        "link": link,
        "texto_extraido_do_documento": texto_extraido.strip(),
        "arquivo_salvo": filename
    }

    json_filename = f"{nome.replace(' ', '_')}_{timestamp}.json"
    json_path = os.path.join(UPLOAD_FOLDER, json_filename)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return """
    <html>
    <head><title>Cadastro Confirmado</title></head>
    <body style="background-color:black; color:white; text-align:center; font-family:Times New Roman;">
        <img src="https://furiagg.fbitsstatic.net/sf/img/logo-furia.svg?theme=main&v=202503171541" alt="FURIA Logo" style="margin-top:20px; width:200px;"/>
        <h1 style="margin-top:20px;">Cadastro Confirmado!</h1>
        <p>Seja bem-vindo ao Clube de Fãs da FURIA!</p>
        <p>Em breve você receberá novidades e benefícios exclusivos.</p>
        <a href="/" style="display:inline-block; margin-top:20px; padding:10px 20px; background:white; color:black; text-decoration:none; font-weight:bold; border-radius:6px;">Voltar para a página inicial</a>
    </body>
    </html>
    """
