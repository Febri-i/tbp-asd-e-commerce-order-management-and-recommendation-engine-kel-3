from typing import Optional, List
from produk import Produk

class BSTNode:
    __slots__ = 'produk', 'left', 'right', 'parent'
    def __init__(self, produk: Produk, parent: Optional['BSTNode'] = None):
        self.produk = produk
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None
        self.parent: Optional['BSTNode'] = parent

class BSTKatalog:
    def __init__(self):
        self.root: Optional[BSTNode] = None
        self._size = 0

    def __len__(self) -> int:
        """Big-O = O(1)"""
        return self._size
    
    def _find_node(self, kode: str) -> Optional[BSTNode]:
        """Big-O = O(log n)"""
        curr = self.root
        while curr: 
            if kode == curr.produk.kode:
                return curr
            elif kode < curr.produk.kode:
                curr = curr.left
            else:
                curr = curr.right
        return None