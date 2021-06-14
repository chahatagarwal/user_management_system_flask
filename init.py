from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig

app = Flask(__name__)

#fetch the config of the application
app.config.from_object(BaseConfig)
#create a db object for the application
db = SQLAlchemy(app)