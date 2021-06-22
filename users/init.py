from users.modules import SQLAlchemy, BaseConfig, Flask

#create an app object for FLASK
app = Flask(__name__)

#fetch the config of the application
app.config.from_object(BaseConfig)

#create a db object for the application
db = SQLAlchemy(app)