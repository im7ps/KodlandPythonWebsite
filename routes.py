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
	if 'final_score' not in session:
		session['final_score'] = None
	if 'question_count' not in session:
		session['question_count'] = 0
		session['final_score'] = None
	if 'score' not in session:
		session['score'] = 0


	if session['question_count'] == 0:
		session['final_score'] = None

	# Se l'utente ha cliccato la freccia 3 volte, lo mandiamo alla login
	if session['question_count'] >= 3:
		session.pop('question_count')
		print(f"Score: {session['score']}")
		session['final_score'] = session['score']
		# session['score'] = 0
		session.pop('score')
		return render_template(
			"quiz.html",
			question=session['question'],
			options=session['options'],
			correct_index=session['correct_index'],
			final_score=session['final_score'],
		)


	if 'question' not in session:
		session['question'], session['options'], session['correct_index'] = load_question()
		session['user_answer'] = None

	# Se è la prima volta che l'utente arriva qui, carichiamo una domanda

	# Se l'utente ha cliccato "➡️" (next_question=1)
	# if request.method == 'POST' and 'next_question' in request.form:
	# 	session['question'], session['options'], session['correct_index'] = load_question()
	# 	session['user_answer'] = None
	# 	session['question_count'] += 1  # Incrementiamo il contatore delle domande

	# Se l'utente ha risposto a una domanda
	if request.method == 'POST' and 'answer' in request.form:
		user_answer = int(request.form.get('answer'))
		session['user_answer'] = user_answer
		
		if session['user_answer'] == session['correct_index']:
			session['score'] += 1

		session['question_count'] += 1
		session['question'], session['options'], session['correct_index'] = load_question()
	
	print(f"Question_count: {session['question_count']}")
	print(f"Final: {session['final_score']}")

	return render_template(
		"quiz.html",
		question=session['question'],
		options=session['options'],
		correct_index=session['correct_index'],
		final_score=session['final_score'],
	)


@routes.route('/leaderboard')
def leaderboard():
	return render_template('leaderboard.html')
