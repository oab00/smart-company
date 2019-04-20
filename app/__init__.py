from flask import Flask
#from config import Config
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

def create_app():
    app = Flask(__name__, static_url_path='/assets')

    with app.app_context():
        #app.config.from_object(Config)
        #db = SQLAlchemy(app)
        #migrate = Migrate(app, db)

        #from . import routes
        from . import mqtt_routes
    return app
