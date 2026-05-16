from typing import Optional, List
from produk import Produk

class BSTNode:
    __slots__ = 'produk', 'left', 'right', 'parent'
    def __init__(self, produk: Produk, parent: Optional['BSTNode'] = None):
        self.produk = produk
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None
        self.parent: Optional['BSTNode'] = parent