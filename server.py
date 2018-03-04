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
    date = datetime.strptime(data["nlp"]["entities"]["datetime"][0]["iso"], "%Y-%m-%dT%H:%M:%S+00:00")
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

@app.route('/pomos_conversion', methods=['POST'])
def pomos_conversion():
    data = json.loads(request.get_data())
    unit_to = data["nlp"]["entities"]["unit-time"][0]["value"]

    value = data["nlp"]["entities"]["duration2"][0]["value"].split()
    value_v = value[0]
    try:
        temp = int(value_v)
        value_v = temp
    except ValueError:
        other_quantities = {"un" : 1}
        value_v = other_quantities[value_v]

    value_unit = value[1]
    units = {"horas" : 60, "hora" : 60, "minuto" : 1, "minutos" : 1}
    multiplier = units[value_unit]

    ans = 0
    if unit_to in ["pomos", "pomo"]:
        ans = (value_v * multiplier)/25
    else:
        raise Exception("unknown unit")
    return jsonify(
        status=200,

        replies=[{
            'type' : 'text',
            'content' : 'Son {} {}'.format(ans, unit_to)
        }]
    )

@app.route('/errors', methods=['POST'])
def errors():
  print(json.loads(request.get_data()))
  return jsonify(status=200)

app.run(port=port, host="0.0.0.0")