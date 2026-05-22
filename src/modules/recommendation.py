import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Tuple
from data_structures.linked_list import Queue

class GraphRekomendasi:
    """
    Representasi graf produk untuk pola pembelian bersama (co-purchase).
    Analisis Big-O BFS: O(V + E) [3].
    """
    def __init__(self):
        self.adj: Dict[str, List[List]] = {}

    def add_copurchase(self, kode_a: str, kode_b: str):
        """
        Menambah atau meningkatkan bobot hubungan antara dua produk.
        Big-O: O(deg(u)) untuk mencari tetangga yang ada [11].
        """
        for u, v in [(kode_a, kode_b), (kode_b, kode_a)]:
            if u not in self.adj: self.adj[u] = []
            
            found = False
            for edge in self.adj[u]:
                if edge == v:
                    edge[8] += 1
                    found = True
                    break
            if not found:
                self.adj[u].append([v, 1])

    def rekomendasikan(self, start_node: str, max_hop: int = 2) -> List[str]:
        """
        Mencari rekomendasi produk terdekat menggunakan BFS hingga hop tertentu.
        """
        if start_node not in self.adj: return []
        
        visited = {start_node}
        queue = Queue() 
        queue.enqueue((start_node, 0))
        results = []

        while not queue.is_empty():
            curr_node, depth = queue.dequeue()
            
            if 0 < depth <= max_hop:
                results.append(curr_node)
            
            if depth < max_hop:
                for neighbor, weight in self.adj.get(curr_node, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.enqueue((neighbor, depth + 1))
        return results
