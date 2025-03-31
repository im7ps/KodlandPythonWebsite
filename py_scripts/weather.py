import requests
from datetime import datetime
import os

def get_weather(city):
	API_KEY = "0c9d4006a5af8dcf2c7097fdb534f5ac"
	BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
	params = {
		"q": city,
		"appid": API_KEY,
		"units": "metric",
		"lang": "en"
	}
	try:
		response = requests.get(BASE_URL, params=params)
		response.raise_for_status()
		data = response.json()
		forecasts = []
		for i in range(0, 24, 8):
			forecast = data["list"][i]
			date_str = forecast['dt_txt']
			date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
			day_name = date_obj.strftime("%A")
			forecasts.append({
				"date": forecast["dt_txt"].split()[0] + ' - ' + day_name,
				"temp_max": forecast["main"]["temp_max"],
				"temp_min": forecast["main"]["temp_min"]
			})
		return forecasts
	except (requests.RequestException, KeyError, IndexError) as e:
		print(f"Error fetching weather's data: {e}")
		return []