from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Processador de Textos - IO-BOUND</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .container {
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    max-width: 400px;
                    width: 100%;
                }
                h1 {
                    margin-top: 0;
                    color: #007BFF;
                }
                form {
                    display: flex;
                    flex-direction: column;
                }
                input[type="file"] {
                    margin-bottom: 10px;
                }
                input[type="submit"] {
                    background-color: #007BFF;
                    border: none;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                }
                input[type="submit"]:hover {
                    background-color: #0056b3;
                }
                .message {
                    margin-top: 10px;
                    font-size: 14px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Processador de Arquivos de Texto - Aplicação IO-BOUND [POI - Atividade 02]</h1>
                <p class="message">Selecione um arquivo de texto para calcular estatísticas como o número de palavras, linhas e caracteres.</p>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="file" required>
                    <input type="submit" value="Upload">
                </form>
            </div>
        </body>
        </html>
    ''')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template_string('''
            <!doctype html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Resultado do Upload</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        color: #333;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }
                    .container {
                        background: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        max-width: 400px;
                        width: 100%;
                        text-align: center;
                    }
                    h1 {
                        margin-top: 0;
                        color: #dc3545;
                    }
                    p {
                        font-size: 16px;
                        color: #dc3545;
                    }
                    a {
                        display: inline-block;
                        margin-top: 20px;
                        color: #007BFF;
                        text-decoration: none;
                        font-size: 16px;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Erro no Upload</h1>
                    <p>Não foi possível processar o arquivo. Por favor, tente novamente.</p>
                    <a href="/">Voltar</a>
                </div>
            </body>
            </html>
        '''), 400
    file = request.files['file']
    if file.filename == '':
        return render_template_string('''
            <!doctype html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Resultado do Upload</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        color: #333;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }
                    .container {
                        background: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        max-width: 400px;
                        width: 100%;
                        text-align: center;
                    }
                    h1 {
                        margin-top: 0;
                        color: #dc3545;
                    }
                    p {
                        font-size: 16px;
                        color: #dc3545;
                    }
                    a {
                        display: inline-block;
                        margin-top: 20px;
                        color: #007BFF;
                        text-decoration: none;
                        font-size: 16px;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Erro no Upload</h1>
                    <p>Nenhum arquivo selecionado. Por favor, selecione um arquivo e tente novamente.</p>
                    <a href="/">Voltar</a>
                </div>
            </body>
            </html>
        '''), 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        word_count, line_count, char_count = process_file(filepath)
        return render_template_string('''
            <!doctype html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Resultado do Upload</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        color: #333;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }
                    .container {
                        background: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        max-width: 400px;
                        width: 100%;
                        text-align: center;
                    }
                    h1 {
                        margin-top: 0;
                        color: #28a745;
                    }
                    p {
                        font-size: 16px;
                        color: #333;
                    }
                    a {
                        display: inline-block;
                        margin-top: 20px;
                        color: #007BFF;
                        text-decoration: none;
                        font-size: 16px;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Resultado do Upload</h1>
                    <p><strong>Nome do Arquivo:</strong> {{ filename }}</p>
                    <p><strong>Número de Palavras:</strong> {{ word_count }}</p>
                    <p><strong>Número de Linhas:</strong> {{ line_count }}</p>
                    <p><strong>Número de Caracteres:</strong> {{ char_count }}</p>
                    <a href="/">Voltar</a>
                </div>
            </body>
            </html>
        ''', filename=file.filename, word_count=word_count, line_count=line_count, char_count=char_count)

def process_file(filepath):
    with open(filepath, 'r') as file:
        text = file.read()
        word_count = len(text.split())
        line_count = text.count('\n')
        char_count = len(text)
    return word_count, line_count, char_count

if __name__ == '__main__':
    app.run(debug=True)
