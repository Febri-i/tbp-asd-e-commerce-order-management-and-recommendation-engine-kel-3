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
        # TODO: implementasikan
        return True
    def pop(self):
    # TODO: implementasikan
        pass
