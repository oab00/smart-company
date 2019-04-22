from flask import Flask
#from config import Config
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

def create_app():
    app = Flask(__name__, static_url_path='/assets')
    #static_url_path='/assets'
    #static_folder='assets'
    #return send_from_directory(app.static_folder, "403.html")

    with app.app_context():
        #app.config.from_object(Config)
        #db = SQLAlchemy(app)
        #migrate = Migrate(app, db)

        from . import routes
        from . import mqtt_routes
    return app
