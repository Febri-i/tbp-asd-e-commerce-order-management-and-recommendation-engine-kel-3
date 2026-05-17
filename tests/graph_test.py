import sys
import os
import unittest

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

src_path = os.path.join(root_path, 'src')

sys.path.insert(0, root_path)
sys.path.insert(0, src_path)

from data_structures.graph import GraphRekomendasi

class TestGraphRekomendasi(unittest.TestCase):
    def setUp(self):
        """
        Dijalankan sebelum setiap test case.
        Membuat instance graf baru yang kosong agar pengujian saling terisolasi.
        """
        self.graph = GraphRekomendasi()

    def test_add_copurchase_baru(self):
        """Memastikan edge baru ditambahkan dengan frekuensi awal 1 secara dua arah (undirected)."""
        self.graph.add_copurchase("P001", "P002")
        
        # Validasi arah P001 -> P002
        self.assertIn("P001", self.graph.adj, "Node P001 gagal dibuat di Adjacency List")
        self.assertEqual(self.graph.adj["P001"][0], ("P002", 1), "Relasi ke P002 atau frekuensi salah")
        
        # Validasi arah P002 -> P001
        self.assertIn("P002", self.graph.adj, "Node P002 gagal dibuat di Adjacency List")
        self.assertEqual(self.graph.adj["P002"][0], ("P001", 1), "Relasi ke P001 atau frekuensi salah")

    def test_add_copurchase_existing(self):
        """Memastikan bobot (frekuensi) bertambah jika produk dibeli bersamaan lebih dari sekali."""
        self.graph.add_copurchase("P001", "P002")
        self.graph.add_copurchase("P001", "P002") # Simulasi dibeli bersamaan untuk kedua kalinya
        
        self.assertEqual(self.graph.adj["P001"][0], ("P002", 2), "Frekuensi P001 -> P002 gagal bertambah")
        self.assertEqual(self.graph.adj["P002"][0], ("P001", 2), "Frekuensi P002 -> P001 gagal bertambah")

    def test_add_copurchase_self_loop(self):
        """Memastikan sistem menolak relasi produk dengan dirinya sendiri."""
        self.graph.add_copurchase("P001", "P001")
        
        self.assertNotIn("P001", self.graph.adj, "Sistem salah mencatat self-loop di Adjacency List")

    def test_rekomendasikan_tidak_ada(self):
        """Memastikan pencarian pada produk yang belum memiliki riwayat mengembalikan list kosong."""
        hasil = self.graph.rekomendasikan("P999")
        
        self.assertEqual(hasil, [], "Sistem seharusnya mengembalikan list kosong untuk produk tak dikenal")

    def test_rekomendasikan_max_hop(self):
        """Memastikan algoritma BFS berjalan benar dan mematuhi batasan max_hop."""
        # Simulasi Jaringan:
        # P001 saling beli dengan P002 (Hop 1 dari P001)
        # P002 saling beli dengan P003 (Hop 2 dari P001)
        # P003 saling beli dengan P004 (Hop 3 dari P001)
        self.graph.add_copurchase("P001", "P002")
        self.graph.add_copurchase("P002", "P003")
        self.graph.add_copurchase("P003", "P004")

        # Pengujian Hop = 1 (Seharusnya hanya P002)
        hasil_hop_1 = self.graph.rekomendasikan("P001", max_hop=1)
        self.assertIn("P002", hasil_hop_1)
        self.assertNotIn("P003", hasil_hop_1, "P003 bocor ke hop 1")

        # Pengujian Hop = 2 (Seharusnya P002 dan P003)
        hasil_hop_2 = self.graph.rekomendasikan("P001", max_hop=2)
        self.assertIn("P002", hasil_hop_2)
        self.assertIn("P003", hasil_hop_2)
        self.assertNotIn("P004", hasil_hop_2, "P004 bocor ke hop 2")

        # Pengujian Hop = 3 (Seharusnya menjangkau P004)
        hasil_hop_3 = self.graph.rekomendasikan("P001", max_hop=3)
        self.assertIn("P004", hasil_hop_3, "BFS gagal menjangkau kedalaman hop 3")

if __name__ == '__main__':
    unittest.main(verbosity=2)
