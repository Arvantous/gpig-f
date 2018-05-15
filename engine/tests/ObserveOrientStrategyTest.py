import sys
sys.path.append("..")
from ObserveOrientStrategy import ObserveOrientStrategy
from GridNode import GridNode
from SimEng import World

import unittest

def get_agent(world, id):
     return list(filter(lambda x: x.node_id == id, world.agents))[0]

class TestExcecute(unittest.TestCase):
    def test_parent_node_none(self):
         """
         Unit test behaviour for node with no parent
         """
         node = GridNode(1, World())

         node.power_consumption_rate = 6
         node.power_production_rate = 8

         ObserveOrientStrategy.execute(node)

         self.assertTrue(node.power_level == 2)

    def test_balanced_node_with_parent(self):
         """
         Integration test behaviour for node with parent where net power is 0
         """
         parent_node = GridNode(0, World())
         child_node = GridNode(1, World())
         child_node.parent_node = parent_node

         child_node.power_consumption_rate = 6
         child_node.power_production_rate = 6

         ObserveOrientStrategy.execute(child_node)

         self.assertTrue(child_node.power_level == 0)
         self.assertTrue(len(parent_node.request_queue) == 0)
         self.assertTrue(len(parent_node.share_queue) == 0)

    def test_share_ticket_for_node_with_parent(self):
         """
         Integration test behaviour for node with parent where net power is positive.
         Check ShareTicket added to parent.
         """
         parent_node = GridNode(0, World())
         child_node = GridNode(1, World())
         child_node.parent_node = parent_node

         child_node.power_consumption_rate = 3
         child_node.power_production_rate = 8

         ObserveOrientStrategy.execute(child_node)

         self.assertTrue(child_node.power_level == 5)
         self.assertTrue(len(parent_node.request_queue) == 0)
         self.assertTrue(len(parent_node.share_queue) == 1)

    def test_request_ticket_for_node_with_parent(self):
         """
         Integration test behaviour for node with parent where net power is negative.
         Check RequestTicket is added to parent.
         """
         parent_node = GridNode(0, World())
         child_node = GridNode(1, World())
         child_node.parent_node = parent_node

         child_node.power_consumption_rate = 10
         child_node.power_production_rate = 8

         ObserveOrientStrategy.execute(child_node)

         self.assertTrue(child_node.power_level == -2)
         self.assertTrue(len(parent_node.request_queue) == 1)
         self.assertTrue(len(parent_node.share_queue) == 0)

    def test_share_and_request_tickets_added_to_power_level(self):
         """
         Integration test for parent nodes power level and sums over share queue and request queue.
         """
         world = World()
         parent_node = GridNode(0, world)
         child_node1 = GridNode(1, world)
         child_node2 = GridNode(2, world)
         child_node3 = GridNode(3, world)

         child_node1.parent_node = parent_node
         child_node2.parent_node = parent_node
         child_node3.parent_node = parent_node

         child_node1.power_consumption_rate = 10
         child_node1.power_production_rate = 12

         child_node2.power_consumption_rate = 3
         child_node2.power_production_rate = 8

         child_node3.power_consumption_rate = 9
         child_node3.power_production_rate = 3

         ObserveOrientStrategy.execute(child_node1) # Should send a share ticket of 2
         ObserveOrientStrategy.execute(child_node2) # Should send a share ticket of 5
         ObserveOrientStrategy.execute(child_node3) # Should send a request ticket of 6

         self.assertTrue(child_node1.power_level == 2)
         self.assertTrue(child_node2.power_level == 5)
         self.assertTrue(child_node3.power_level == -6)

         self.assertTrue(len(parent_node.request_queue) == 1)
         self.assertTrue(len(parent_node.share_queue) == 2)

         ObserveOrientStrategy.execute(parent_node)
         self.assertTrue(parent_node.power_level == 1) # 2 + 5 - 6

if __name__ == "__main__":
    unittest.main()
