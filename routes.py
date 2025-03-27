from flask import Blueprint, render_template
from .models import User, Quiz, Score

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('home.html')

@routes.route('/register')
def register():
    return render_template('register.html')

@routes.route('/login')
def login():
    return render_template('login.html')

@routes.route('/quiz')
def quiz():
    return render_template('quiz.html')

@routes.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')
