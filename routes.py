from flask import Blueprint, render_template, request, session, redirect, url_for

from .quiz import load_question
from .weather import get_weather
from .models import User, Quiz, Score, db


routes = Blueprint('routes', __name__)

@routes.route("/", methods=["GET", "POST"])
def home():
	forecasts = None
	city = None
	if request.method == "POST":
		city = request.form["city"]
		forecasts = get_weather(city)
		
	return render_template("home.html", forecasts=forecasts, city=city)


@routes.route('/registration')
def registration():
	return render_template('registration.html')


@routes.route('/login')
def login():
	return render_template('login.html')


@routes.route('/leaderboard')
def leaderboard():
    # Recupera i punteggi ordinati dal più alto al più basso
    scores = db.session.query(Score, User).join(User, Score.user_id == User.id).order_by(Score.score.desc()).all()
    
    # Prepara i dati con il rank
    leaderboard_data = [
        {"rank": rank + 1, "nickname": user.nickname, "score": score.score}
        for rank, (score, user) in enumerate(scores)
    ]
    
    return render_template('leaderboard.html', leaderboard_data=leaderboard_data)



@routes.route('/quiz', methods=['GET', 'POST'])
def quiz():
	# if 'final_score' not in session:
	# 	session['final_score'] = None
	if 'question_count' not in session:
		session['question_count'] = 0
		# session['final_score'] = None
	if 'score' not in session:
		session['score'] = 0


	# if session['question_count'] == 0:
	# 	session['final_score'] = None

	# Se l'utente ha cliccato la freccia 3 volte, lo mandiamo alla login
	# if session['question_count'] > 2:
	# 	session.pop('question_count')
	# 	session['final_score'] = session['score']
	# 	session.pop('score')
	# 	return render_template(
	# 		"quiz.html",
	# 		question=session['question'],
	# 		options=session['options'],
	# 		correct_index=session['correct_index'],
	# 		final_score=session['final_score'],
	# 	)


	if 'question' not in session:
		session['question'], session['options'], session['correct_index'] = load_question()
		session['user_answer'] = None


	if request.method == 'POST' and 'answer' in request.form:
		user_answer = int(request.form.get('answer'))
		session['user_answer'] = user_answer
		
		if session['user_answer'] == session['correct_index']:

			username = session.get('user')
			# print(f"Username: {username}")
			user_entry = User.query.filter_by(username=username).first()
			# print(f"User entry: {user_entry}")
			if user_entry:
				score_entry = Score.query.filter_by(user_id=user_entry.id).first()
				# print(f"Score entry: {score_entry}")
				if score_entry:
					# print(f"Current score entry: {score_entry}")
					score_entry.score += 1
					session['score'] = score_entry.score
					# print(f"Current score: {score_entry.score}")
					db.session.add(score_entry)
					db.session.commit()
					
				# print(username)

		session['question_count'] += 1
		session['question'], session['options'], session['correct_index'] = load_question()
	
	# print(f"Question_count: {session['question_count']}")
	# print(f"Final: {session['final_score']}")

	return render_template(
		"quiz.html",
		question=session['question'],
		options=session['options'],
		correct_index=session['correct_index'],
		total_score=session['score'],
	)
