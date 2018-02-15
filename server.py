from flask import Flask, request, jsonify
import json
import requests
import os
from datetime import timedelta, datetime

app = Flask(__name__)
port = int(os.environ["PORT"])

@app.route('/today_pomos', methods=['POST'])
def index():
    data = json.loads(request.get_data())
    date = datetime.strptime(data["nlp"]["entities"]["datetime"]["iso"], "%Y-%m-%dT%H:%M:%S+00:00")
    date -= timedelta(hours=5)
    end = datetime(date.year, date.month, date.day) + timedelta(days=1)
    diff = end - date
    q, r = divmod(diff, timedelta(minutes=25))
    pomos = q
    if r > timedelta(0): pomos += 1
    return jsonify(
        status=200,

        replies=[{
            'type' : 'text',
            'content' : 'Puedes hacer {} pomos'.format(pomos)
        }]
    )

@app.route('/errors', methods=['POST'])
def errors():
  print(json.loads(request.get_data()))
  return jsonify(status=200)

app.run(port=port, host="0.0.0.0")