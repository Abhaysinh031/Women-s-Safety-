import pywhatkit as kit
import pyautogui as pg
from datetime import datetime, timedelta
import requests
import json
import pywhatkit as kit
from flask import Flask, render_template
THING_SPEAK_URL = "https://api.thingspeak.com/channels/2505252/feeds.json?api_key=9OOWPUGXMW56G6TB&results=1"

def index():
    data = fetch_data()
    return render_template('index.html', data=data)

def fetch_data():
    response = requests.get(THING_SPEAK_URL)
    if response.status_code == 200:
        data = response.json()
        return data['feeds'][0] if 'feeds' in data else None
    return None

def send_whatsapp(numbers, name, data, link):
    message_emergency = f"""🚨🛑 *Emergency* 🛑🚨
{name} is in emergency and need your help immediately.
Click the link below for location
{link}"""
    message_data = f"{name} Health Status :\nOxygen: {data.get('field1')}\nPulse Rate: {data.get('field2')}\nTemperature: {data.get('field3')}"
    message = f"{message_emergency}\n\n{message_data}"
    time = str(datetime.now() + timedelta(seconds=90))
    hour, minute = time[11:13], time[14:16]
    if hour[0] == "0":
        hour = hour[1]
    if minute[0] == "0":
        minute = minute[1]
    hour, minute = int(hour), int(minute)
    for x in range(len(numbers)):
        kit.sendwhatmsg(numbers[x], message, hour, minute + int(x), wait_time=2)
        pg.press("enter")
