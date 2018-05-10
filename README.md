# GPIG - Simulation
This is a repository containing containing the source code for the demonstration simulation and engine.

Code is written in Python 3.

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
helloAgent = Agent(my_world)
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



