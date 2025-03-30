from flask import Blueprint, render_template, request, session

from .quiz import load_question
from .weather import get_weather
from .models import User, Score, db


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
    scores = db.session.query(Score, User).join(User, Score.user_id == User.id).order_by(Score.score.desc()).all()

    leaderboard_data = [
        {"rank": rank + 1, "nickname": user.nickname, "score": score.score}
        for rank, (score, user) in enumerate(scores)
    ]
    
    return render_template('leaderboard.html', leaderboard_data=leaderboard_data)



@routes.route('/quiz', methods=['GET', 'POST'])
def quiz():
	if 'question_count' not in session:
		session['question_count'] = 0

	if 'score' not in session:
		session['score'] = 0

	if 'question' not in session:
		session['question'], session['options'], session['correct_index'] = load_question()
		session['user_answer'] = None


	if request.method == 'POST' and 'answer' in request.form:
		user_answer = int(request.form.get('answer'))
		session['user_answer'] = user_answer
		
		if session['user_answer'] == session['correct_index']:

			username = session.get('user')
			user_entry = User.query.filter_by(username=username).first()
			if user_entry:
				score_entry = Score.query.filter_by(user_id=user_entry.id).first()
				if score_entry:
					score_entry.score += 1
					session['score'] = score_entry.score
					db.session.add(score_entry)
					db.session.commit()
					

		session['question_count'] += 1
		session['question'], session['options'], session['correct_index'] = load_question()

	return render_template(
		"quiz.html",
		question=session['question'],
		options=session['options'],
		correct_index=session['correct_index'],
		total_score=session['score'],
	)
