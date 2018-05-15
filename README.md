# GPIG - Simulation
This is a repository containing containing the source code for the demonstration simulation and engine.


Requirements:

[Python 3](https://www.python.org/downloads/)

Installing Pip on University Computer

Make a directory:
```
mkdir pip-install
cd pip-install
```

Get pip installer
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
Install pip
```
python3 get-pip.py
```

[Flask](http://flask.pocoo.org/)

Flask can be installed on University computers using the following command:
```
$ python3 -m pip install --user flask
```

## Running the simulation


Run:

```
$ python ./engine/GridWebInterface.py
```


Go to:

```
http://127.0.0.1:5000/
```
# A complete example
A complete example, with simulation backend, web server, and a website to render the information can be found under: 
```
/engine/examples/Complete Example
```
Run this example using:
```
$ cd /engine/examples/Complete\ Example
/engine/examples/Complete\ Example$ python webInterface.py

```

# Create a basic simulation, Hello World
Import the World and Agent object. The World class is a container for the simulation. It controls the update order for the objects and provides a parent for the object to communicate through. it provides methods for updating each agent.

The Agent class is the actor, the thing that will be updated each step of the simulation.
```python
from SimEng import World, Agent
``` 
We create a new agent using the base Agent class a blueprint, purpose of this agent will be to say "Hello World" and tell us how many steps have passed since the simulation was started.
We can define this agent as so:
```python
class Hello_world(Agent):
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
hello_agent = Hello_world(my_world)
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

The simulation will be run on a separate thread, and will contact the outside world through the a web interface run on Flask. We import the relevant modules.

```python
import threading
import time
from flask import Flask, jsonify
from SimEng import World, Agent
```
As in the previous example, we define a Hello World agent which will just increment it's own step counter. A function is added "toJson" which returns a json object containing the objects properties we are interested in for transmitting. We also create the app variable which flask uses to tell which app it will be running on the web server, in this case it is the this file itself. We set my_world as a global variable so that the generated responses can access the running simulation attributes.
```python
my_world = None
app = Flask(__name__)
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
```
A method is created to start up the simulation before the first web request. The world is instantiated and an agent is created to execute within that world. Using threads the simulation is run in the background with a time step executing every 1 second.
```python
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

```
A web entry point needs to be created, this is the URL that will be used to handle the GET request for information about the currently running simulation. Flask uses the 'app.route' decorator to define the access URL, in this case the index page. This function returns the json data of the first agent in the world list.
```python
@app.route('/')
def hello_world():
    # Return the step value of the first
    return my_world.agents[0].toJson()
```
We create a quick method to run the web server in debug mode so we can see what's going on.
```python
if __name__ == "__main__":
    app.run(debug=True)
```
Accessing the web server by the given URL, in our case 'http://127.0.0.1:5000/' and returns the json data.
![Image of json Return](https://github.com/vd548/gpig-f/blob/master/pictures/jsonReturn.png)

## Full Code
```python
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

```
Open your web browser and go to the appropriate url, likely "http://127.0.0.1:5000/" to receive the json request.

