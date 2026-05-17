import sys
import os
import unittest
import time
import random

# Tambahkan folder 'src' ke sys.path, agar 'data_structures' bisa diakses
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_structures.bst import BSTKatalog
from data_structures.produk import Produk

class TestBSTKatalog(unittest.TestCase):
    """Unit tests untuk BSTKatalog (fitur dan analisis kompleksitas)"""

    def setUp(self):
        self.katalog = BSTKatalog()
        self.produk1 = Produk("P001", "Laptop", 15000000, 10)
        self.produk2 = Produk("P002", "Mouse", 200000, 50)
        self.produk3 = Produk("P003", "Keyboard", 500000, 30)
        self.produk4 = Produk("P004", "Monitor", 3000000, 5)

    # ------------------------ INSERT & SEARCH ------------------------
    def test_insert_and_search(self):
        self.assertTrue(self.katalog.insert(self.produk1))
        self.assertTrue(self.katalog.insert(self.produk2))
        self.assertTrue(self.katalog.insert(self.produk3))

        self.assertEqual(self.katalog.search("P001"), self.produk1)
        self.assertEqual(self.katalog.search("P002"), self.produk2)
        self.assertEqual(self.katalog.search("P003"), self.produk3)
        self.assertIsNone(self.katalog.search("P999"))

    def test_insert_duplicate(self):
        self.assertTrue(self.katalog.insert(self.produk1))
        self.assertFalse(self.katalog.insert(self.produk1))

    # ------------------------ DELETE ------------------------
    def test_delete_leaf(self):
        self.katalog.insert(self.produk1)
        self.katalog.insert(self.produk2)
        self.assertTrue(self.katalog.delete("P002"))
        self.assertIsNone(self.katalog.search("P002"))
        self.assertEqual(len(self.katalog), 1)

    def test_delete_node_one_child(self):
        self.katalog.insert(self.produk2)  # P002
        self.katalog.insert(self.produk1)  # P001 left
        self.katalog.insert(self.produk3)  # P003 right
        self.assertTrue(self.katalog.delete("P001"))
        self.assertTrue(self.katalog.delete("P002"))
        self.assertIsNone(self.katalog.search("P002"))
        self.assertEqual(self.katalog.search("P003"), self.produk3)
        self.assertEqual(len(self.katalog), 1)

    def test_delete_node_two_children(self):
        self.katalog.insert(self.produk2)
        self.katalog.insert(self.produk1)
        self.katalog.insert(self.produk3)
        self.katalog.insert(self.produk4)
        self.assertTrue(self.katalog.delete("P002"))
        self.assertIsNone(self.katalog.search("P002"))
        assert self.katalog.root is not None
        # Inorder successor: P003
        self.assertEqual(self.katalog.root.produk.kode, "P003")
        self.assertEqual(len(self.katalog), 3)
        self.assertEqual(self.katalog.search("P001"), self.produk1)
        self.assertEqual(self.katalog.search("P004"), self.produk4)

    def test_delete_root_only(self):
        self.katalog.insert(self.produk1)
        self.assertTrue(self.katalog.delete("P001"))
        self.assertIsNone(self.katalog.root)
        self.assertEqual(len(self.katalog), 0)

    def test_delete_not_found(self):
        self.katalog.insert(self.produk1)
        self.assertFalse(self.katalog.delete("P999"))

    # ------------------------ UPDATE STOK ------------------------
    def test_update_stok_positive(self):
        self.katalog.insert(self.produk1)
        self.assertTrue(self.katalog.update_stok("P001", 5))
        self.assertEqual(self.produk1.stok, 15)

    def test_update_stok_negative(self):
        self.katalog.insert(self.produk1)
        self.assertTrue(self.katalog.update_stok("P001", -3))
        self.assertEqual(self.produk1.stok, 7)

    def test_update_stok_insufficient(self):
        self.katalog.insert(self.produk1)  # stok = 10
        self.assertFalse(self.katalog.update_stok("P001", -20))
        self.assertEqual(self.produk1.stok, 10)

    def test_update_stok_not_found(self):
        self.assertFalse(self.katalog.update_stok("P999", 5))

    # ------------------------ LENGTH ------------------------
    def test_len(self):
        self.assertEqual(len(self.katalog), 0)
        self.katalog.insert(self.produk1)
        self.assertEqual(len(self.katalog), 1)
        self.katalog.insert(self.produk2)
        self.assertEqual(len(self.katalog), 2)
        self.katalog.delete("P001")
        self.assertEqual(len(self.katalog), 1)
        self.katalog.delete("P002")
        self.assertEqual(len(self.katalog), 0)

    # ------------------------ INORDER TRAVERSAL ------------------------
    def test_inorder(self):
        produk_list = [
            Produk("P002", "Mouse", 200000, 50),
            Produk("P001", "Laptop", 15000000, 10),
            Produk("P004", "Monitor", 3000000, 5),
            Produk("P003", "Keyboard", 500000, 30)
        ]
        for p in produk_list:
            self.katalog.insert(p)
        inorder_result = self.katalog.inorder()
        kodes = [p.kode for p in inorder_result]
        self.assertEqual(kodes, ["P001", "P002", "P003", "P004"])




if __name__ == "__main__":
    unittest.main(verbosity=2)
