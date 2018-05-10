import sys
sys.path.append("..") # Adds higher directory to python modules path.

from SimEng import World, Agent



class Test(Agent):
    """Test Agent"""
    def __init__(self, world):
        super(Test, self).__init__(world)
        self.steps = 0

    def step(self):
        self.steps +=1
        print("Hello world, steps:", self.steps)


class Test2(Agent):
    """Test Agent"""
    def __init__(self, world):
        super(Test2, self).__init__(world,1)
        self.steps = 0

    def step(self):
        self.steps +=1
        print("Hello from 2, steps:", self.steps)

# Class House(Agent), -> Read from usage file -> update power usage -> make request
# Class Node(Agent), ->

if __name__ == "__main__":
    myWorld = World()
    c = Test2(myWorld)
    a = Test(myWorld)
    b = Test(myWorld)
