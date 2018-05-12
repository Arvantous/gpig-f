import json
from GridNodeTemplateRegistry import GridNodeTemplateRegistry
from SimEng import World

class Grid(World):

    def __init__(self, config_filepath, template_filepath):
        super().__init__()
        registry = GridNodeTemplateRegistry(template_filepath)
        with open(config_filepath) as config_file:
            config = json.load(config_file)
            nodes = {}

            # first pass: create nodes and add them to the grid
            for node_config in config["nodes"]:
                node = registry.make_node(node_config["type"], node_config["id"], self)
                nodes[node.node_id] = node

            # second pass: connect nodes
            for node_config in config["nodes"]:
                if node_config["parentNode"] is not None:
                    nodes[node_config["id"]].parent_node = nodes[node_config["parentNode"]]
                    nodes[node_config["parentNode"]].children_nodes.append(nodes[node_config["id"]])

    def step_all(self):
        """step and update all agents in simulation"""
        super().step_all()

        nodes = self.find_leaf_nodes()
        for node in nodes:
            node.observe_orient_strategy.execute(node)
            if node.parent_node is not None:
                nodes.append(node.parent_node)

        nodes = self.find_root_nodes()
        for node in nodes:
            node.decide_act_strategy.execute(node)
            nodes.extend(node.children_nodes)

    def find_leaf_nodes(self):
        return list(filter(lambda node: len(node.children_nodes) == 0, self.agents))

    def find_root_nodes(self):
        return list(filter(lambda node: node.parent_node is None, self.agents))

if __name__ == "__main__":
    """
    run tests
    """
    grid = Grid("./config/config.json", "./config/templates.json")
