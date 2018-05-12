from GridNode import TransferTicket
from Strategy import Strategy

class DecideActStrategy(Strategy):

    def execute(node):
        if node.parent_node is None:
            if node.power_level < 0:
                node.transfer_queue.append(TransferTicket(None, node, -node.power_level))

        # All request tickets are satisfied, either locally or externally
        total_request_amount = sum([amount for _, amount in node.request_queue])
        for request_node, request_amount in node.request_queue:
            request_node.transfer_queue.append(TransferTicket(node, request_node, request_amount))

        # Decide which share tickets to satisfy
        for share_node, share_amount in node.share_queue:
            if total_request_amount >= share_amount:
                share_node.transfer_queue.append(TransferTicket(share_node, node, share_amount))
                total_request_amount -= share_amount
            else:
                share_node.transfer_queue.append(TransferTicket(share_node, node, total_request_amount))
                total_request_amount = 0
                break

        # Update power level using information from transfer queue
        for source_node, target_node, amount in node.transfer_queue:
            if source_node is node:
                node.power_level -= amount
            else:
                node.power_level += amount
        node.power_level = min(node.power_level, node.power_limit)
