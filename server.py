from flask import Flask, request, jsonify
import json
import requests
import os

app = Flask(__name__)
port = int(os.environ["PATH"])

@app.route('/today_pomos', methods=['POST'])
def index():
  return jsonify(
    status=200,
    replies=[{
        'type' : 'text',
        'content' : 'infinitos'
    }]
  )

@app.route('/errors', methods=['POST'])
def errors():
  print(json.loads(request.get_data()))
  return jsonify(status=200)

app.run(port=port, host="0.0.0.0")