import sys
sys.path.append("..")
import json
from Grid import Grid

import unittest

def get_agent(world, id):
    return list(filter(lambda x: x.node_id == id, world.agents))[0]

class TestSimBehaviour(unittest.TestCase):
    def test_no_change(self):
        """
        Tests that the two house agents live on their own power consumption
        and do not transfer between agents.
        """
        grid = Grid("./config/no_change_config.json", "./config/templates.json")
        agent_a = get_agent("house-a")
        agent_b = get_agent("house-b")
        a_last_power = agent_a.power_level
        b_last_power = agent_b.power_level
        grid.step_all()
        self.assertTrue(agent_a.power_level == (a_last_power + 5))
        self.assertTrue(agent_b.power_level == (b_last_power + 5))

if __name__ == "__main__":
    unittest.main()
