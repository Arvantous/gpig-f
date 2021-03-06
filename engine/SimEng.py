import copy
import json

class World(object):
    """
    Scene Object, container for agents for steppables
    """

    def __init__(self):
        self.agents = []
        self.run = True
        self.steps = 0

    def to_dict(self):
        world_data = copy.deepcopy(vars(self))
        world_data["agents"] = [agent.to_dict() for agent in self.agents]
        return world_data

    def to_json(self):
        return json.dumps(self.to_dict(), default=lambda obj: str(obj))

    def add_agent(self,agent):
        """Add agent to list of agents, sort on update priority, higher is more important"""
        self.agents.append(agent)
        self.agents = sorted(self.agents, key = lambda x: x.sim_priority, reverse=True)

    def step_all(self):
        """step and update all agents in simulation"""
        for agent in self.agents:
            agent.step()

    def run_forever(self):
        """Run simulation forever, or until stop"""
        while(run):
            self.step_all()
            self.steps += 1

    def run_for_n(self,steps):
        """Run simulation for n steps"""
        for step in range(steps):
            self.step_all()
            self.steps += 1

class Agent(object):
    """
    Smallest steppable object
    """
    def __init__(self, world, sim_priority = 0):
        self.world = world
        self.sim_priority = sim_priority
        world.add_agent(self)


    def step(self):
        """Empty step"""
        pass
