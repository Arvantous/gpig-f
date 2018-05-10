import sys
import threading
import time
from flask import Flask, jsonify
from SimEng import World, Agent
import json
from GridCreator import GridCreator

# Global world object

app = Flask(__name__)

grid = None

@app.before_first_request
def create_world():
    def run_simulation():
        # Tick simulation every 1 second
        while(True):
            grid.step_all()
            time.sleep(1)
    global grid
    grid = GridCreator.make_grid("../config/config.json", "../config/templates.json")
    thread = threading.Thread(target=run_simulation)
    thread.start()


@app.route('/')
def grid_interface():
    # Return the step value of the first
    return jsonify(json.loads(grid.to_json()))

if __name__ == "__main__":
    app.run(debug=True)
