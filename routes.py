from flask import Blueprint, render_template, request, session, redirect, url_for

from .quiz import load_question
from .models import User, Quiz, Score


routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
	return render_template('home.html')

@routes.route('/registration')
def registration():
	return render_template('registration.html')

@routes.route('/login')
def login():
	return render_template('login.html')

@routes.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'question_count' not in session:
        session['question_count'] = 0

    # Se l'utente ha cliccato la freccia 3 volte, lo mandiamo alla login
    if session['question_count'] >= 3:
        session.pop('question_count')
        return render_template('login.html')  # 🔥 Usiamo redirect per cambiare pagina

    # Se è la prima volta che l'utente arriva qui, carichiamo una domanda
    if 'question' not in session:
        session['question'], session['options'], session['correct_index'] = load_question()
        session['user_answer'] = None

    # Se l'utente ha cliccato "➡️" (next_question=1)
    if request.method == 'POST' and 'next_question' in request.form:
        session['question'], session['options'], session['correct_index'] = load_question()
        session['user_answer'] = None
        session['question_count'] += 1  # Incrementiamo il contatore delle domande

    # Se l'utente ha risposto a una domanda
    if request.method == 'POST' and 'answer' in request.form:
        user_answer = int(request.form.get('answer'))
        session['user_answer'] = user_answer

    return render_template(
        "quiz.html",
        question=session['question'],
        options=session['options'],
        correct_index=session['correct_index'],
        user_answer=session['user_answer']
    )


@routes.route('/leaderboard')
def leaderboard():
	return render_template('leaderboard.html')
