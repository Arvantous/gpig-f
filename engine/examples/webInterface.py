import sys
import threading
import time
sys.path.append("..") # Adds higher directory to python modules path.
from flask import Flask, jsonify
from SimEng import World, Agent

# Global world object
my_world = None

class Hello_world(Agent):
    """Test Agent"""
    def __init__(self, world):
        super().__init__(world)
        self.steps = 0

    def step(self):
        self.steps += 1
        print("Hello world, steps:", self.steps)

    def toJson(self):
        return jsonify({"steps": self.steps})


app = Flask(__name__)

@app.before_first_request
def create_world():
    def run_simulation():
        # Tick simulation every 1 second
        while(True):
            my_world.step_all()
            time.sleep(1)
    global my_world
    my_world = World()
    hello_agent = Hello_world(my_world)

    thread = threading.Thread(target=run_simulation)
    thread.start()


@app.route('/')
def hello_world():
    # Return the step value of the first
    return my_world.agents[0].toJson()

if __name__ == "__main__":
    app.run(debug=True)
