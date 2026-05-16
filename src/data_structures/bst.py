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
    
    def insert(self, produk: Produk) -> bool:
        """Big-O = O(log n), worst case = O(n)"""
        new_node = BSTNode(produk)

        if self.root is None:
            self.root = new_node
            self._size += 1
            return True
        
        curr = self.root
        while True:
            if produk.kode < curr.produk.kode:
                if curr.left is None:
                    curr.left = BSTNode(produk, parent=curr)
                    break
                curr = curr.left
            elif produk.kode > curr.produk.kode:
                if curr.right is None:
                    curr.right = BSTNode(produk, parent=curr)
                    break
                curr = curr.right
            else:
                return False
        
        self._size += 1
        return True
    
    def delete(self, kode: str) -> bool:
        """Big-O = O(log n), worst case = O(n)"""
        n = self._find_node(kode)
        if not n:
            return False
        
        if n.left and n.right: 
            s = n.right
            while s.left:
                s = s.left
            n.produk = s.produk
            n = s
        ch = n.left if n.left else n.right

        if ch:
            ch.parent = n.parent

        if not n.parent:
            self.root = ch
        elif n == n.parent.left:
            n.parent.left = ch
        else:
            n.parent.right = ch

        self._size -= 1 
        return True
    
    def search(self, kode: str) -> Optional[Produk]:
        """Big-O = O(log n)"""
        node = self._find_node(kode)
        return node.produk if node else None
        

    def update_stok(self, kode: str, qty_delta: int) -> bool:
        """Big-O = O(log n)"""
        node = self._find_node(kode)

        if not node:
            return False
        
        if node.produk.stok + qty_delta < 0:
            return False
        
        node.produk.stok += qty_delta
        return True
    
