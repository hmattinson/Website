import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from website import mail
import re

ip_addr_regex = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
website_substitute = 'mattinson.nl'

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    # resize
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn

def send_request_email(user):
    token = user.username
    msg = Message('Account Request',
                  sender='noreply@mattinson.nl',
                  recipients=["henrymattinson@westfieldhouse.org"])
    ip_url = url_for('users.add_user', token=token, _external=True)
    url = re.sub(ip_addr_regex, website_substitute, ip_url)
    msg.body = f'''Account requested for {user.username}, email: {user.email}.
    Authenticate: {url}
'''
    mail.send(msg)

def send_set_email(user):
    token = user.get_reset_token()
    msg = Message('Set Password',
                  sender='noreply@mattinson.nl',
                  recipients=[user.email])
    ip_url = url_for('users.reset_token', token=token, _external=True)
    url = re.sub(ip_addr_regex, website_substitute, ip_url)
    msg.body = f'''To set your password, visit the following link:{url}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
