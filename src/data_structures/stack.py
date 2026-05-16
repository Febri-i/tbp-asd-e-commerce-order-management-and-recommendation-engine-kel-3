from data_structures.ll import LLNode
from typing import Optional


class Stack:
    def __init__(self, kapasitas=10):
        self.top: Optional[LLNode] = None
        self._size: int = 0
        self.kapasitas = kapasitas
    def push(self, data) -> bool:
        """Big-O: O(1). Kembalikan False jika kapasitas penuh."""
        if self._size >= self.kapasitas:
        # Hapus elemen terbawah (implementasi opsional)
            return False
        new_node = LLNode(data)
        new_node.next = self.top
        self.top = new_node
        self._size += 1
        return True
    def pop(self):
        """Big-O: O(1) ambil dari top"""
        if self.top is None:
            return None
        data = self.top.data
        #geser top ke bawahnyya
        self.top = self.top.next
        self._size -= 1
        return data
