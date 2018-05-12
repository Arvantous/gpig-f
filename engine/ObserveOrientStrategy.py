from GridNode import ShareTicket, TransferTicket
from Strategy import Strategy

class ObserveOrientStrategy(Strategy):

    def execute(node):
        node.power_level += node.power_production_rate
        node.power_level -= node.power_consumption_rate
        node.power_level += sum([amount for _, amount in node.share_queue])
        node.power_level -= sum([amount for _, amount in node.request_queue])
        if node.parent_node is not None:
            if node.power_level < 0:
                node.send_request_ticket(-node.power_level)
            elif node.power_level > 0:
                node.send_share_ticket(node.power_level)
