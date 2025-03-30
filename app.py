from flask import Flask
from .config import Config
from .routes import routes
from .models import db
from .auth import auth
from flask_migrate import Migrate
from .quiz import quiz_bp

def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)
 
	db.init_app(app)
	# use this only to notify changes in the db
	# Migrate(app, db)
	
	app.register_blueprint(routes)
	app.register_blueprint(auth)
	app.register_blueprint(quiz_bp)

	with app.app_context():
		# db.drop_all()
		db.create_all()

	return app


if __name__ == "__main__":
	app = create_app()
	app.run(debug=True)