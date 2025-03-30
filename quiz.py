import json
from flask import Blueprint
import random


def load_question():
	"""Carica le domande dal file JSON."""
	with open("quiz.json", "r", encoding="utf-8") as file:
		data = json.load(file)
		questions = []
		for category in data["quiz"]:
			questions.extend(category["questions"])
		question_data = random.choice(questions)
		question = question_data['question']
		options = question_data['options']
		correct_index = question_data['correct_index']

		# print(correct_index)
		correct_option = options[correct_index]
		# print(correct_option)

		random.shuffle(options)

  
		options_data = []
		for index, option in enumerate(options):
			options_data.append({
				'text': option,
    			'index': index
			})
			if correct_option == option:
				correct_index = index
    
		# print(options[correct_index])

		return question, options_data, correct_index

quiz_bp = Blueprint("quiz", __name__)
