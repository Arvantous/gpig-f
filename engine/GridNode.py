import copy
import json
from SimEng import Agent

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
        self.behavioural_strategies = []
        self.evaluation_strategy = None

    def to_dict(self):
        node_data = copy.deepcopy(vars(self))
        node_data["parent_node"] = None if self.parent_node is None else self.parent_node.node_id
        node_data["children_nodes"] = [child_node.node_id for child_node in self.children_nodes]
        return node_data

    def step(self):
        self.power_level += self.power_production_rate
        self.power_level -= self.power_consumption_rate
        self.power_level = max(0, min(self.power_limit, self.power_level))
        # Execute strategies



class GridNodeTemplateRegistry(object):

    def __init__(self, template_filepath):
        self.templates = {}
        with open(template_filepath) as template_file:
            templates = json.load(template_file)["templates"]
            for template in templates:
                self.templates[template["type"]] = template

    def make_node(self, node_type, node_id, world):
        if node_type in self.templates:
            template = self.templates[node_type]
            node = GridNode(node_id, world)
            node.node_priority = template["priority"]
            node.power_level = template["powerLevel"]
            node.power_limit = template["powerLimit"]
            node.power_production_rate = template["powerProductionRate"]
            node.power_consumption_rate = template["powerConsumptionRate"]
            node.behavioural_strategies = template["behaviouralStrategies"]
            node.evaluation_strategy = template["evaluationStrategy"]
            return node
        else:
            raise RuntimeError("Could not find a node with type '{}'".format(node_type))
