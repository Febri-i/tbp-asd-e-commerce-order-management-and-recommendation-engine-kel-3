from data_structures.ll import LLNode
from typing import Optional

class Queue:
    """FIFO Queue berbasis Linked List."""
    def __init__(self):
        self.head: Optional[LLNode] = None
        self.tail: Optional[LLNode] = None
        self._size: int = 0

    def enqueue(self, data) -> None:
        """Big-O: O(1) sisip di tail."""
        """Menambahkan pesanan/order baru ke antrean paling belakang"""
        new_node = LLNode(data)
        if self.is_empty() or not self.tail:
            self.head= self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def dequeue(self):
        """Big-O: O(1) ambil dari head."""
        """Memproses/mengambil pesanan antrean paling depan"""
        if self.is_empty() or not self.head:
            return None
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return data


    def peek(self):
        return self.head.data if self.head else None

    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size
