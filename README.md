# GPIG - Simulation
This is a repository containing containing the source code for the demonstration simulation and engine.

Technologies:
[Python 3](https://www.python.org/downloads/)
[Flask](http://flask.pocoo.org/)

# Create a basic simulation, Hello World
Import the World and Agent object. The World class is a container for the simulation. It controls the update order for the objects and provides a parent for the object to communicate through. it provides methods for updating each agent.

The Agent class is the actor, the thing that will be updated each step of the simulation.
```python
from SimEng import World, Agent
``` 
We create a new agent using the base Agent class a blueprint, purpose of this agent will be to say "Hello World" and tell us how many steps have passed since the simulation was started.
We can define this agent as so:
```python
class HelloWorld(Agent):
    """Test Agent"""
    def __init__(self, world):
        super().__init__(world)
        self.steps = 0

    def step(self):
        self.steps += 1
        print("Hello world, steps:", self.steps)
```
The init method adds the HelloWorld Agent to the simulation world and sets the number of steps passed since the simulation began to 0 so we can count them :) . The step function is the action the agent will take at each step of the simulation. We can now create a new world and an agent to simulate.

```python
my_world = World()
hello_agent = Agent(my_world)
```
We pass the agent the world object so it can make reference to other entities and make itself a member of this simulation world. We can now run the simulation for 10 steps and see the corresponding output.
```python
my_world.run_for_n(10)
```
Output:
```
Hello world, steps: 1
Hello world, steps: 2
Hello world, steps: 3
Hello world, steps: 4
Hello world, steps: 5
Hello world, steps: 6
Hello world, steps: 7
Hello world, steps: 8
Hello world, steps: 9
Hello world, steps: 10
```
## Full Code
```python
from SimEng import World, Agent

class Hello_world(Agent):
    """Test Agent"""
    def __init__(self, world):
        super().__init__(world)
        self.steps = 0

    def step(self):
        self.steps += 1
        print("Hello world, steps:", self.steps)

if __name__ == "__main__":
    my_world = World()
    hello_agent = Hello_world(my_world)
    my_world.run_for_n(10)
```
# Extending our Simulation to enable a web interface

## Full Code
```python
import threading
import time
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
    # Return the step value of the first agent
    step_val = my_world.agents[0].steps
    return jsonify({"some_text":"Hello!","steps":step_val})

```
Open your web browser and go to the appropriate url, likely "http://127.0.0.1:5000/" to receive the json request.

