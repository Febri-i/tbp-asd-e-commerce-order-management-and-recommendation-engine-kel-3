from typing import Optional, List
from data_structures.produk import Produk

class BSTNode:
    def __init__(self, produk: Produk):
        self.produk = produk
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

class BSTKatalog:
    def __init__(self):
        self.root: Optional[BSTNode] = None
    def insert(self, produk: Produk) -> None:
    # TODO: kunci = produk.kode (string comparison)
        pass
    def search(self, kode: str) -> Optional[Produk]:
    # TODO: implementasikan
        pass
    def update_stok(self, kode: str, qty_delta: int) -> bool:
        return False

    def inorder(self) -> List[Produk]:
        return [];
    # TODO: kembalikan list Produk terurut kode
