import os
from PIL import Image
import stepic
import shutil
from flask import Blueprint, current_app, render_template, url_for, redirect, request, session, flash
from datetime import timedelta
# from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename

# This line creates a Flask Blueprint object called text. It specifies the name of the Blueprint as "text" and the location of the static and template folders.

text = Blueprint("text", __name__, static_folder="static",
                 template_folder="templates")



# This code creates a Flask route decorator that maps the URL "/encode" to the function text_encode(). When a user navigates to this URL, it will return the rendered HTML template "encode-text.html".

@text.route("/encode")
def text_encode():
    return render_template("encode-text.html")

# This function handles a POST or GET request from a user submitting the form on the "encode-text.html" page. The function first checks if a file was uploaded and whether a message was entered. If both conditions are satisfied, the function saves the uploaded file to the designated folder and calls the encrypt_text() function to encode the message into the image. It then returns the rendered HTML template "encode-text-result.html", which displays the original image, the encrypted image, and the message.

@text.route("/encode-result", methods=['POST', 'GET'])
def text_encode_result():
    if request.method == 'POST':
        message = request.form['message']
        if 'file' not in request.files:
            flash('No image found')
        file = request.files['image']

        if file.filename == '':
            flash('No image selected')

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                current_app.config['UPLOAD_TEXT_FOLDER'], filename))
            text_encryption = True
            encrypt_text(os.path.join(
                current_app.config['UPLOAD_TEXT_FOLDER'], filename), message)
        else:
            text_encryption = False
        result = request.form

        return render_template("encode-text-result.html", result=result, file=file, text_encryption=text_encryption, message=message)





@text.route("/decode")
def text_decode():
    return render_template("decode-text.html")


@text.route("/decode-result", methods=['POST', 'GET'])
def text_decode_result():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No image found')
        file = request.files['image']
        if file.filename == '':
            flash('No image selected')
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                current_app.config['UPLOAD_TEXT_FOLDER'], filename))
            text_decryption = True
            message = decrypt_text(os.path.join(
                current_app.config['UPLOAD_TEXT_FOLDER'], filename))
        else:
            text_decryption = False
        result = request.form
        return render_template("decode-text-result.html", result=result, file=file, text_decryption=text_decryption, message=message)

# Encryption function


def encrypt_text(image_1, message):
    im = Image.open(image_1)

    im1 = stepic.encode(im, bytes(str(message), encoding='utf-8'))
    im1.save(os.path.join(
        current_app.config['UPLOAD_TEXT_FOLDER'], "encrypted_text_image.png"))

# Decryption function


def decrypt_text(image_1):
    im2 = Image.open(image_1)
    stegoImage = stepic.decode(im2)
    return stegoImage
