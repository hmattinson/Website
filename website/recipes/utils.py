import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from website import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/recipe_pics', picture_fn)

    i = Image.open(form_picture)
    i.save(picture_path)
    return picture_fn
