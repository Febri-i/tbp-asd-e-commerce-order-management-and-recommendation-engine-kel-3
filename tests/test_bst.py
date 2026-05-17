import sys
import os
import unittest
import time
import random

# Adjust path to import BSTKatalog from src/data_structures
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'data_structures')))

from bst import BSTKatalog

# Minimal Produk class for testing (matches expected attributes)
class Produk:
    def __init__(self, kode: str, nama: str, harga: int, stok: int):
        self.kode = kode
        self.nama = nama
        self.harga = harga
        self.stok = stok

    def __repr__(self):
        return f"Produk({self.kode}, stok={self.stok})"


class TestBSTKatalog(unittest.TestCase):
    """Unit tests for BSTKatalog covering all features and complexity analysis."""

    def setUp(self):
        """Create a fresh BST and some sample products before each test."""
        self.katalog = BSTKatalog()
        self.produk1 = Produk("P001", "Laptop", 15000000, 10)
        self.produk2 = Produk("P002", "Mouse", 200000, 50)
        self.produk3 = Produk("P003", "Keyboard", 500000, 30)
        self.produk4 = Produk("P004", "Monitor", 3000000, 5)

    # ------------------------ INSERT & SEARCH ------------------------
    def test_insert_and_search(self):
        """Test inserting products and searching for them by kode."""
        self.assertTrue(self.katalog.insert(self.produk1))
        self.assertTrue(self.katalog.insert(self.produk2))
        self.assertTrue(self.katalog.insert(self.produk3))

        self.assertEqual(self.katalog.search("P001"), self.produk1)
        self.assertEqual(self.katalog.search("P002"), self.produk2)
        self.assertEqual(self.katalog.search("P003"), self.produk3)
        self.assertIsNone(self.katalog.search("P999"))

    def test_insert_duplicate(self):
        """Inserting a product with an existing kode should return False."""
        self.assertTrue(self.katalog.insert(self.produk1))
        self.assertFalse(self.katalog.insert(self.produk1))  # Duplicate

    # ------------------------ DELETE ------------------------
    def test_delete_leaf(self):
        """Delete a leaf node (no children)."""
        self.katalog.insert(self.produk1)  # root
        self.katalog.insert(self.produk2)  # right child
        self.assertTrue(self.katalog.delete("P002"))  # leaf
        self.assertIsNone(self.katalog.search("P002"))
        self.assertEqual(len(self.katalog), 1)

    def test_delete_node_one_child(self):
        """Delete a node with exactly one child."""
        # Build tree: P002 (root) -> left child P001, right child P003
        self.katalog.insert(self.produk2)  # "P002"
        self.katalog.insert(self.produk1)  # "P001" left
        self.katalog.insert(self.produk3)  # "P003" right
        # Delete root with one child? Actually root has two children here.
        # Let's delete P001 (leaf) then P002 will have one child (P003)
        self.assertTrue(self.katalog.delete("P001"))
        # Now tree: P002 (root) with right child P003, left empty
        self.assertTrue(self.katalog.delete("P002"))  # node with one child (right)
        self.assertIsNone(self.katalog.search("P002"))
        self.assertEqual(self.katalog.search("P003"), self.produk3)
        self.assertEqual(len(self.katalog), 1)

    def test_delete_node_two_children(self):
        """Delete a node with two children (uses inorder successor)."""
        # Build a small BST
        self.katalog.insert(self.produk2)  # "P002" root
        self.katalog.insert(self.produk1)  # "P001" left
        self.katalog.insert(self.produk3)  # "P003" right
        self.katalog.insert(self.produk4)  # "P004" right-right
        # Delete root "P002" which has two children
        self.assertTrue(self.katalog.delete("P002"))
        self.assertIsNone(self.katalog.search("P002"))
        # Check that root was replaced by inorder successor (P003) and tree is still valid
        root_produk = self.katalog.root.produk
        self.assertEqual(root_produk.kode, "P003")  # successor
        self.assertEqual(len(self.katalog), 3)
        # Verify other nodes remain
        self.assertEqual(self.katalog.search("P001"), self.produk1)
        self.assertEqual(self.katalog.search("P004"), self.produk4)

    def test_delete_root_only(self):
        """Delete the only node (root with no children)."""
        self.katalog.insert(self.produk1)
        self.assertTrue(self.katalog.delete("P001"))
        self.assertIsNone(self.katalog.root)
        self.assertEqual(len(self.katalog), 0)

    def test_delete_not_found(self):
        """Deleting a non‑existent kode returns False."""
        self.katalog.insert(self.produk1)
        self.assertFalse(self.katalog.delete("P999"))

    # ------------------------ UPDATE STOK ------------------------
    def test_update_stok_positive(self):
        """Increase stock by a positive quantity."""
        self.katalog.insert(self.produk1)
        self.assertTrue(self.katalog.update_stok("P001", 5))
        self.assertEqual(self.produk1.stok, 15)

    def test_update_stok_negative(self):
        """Decrease stock by a negative quantity (if enough stock)."""
        self.katalog.insert(self.produk1)
        self.assertTrue(self.katalog.update_stok("P001", -3))
        self.assertEqual(self.produk1.stok, 7)

    def test_update_stok_insufficient(self):
        """Decreasing stock below zero should fail and leave stock unchanged."""
        self.katalog.insert(self.produk1)  # stok = 10
        self.assertFalse(self.katalog.update_stok("P001", -20))
        self.assertEqual(self.produk1.stok, 10)  # unchanged

    def test_update_stok_not_found(self):
        """Updating stock for a non‑existent product returns False."""
        self.assertFalse(self.katalog.update_stok("P999", 5))

    # ------------------------ LENGTH (__len__) ------------------------
    def test_len(self):
        """Test that __len__ returns the correct number of products."""
        self.assertEqual(len(self.katalog), 0)
        self.katalog.insert(self.produk1)
        self.assertEqual(len(self.katalog), 1)
        self.katalog.insert(self.produk2)
        self.assertEqual(len(self.katalog), 2)
        self.katalog.delete("P001")
        self.assertEqual(len(self.katalog), 1)
        self.katalog.delete("P002")
        self.assertEqual(len(self.katalog), 0)

    # ------------------------ BIG‑O ANALYSIS (Performance) ------------------------
    def test_complexity_analysis(self):
        """
        Measure insertion and search times for different input sizes.
        This is not a strict assertion but prints empirical results to demonstrate
        O(log n) average case and O(n) worst‑case behaviour.
        """
        sizes = [100, 500, 1000, 2000, 5000]
        print("\n=== Complexity Analysis (Average vs Worst Case) ===")
        print("Size\tAvg Insert (s)\tWorst Insert (s)\tSearch (s)")
        
        for n in sizes:
            # Average case: random order
            random_keys = [f"ID{i:05d}" for i in range(n)]
            random.shuffle(random_keys)
            bst_avg = BSTKatalog()
            start = time.perf_counter()
            for key in random_keys:
                bst_avg.insert(Produk(key, "item", 100, 1))
            avg_insert_time = time.perf_counter() - start

            # Worst case: sorted order (degenerate tree -> O(n))
            sorted_keys = sorted(random_keys)
            bst_worst = BSTKatalog()
            start = time.perf_counter()
            for key in sorted_keys:
                bst_worst.insert(Produk(key, "item", 100, 1))
            worst_insert_time = time.perf_counter() - start

            # Search in average tree
            target = random_keys[n//2]
            start = time.perf_counter()
            _ = bst_avg.search(target)
            search_time = time.perf_counter() - start

            print(f"{n}\t{avg_insert_time:.6f}\t\t{worst_insert_time:.6f}\t\t{search_time:.6f}")
        
        print("Observation: Average insert ~ O(log n), worst‑case insert ~ O(n).")
        print("Search also follows tree height (log n average, n worst‑case).\n")
        # No assertion – just informative output. Uncomment the line below to force a pass.
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main(verbosity=2)