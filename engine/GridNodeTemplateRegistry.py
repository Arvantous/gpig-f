import json
from GridNode import GridNode

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
            return node
        else:
            raise RuntimeError("Could not find a node with type '{}'".format(node_type))
