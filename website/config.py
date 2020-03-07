import os
import json
import socket
import base64

# Server
if socket.gethostname() == 'ubuntu-instance':
    with open('/etc/config.json') as config_file:
        config=json.load(config_file)

class Config:
    # Server
    if socket.gethostname() == 'ubuntu-instance':
        SECRET_KEY = config.get("FLASK_BLOG_SECRET_KEY")
        SQLALCHEMY_DATABASE_URI = config.get("FLASK_BLOG_SQLALCHEMY_DATABASE_URI")
        MAIL_SERVER = config.get("FLASK_BLOG_MAIL_SERVER")
        MAIL_PORT = 587
        MAIL_USE_TLS = True
        MAIL_USERNAME = config.get("FLASK_BLOG_MAIL_USERNAME")
        pw = config.get("FLASK_BLOG_MAIL_PASSWORD")
        MAIL_PASSWORD = base64.b64decode(pw).decode("utf-8")

    # Local
    else:
        SECRET_KEY = os.environ.get("FLASK_BLOG_SECRET_KEY")
        SQLALCHEMY_DATABASE_URI = os.environ.get("FLASK_BLOG_SQLALCHEMY_DATABASE_URI")
        MAIL_SERVER = os.environ.get("FLASK_BLOG_MAIL_SERVER")
        MAIL_PORT = 587
        MAIL_USE_TLS = True
        MAIL_USERNAME = os.environ.get("FLASK_BLOG_MAIL_USERNAME")
        pw = os.environ.get("FLASK_BLOG_MAIL_PASSWORD")
        MAIL_PASSWORD = base64.b64decode(pw).decode("utf-8")
