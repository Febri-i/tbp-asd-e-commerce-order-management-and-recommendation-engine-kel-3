import sys
import os
import unittest

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

src_path = os.path.join(root_path, 'src')

sys.path.insert(0, root_path)
sys.path.insert(0, src_path)
from unittest.mock import Mock
from src.data_structures.linked_list import LLNode 

from modules.insertion_sort import sorted_insert_order, insertion_sort_order

class TestInsertionSort(unittest.TestCase):
    
    def setUp(self):
        pass
    

    def test_sorted_insert_order(self):
        """Memastikan penyisipan node tunggal ke Linked List terurut berjalan benar (ascending)"""
        # Membuat List yang sudah terurut: 10 -> 30
        head = LLNode(Mock(waktu_pesan=10))
        head.next = LLNode(Mock(waktu_pesan=30))

        # Node baru dengan waktu_pesan di tengah-tengah (20)
        new_node = LLNode(Mock(waktu_pesan=20))
        
        # Eksekusi
        new_head = sorted_insert_order(new_node, head)
        
        # Verifikasi urutan menjadi 10 -> 20 -> 30
        self.assertIsNotNone(new_head)
        self.assertEqual(new_head.data.waktu_pesan, 10)
        self.assertEqual(new_head.next.data.waktu_pesan, 20)
        self.assertEqual(new_head.next.next.data.waktu_pesan, 30)

    def test_insertion_sort_order(self):
        """Memastikan insertion sort mengurutkan keseluruhan Linked List (ascending waktu_pesan)"""
        # Rangkai node acak: 50 -> 10 -> 40
        node1 = LLNode(Mock(waktu_pesan=50))
        node2 = LLNode(Mock(waktu_pesan=10))
        node3 = LLNode(Mock(waktu_pesan=40))
        
        node1.next = node2
        node2.next = node3

        # Eksekusi
        sorted_head = insertion_sort_order(node1)

        # Verifikasi urutan berubah jadi 10 -> 40 -> 50
        self.assertIsNotNone(sorted_head)
        self.assertEqual(sorted_head.data.waktu_pesan, 10)
        self.assertEqual(sorted_head.next.data.waktu_pesan, 40)
        self.assertEqual(sorted_head.next.next.data.waktu_pesan, 50)
        self.assertIsNone(sorted_head.next.next.next, "Ekor Linked List harus menunjuk ke None")


if __name__ == '__main__':
    unittest.main(verbosity=2)

