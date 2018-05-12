import collections
import copy

ShareTicket = collections.namedtuple('ShareTicket', ['source', 'amount'])
RequestTicket = collections.namedtuple('RequestTicket', ['source', 'amount'])
TransferTicket = collections.namedtuple('TransferTicket', ['source', 'target', 'amount'])

from SimEng import Agent
from DecideActStrategy import DecideActStrategy
from ObserveOrientStrategy import ObserveOrientStrategy


class GridNode(Agent):

    def __init__(self, node_id, world, sim_priority=0):
        super().__init__(world, sim_priority)
        self.node_priority = 0
        self.node_id = node_id
        self.parent_node = None
        self.children_nodes = []
        self.power_level = 0
        self.power_limit = 0
        self.power_production_rate = 0
        self.power_consumption_rate = 0
        self.observe_orient_strategy = ObserveOrientStrategy
        self.decide_act_strategy = DecideActStrategy
        self.share_queue = []
        self.request_queue = []
        self.transfer_queue = []

    def to_dict(self):
        node_data = copy.deepcopy(vars(self))
        node_data["parent_node"] = None if self.parent_node is None else self.parent_node.node_id
        node_data["children_nodes"] = [child_node.node_id for child_node in self.children_nodes]
        return node_data

    def step(self):
        self.share_queue.clear()
        self.request_queue.clear()
        self.transfer_queue.clear()

    def send_request_ticket(self, amount):
        self.parent_node.add_request_ticket(self, amount)

    def send_share_ticket(self, amount):
        self.parent_node.add_share_ticket(self, amount)

    def add_request_ticket(self, source, amount):
        self.request_queue.append(RequestTicket(source, amount))

    def add_share_ticket(self, source, amount):
        self.share_queue.append(ShareTicket(source, amount))
