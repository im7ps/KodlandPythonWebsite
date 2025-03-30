import requests

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
		response.raise_for_status()  # Solleva un'eccezione per errori HTTP
		data = response.json()
		forecasts = []
		for i in range(0, 40, 8):  # Prende le previsioni ogni 24 ore
			forecast = data["list"][i]
			forecasts.append({
				"date": forecast["dt_txt"].split()[0],  # Prende solo la data
				"temp_max": forecast["main"]["temp_max"],
				"temp_min": forecast["main"]["temp_min"]
			})
		return forecasts
	except (requests.RequestException, KeyError, IndexError) as e:
		print(f"Error fetching weather's data: {e}")
		return []  # Restituisce una lista vuota in caso di errore