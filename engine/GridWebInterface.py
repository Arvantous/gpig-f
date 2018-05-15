import sys
import threading
import time
from flask import Flask, jsonify, request
from SimEng import World, Agent
import json
from Grid import Grid

# Global world object

app = Flask(__name__)

grid = None

@app.before_first_request
def create_world():
    global grid
    grid = Grid("./config/config.json", "./config/templates.json")

@app.route('/', methods=['GET', 'POST'])
def grid_interface():
    if request.method == 'POST':
        grid.step_all()
    resp = jsonify(json.loads(grid.to_json()))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == "__main__":
    app.run(debug=True)
