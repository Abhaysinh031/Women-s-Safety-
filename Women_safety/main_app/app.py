from flask import Flask, render_template
import requests
import json
import time

app = Flask(__name__)

THING_SPEAK_URL = "https://api.thingspeak.com/channels/2505252/feeds.json?api_key=9OOWPUGXMW56G6TB&results=1"

@app.route('/')
def index():
    data = fetch_data()
    return render_template('index.html', data=data)

def fetch_data():
    response = requests.get(THING_SPEAK_URL)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data['feeds'][0] if 'feeds' in data else None
    return None

if __name__ == '__main__':
    app.run(debug=True)

