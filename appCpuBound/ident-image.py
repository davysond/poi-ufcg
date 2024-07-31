from flask import Flask, request, jsonify, render_template_string
import os
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# MobileNetV2 
model = tf.keras.applications.MobileNetV2(weights='imagenet')

@app.route('/')
def index():
    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Identificação de Imagens - CPU-BOUND</title>
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
                <h1>Identificação de Imagens - Aplicação CPU-BOUND</h1>
                <p class="message">Selecione uma imagem para identificação usando um modelo pré-treinado.</p>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="file" accept="image/*" required>
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
        predictions = process_image(filepath)
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
                    <h1>Resultado da Identificação</h1>
                    <p><strong>Nome do Arquivo:</strong> {{ filename }}</p>
                    <p><strong>Classificação:</strong> {{ predictions }}</p>
                    <a href="/">Voltar</a>
                </div>
            </body>
            </html>
        ''', filename=file.filename, predictions=predictions)

def process_image(filepath):
    # Imagem
    img = Image.open(filepath).convert('RGB').resize((224, 224))
    img_array = np.array(img)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    # Previsão
    predictions = model.predict(img_array)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions)
    top_prediction = decoded_predictions[0][0]

    class_name = top_prediction[1]
    class_prob = top_prediction[2]
    
    return f'{class_name} ({class_prob:.2f})'

if __name__ == '__main__':
    app.run(debug=True)
