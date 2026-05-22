from typing import Optional

class BSTNode:
    """Struktur data murni Node BST."""
    __slots__ = 'produk', 'left', 'right', 'parent'
    def __init__(self, produk, parent: Optional['BSTNode'] = None):
        self.produk = produk
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None
        self.parent: Optional['BSTNode'] = parent