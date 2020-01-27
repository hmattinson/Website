import os
import json
import socket

# Server
if socket.gethostname() == 'ubuntu-instance':
    with open('/etc/config.json') as config_file:
        config=json.load(config_file)

class Config:
    # Server
    if socket.gethostname() == 'ubuntu-instance':
        SECRET_KEY = config.get("FLASK_BLOG_SECRET_KEY")
        SQLALCHEMY_DATABASE_URI = config.get("FLASK_BLOG_SQLALCHEMY_DATABASE_URI")

    # Local
    else:
        SECRET_KEY = os.environ.get("FLASK_BLOG_SECRET_KEY")
        SQLALCHEMY_DATABASE_URI = os.environ.get("FLASK_BLOG_SQLALCHEMY_DATABASE_URI")

    # MAIL_SERVER = os.environ.get("FLASK_BLOG_MAIL_SERVER")
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get("FLASK_BLOG_MAIL_USERNAME")
    # MAIL_PASSWORD = os.environ.get("FLASK_BLOG_MAIL_PASSWORD")
