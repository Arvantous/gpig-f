import json
from GridNode import GridNode, GridNodeTemplateRegistry
from SimEng import World

class GridCreator(object):

    @staticmethod
    def make_grid(config_filepath, template_filepath):
        registry = GridNodeTemplateRegistry(template_filepath)
        with open(config_filepath) as config_file:
            config = json.load(config_file)
            nodes = {}
            grid = World()

            # first pass: create nodes and add them to the grid
            for node_config in config["nodes"]:
                node = registry.make_node(node_config["type"], node_config["id"], grid)
                nodes[node.node_id] = node

            # second pass: connect nodes
            for node_config in config["nodes"]:
                if node_config["parentNode"] is not None:
                    nodes[node_config["id"]].parent_node = nodes[node_config["parentNode"]]
                    nodes[node_config["parentNode"]].children_nodes.append(nodes[node_config["id"]])

            return grid

if __name__ == "__main__":
    grid = GridCreator.make_grid("gpig-f/config/config.json", "gpig-f/config/templates.json")
    print(grid.to_json())
    for _ in range(5):
        grid.step_all()
        print(grid.to_json())
        print()