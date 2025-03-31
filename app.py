from flask import Flask
from py_scripts.config import Config
from py_scripts.routes import routes
from py_scripts.models import db
from py_scripts.auth import auth
from flask_migrate import Migrate
from py_scripts.quiz import quiz_bp
from dotenv import load_dotenv
import os


app = Flask(__name__)
def create_app():
	app.config.from_object(Config)
 
	db.init_app(app)
	# use this only to notify changes in the db
	# Migrate(app, db)
	
	app.register_blueprint(routes)
	app.register_blueprint(auth)
	app.register_blueprint(quiz_bp)

	with app.app_context():
		# use this only if you want to recrete the db for every run
		# db.drop_all()
		db.create_all()

	return app


if __name__ == "__main__":
	dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
	load_dotenv(dotenv_path)
	app = create_app()
	app.run(debug=True)