from typing import Dict, List, Tuple
class GraphRekomendasi:
    def __init__(self):
        self.adj: Dict[str, List[Tuple[str, int]]] = {} # kode -> [(kode, freq)]

    def add_copurchase(self, kode_a: str, kode_b: str) -> None:
        """Tambah atau tingkatkan bobot edge co-purchase. Big-O: O(deg)."""
        # TODO: implementasikan
        pass

    def rekomendasikan(self, kode_produk: str, max_hop: int = 2) -> List[str]:
        """BFS hingga max_hop, kembalikan list kode produk rekomendasi."""
        # TODO: implementasikan BFS dengan Queue Linked List
        return [];
