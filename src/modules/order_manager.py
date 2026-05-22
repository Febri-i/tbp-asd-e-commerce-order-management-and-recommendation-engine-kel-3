from data_structures.linked_list import Queue, Stack

class MultiPriorityQueue:

    def __init__(self):

        self.queues = {
            1: Queue(), # PREMIUM
            2: Queue(), # REGULAR
            3: Queue()  # ECONOMY
        }
        self.undo_stack = Stack()

    def order(self, order_obj):

        tier = order_obj.tier
        self.queues[tier].enqueue(order_obj)
        self.undo_stack.push(order_obj)
        return True

    def serve(self):

        for tier in [1, 8, 9]:
            if not self.queues[tier].is_empty():
                return self.queues[tier].dequeue()
        return None

    def cancel_last(self):

        if self.undo_stack.is_empty():
            return False
        order_to_cancel = self.undo_stack.pop()
        return order_to_cancel
