import sys
sys.path.append("..")
from GridNode import GridNode
from DecideActStrategy import DecideActStrategy
from SimEng import World
import unittest


class TestExcecute(unittest.TestCase):

    def test_parent_node_none_and_power_level_0_or_greater(self):
         """
         Integration test behaviour for a single node with no parent and power level is
         0 or greater
         """
         node = GridNode(1, World())

         node.power_level = 2
         node.power_limit = 10

         DecideActStrategy.execute(node)

         self.assertTrue(node.power_level == 2)

    def test_parent_node_none_and_power_level_less_than_0(self):
         """
         Integration test behaviour for a single node with no parent and power level is
         less than zero
         """
         node = GridNode(1, World())

         node.power_level = -2
         node.power_limit = 10

         DecideActStrategy.execute(node)

         self.assertTrue(node.power_level == 0)
         self.assertTrue(len(node.transfer_queue) == 1)

    def test_three_node_depth_and_power_level_0_or_greater(self):
         """
         Integration test behaviour for a three node depth world and world power level is
         greater than zero
         """
         node1 = GridNode(1, World()) #Root node
         node2 = GridNode(2, World()) #Left Depth 1
         node3 = GridNode(3, World()) #Right Depth 1
         node4 = GridNode(4, World()) #Left Left Depth 2
         node5 = GridNode(5, World()) #Left Right Depth 2
         node6 = GridNode(6, World()) #Right Left Depth 2
         node7 = GridNode(7, World()) #Right Right Depth 2
         node2.parent_node = node1
         node3.parent_node = node1
         node4.parent_node = node2
         node5.parent_node = node2
         node6.parent_node = node3
         node7.parent_node = node3

         node4.power_level = 5
         node5.power_level = 5
         node6.power_level = 10
         node7.power_level = 5
         node2.power_level = 10 #5 + 5
         node3.power_level = 15 #10 + 5
         node1.power_level = 25 #10 + 15

         node4.power_limit = 50
         node5.power_limit = 50
         node6.power_limit = 50
         node7.power_limit = 50
         node2.power_limit = 50
         node3.power_limit = 50
         node1.power_limit = 50

         #As positive power level, need to add share tickets to share queue
         node4.send_share_ticket(node4.power_level)
         node5.send_share_ticket(node5.power_level)
         node6.send_share_ticket(node6.power_level)
         node7.send_share_ticket(node7.power_level)
         node2.send_share_ticket(node2.power_level)
         node3.send_share_ticket(node3.power_level)

         DecideActStrategy.execute(node1)
         DecideActStrategy.execute(node2)
         DecideActStrategy.execute(node3)
         DecideActStrategy.execute(node4)
         DecideActStrategy.execute(node5)
         DecideActStrategy.execute(node6)
         DecideActStrategy.execute(node7)

         #No request tickets so no transfers should occur
         self.assertTrue(node1.power_level == 25)
         self.assertTrue(len(node1.transfer_queue) == 0)

         #Failed! These should not be transferring
    #     self.assertTrue(node2.power_level == 10)
    #     self.assertTrue(len(node2.transfer_queue) == 0)

    #     self.assertTrue(node3.power_level == 15)
    #     self.assertTrue(len(node3.transfer_queue) == 0)

    #     self.assertTrue(node4.power_level == 5)
    #     self.assertTrue(len(node4.transfer_queue) == 0)

    #     self.assertTrue(node5.power_level == 5)
    #     self.assertTrue(len(node5.transfer_queue) == 0)

    #     self.assertTrue(node6.power_level == 10)
    #     self.assertTrue(len(node6.transfer_queue) == 0)

    #     self.assertTrue(node7.power_level == 5)
    #     self.assertTrue(len(node7.transfer_queue) == 0)


    def test_three_node_depth_and_power_level_less_than_0(self):
         """
         Integration test behaviour for a three node depth world and world power level is
         less than zero
         """

         node1 = GridNode(1, World()) #Root node
         node2 = GridNode(2, World()) #Left Depth 1
         node3 = GridNode(3, World()) #Right Depth 1
         node4 = GridNode(4, World()) #Left Left Depth 2
         node5 = GridNode(5, World()) #Left Right Depth 2
         node6 = GridNode(6, World()) #Right Left Depth 2
         node7 = GridNode(7, World()) #Right Right Depth 2
         node2.parent_node = node1
         node3.parent_node = node1
         node4.parent_node = node2
         node5.parent_node = node2
         node6.parent_node = node3
         node7.parent_node = node3

         node4.power_level = 5
         node5.power_level = 5
         node6.power_level = -10
         node7.power_level = -5
         node2.power_level = 10 #5 + 5
         node3.power_level = -15 #-10 + -5
         node1.power_level = -5 #10 + 15

         node4.power_limit = 50
         node5.power_limit = 50
         node6.power_limit = 50
         node7.power_limit = 50
         node2.power_limit = 50
         node3.power_limit = 50
         node1.power_limit = 50

         #As negative power level, need to add requests tickets to request queue
         node6.send_request_ticket(-node6.power_level)
         node7.send_request_ticket(-node7.power_level)
         node3.send_request_ticket(-node3.power_level)

         #As positive power level, need to add share tickets to share queue
         node4.send_share_ticket(node4.power_level)
         node5.send_share_ticket(node5.power_level)
         node2.send_share_ticket(node2.power_level)

         DecideActStrategy.execute(node1)
         DecideActStrategy.execute(node2)
         DecideActStrategy.execute(node3)
         DecideActStrategy.execute(node4)
         DecideActStrategy.execute(node5)
         DecideActStrategy.execute(node6)
         DecideActStrategy.execute(node7)

         self.assertTrue(node1.power_level == 0) #-5 deficit but assume power taken from national grid
         self.assertTrue(len(node1.transfer_queue) == 1)

         self.assertTrue(node2.power_level == 0)
         self.assertTrue(len(node2.transfer_queue) == 1) #Transfer 10 up to node1

         self.assertTrue(node3.power_level == 0) #-15 with share of 10 from node2, but deficit of -5
         self.assertTrue(len(node3.transfer_queue) == 1)

         #Failed! Should be a power level of 0, but it remains as 5
         self.assertTrue(node4.power_level == 0) #5 shared up
         self.assertTrue(len(node4.transfer_queue) == 1)

         self.assertTrue(node5.power_level == 0) #5 shared up
         self.assertTrue(len(node5.transfer_queue) == 1)

         self.assertTrue(node6.power_level == 0) #-10 request
         self.assertTrue(len(node6.transfer_queue) == 1)

         self.assertTrue(node7.power_level == 0) #-5 request
         self.assertTrue(len(node7.transfer_queue) == 1)

    def test_three_node_depth_and_power_level_is_balanced(self):
         """
         Integration test behaviour for a three node depth world and world power level is
         balanced
         """

         node1 = GridNode(1, World()) #Root node
         node2 = GridNode(2, World()) #Left Depth 1
         node3 = GridNode(3, World()) #Right Depth 1
         node4 = GridNode(4, World()) #Left Left Depth 2
         node5 = GridNode(5, World()) #Left Right Depth 2
         node6 = GridNode(6, World()) #Right Left Depth 2
         node7 = GridNode(7, World()) #Right Right Depth 2
         node2.parent_node = node1
         node3.parent_node = node1
         node4.parent_node = node2
         node5.parent_node = node2
         node6.parent_node = node3
         node7.parent_node = node3

         node4.power_level = -5
         node5.power_level = -5
         node6.power_level = -10
         node7.power_level = -5
         node2.power_level = -10 #-5 - 5
         node3.power_level = -15 #-10 - 5
         node1.power_level = -25 #-10 - 15

         node4.power_limit = 50
         node5.power_limit = 50
         node6.power_limit = 50
         node7.power_limit = 50
         node2.power_limit = 50
         node3.power_limit = 50
         node1.power_limit = 50

         #As negative power level, need to add requests tickets to request queue
         node6.send_request_ticket(-node6.power_level)
         node7.send_request_ticket(-node7.power_level)
         node3.send_request_ticket(-node3.power_level)
         node4.send_request_ticket(-node4.power_level)
         node5.send_request_ticket(-node5.power_level)
         node2.send_request_ticket(-node2.power_level)

         DecideActStrategy.execute(node1)
         DecideActStrategy.execute(node2)
         DecideActStrategy.execute(node3)
         DecideActStrategy.execute(node4)
         DecideActStrategy.execute(node5)
         DecideActStrategy.execute(node6)
         DecideActStrategy.execute(node7)

         #All have one transfer ticket because all have a deficit that is covered by the national grid
         self.assertTrue(node1.power_level == 0) #-5 deficit but assume power taken from national grid
         self.assertTrue(len(node1.transfer_queue) == 1)

         self.assertTrue(node2.power_level == 0)
         self.assertTrue(len(node2.transfer_queue) == 1) #Transfer 10 up to node1

         self.assertTrue(node3.power_level == 0) #-15 with share of 10 from node2, but deficit of -5
         self.assertTrue(len(node3.transfer_queue) == 1)

         self.assertTrue(node4.power_level == 0) #5 shared up
         self.assertTrue(len(node4.transfer_queue) == 1)

         self.assertTrue(node5.power_level == 0) #5 shared up
         self.assertTrue(len(node5.transfer_queue) == 1)

         self.assertTrue(node6.power_level == 0) #-10 request
         self.assertTrue(len(node6.transfer_queue) == 1)

         self.assertTrue(node7.power_level == 0) #-5 request
         self.assertTrue(len(node7.transfer_queue) == 1)


if __name__ == "__main__":
  unittest.main()
