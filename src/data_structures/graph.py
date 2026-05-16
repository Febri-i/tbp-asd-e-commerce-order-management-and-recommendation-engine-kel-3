from typing import Dict, List, Tuple

class _Node:   
    def __init__(self, data):
        self.data = data
        self.next: Optional['_Node'] = None

class QueueLinkedList:
    def __init__(self):
        self._head: Optional[_Node] = None
        self._tail: Optional[_Node] = None
        self._size: int = 0

    def enqueue(self, data) -> None:
        node = _Node(data)
        if self._tail:
            self._tail.next = node
        self._tail = node
        if self._head is None:
            self._head = node
        self._size += 1
        
     def dequeue(self):
        if self._head is None:
            raise IndexError("dequeue dari queue kosong")
        data = self._head.data
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return data

    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size

class GraphRekomendasi:
    def __init__(self):
        self.adj: Dict[str, List[Tuple[str, int]]] = {} # kode -> [(kode, freq)]

    def _ensure_node(self, kode: str) -> None:     
        if kode not in self.adj:
            self.adj[kode] = []

     def _update_edge(self, src: str, dst: str) -> None:
        for i, (neighbor, freq) in enumerate(self.adj[src]):
            if neighbor == dst:
                self.adj[src][i] = (dst, freq + 1)
                return
        self.adj[src].append((dst, 1)) 

    def add_copurchase(self, kode_a: str, kode_b: str) -> None:
         self._ensure_node(kode_a)
        self._ensure_node(kode_b)
        self._update_edge(kode_a, kode_b)
        self._update_edge(kode_b, kode_a)

    def rekomendasikan(self, kode_produk: str, max_hop: int = 2) -> List[str]:
         if kode_produk not in self.adj:
            return []

        queue   = QueueLinkedList()
        visited = {kode_produk}
        hasil:  List[str] = []

        queue.enqueue((kode_produk, 0))

        while not queue.is_empty():
            node, hop = queue.dequeue()

            if hop >= max_hop:
                continue 

            neighbors_sorted = sorted(
                self.adj.get(node, []),
                key=lambda x: -x[1]
            )

            for neighbor, _freq in neighbors_sorted:
                if neighbor not in visited:  
                    visited.add(neighbor)
                    hasil.append(neighbor)
                    queue.enqueue((neighbor, hop + 1))

        return hasil

    # Utilitas debug
    def tampilkan_graf(self) -> None:
        print("=== Graf Rekomendasi ===")
        for node, edges in sorted(self.adj.items()):
            edge_str = ", ".join(
                f"{nb}(w={w})"
                for nb, w in sorted(edges, key=lambda x: -x[1])
            )
            print(f"  {node} → [{edge_str}]")
        print()

# Demo
if __name__ == "__main__":
    g = GraphRekomendasi()

    # Simulasi transaksi co-purchase
    transaksi = [
        ("P1", "P2"), ("P1", "P2"), ("P1", "P3"),
        ("P2", "P4"), ("P2", "P4"), ("P2", "P4"),
        ("P3", "P5"), ("P4", "P6"), ("P5", "P6"),
    ]
    for a, b in transaksi:
        g.add_copurchase(a, b)

    g.tampilkan_graf()

    for produk in ["P1", "P2", "P3"]:
        hasil = g.rekomendasikan(produk, max_hop=2)
        print(f"Rekomendasi untuk {produk} (hop ≤ 2): {hasil}")
