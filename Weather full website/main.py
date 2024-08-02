# app.py
from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

API_KEY = "7ec6618d70c886276336cf47b9157e88"


@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None
    if request.method == 'POST':
        city = request.form['city']
        weather_data, error = get_weather(city)
    return render_template('index.html', weather_data=weather_data, error=error)


def get_weather(city):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        return process_weather_data(data), None
    else:
        return None, "City not found!"


def process_weather_data(data):
    city_name = data['name']
    temperature = data['main']['temp']
    feels_like = data['main']['feels_like']
    weather_description = data['weather'][0]['description']
    humidity = data['main']['humidity']

    time_zone = data['timezone']
    timezone_offset = timedelta(seconds=time_zone)
    utc_now = datetime.now(timezone.utc)
    local_time = utc_now + timezone_offset
    date = local_time.strftime('%Y-%m-%d')
    time = local_time.strftime('%H:%M:%S')

    return {
        'city': city_name,
        'temperature': temperature,
        'feels_like': feels_like,
        'description': weather_description.capitalize(),
        'humidity': humidity,
        'time': time,
        'date': date
    }


if __name__ == '__main__':
    app.run(debug=True)