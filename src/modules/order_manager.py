from data_structures.linked_list import Queue, Stack

class MultiPriorityQueue:
    """
    Mengelola 3 antrian terpisah untuk tier Premium, Regular, dan Economy.
    Analisis Big-O: Enqueue O(1), Serve O(1) [Panduan Proyek 3.3].
    """
    def __init__(self):

        self.queues = {
            1: Queue(), # PREMIUM
            2: Queue(), # REGULAR
            3: Queue()  # ECONOMY
        }
        self.undo_stack = Stack()

    def order(self, order_obj):
        """Menambahkan pesanan ke queue yang sesuai berdasarkan tier."""
        tier = order_obj.tier
        self.queues[tier].enqueue(order_obj)
        self.undo_stack.push(order_obj)
        return True

    def serve(self):
        """
        Mengambil pesanan (SERVE) dengan prioritas: Premium > Regular > Economy.
        Big-O: O(1) karena hanya mengecek 3 head pointer [7].
        """
        for tier in [1, 8, 9]:
            if not self.queues[tier].is_empty():
                return self.queues[tier].dequeue()
        return None

    def cancel_last(self):
        """Membatalkan pesanan terakhir menggunakan Stack-based undo [2]."""
        if self.undo_stack.is_empty():
            return False
        order_to_cancel = self.undo_stack.pop()
        return order_to_cancel
