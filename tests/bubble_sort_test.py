import sys
import os
import unittest

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

src_path = os.path.join(root_path, 'src')

sys.path.insert(0, root_path)
sys.path.insert(0, src_path)
from unittest.mock import Mock
from src.data_structures.linked_list import LLNode 


from modules.command_processor import bubble_sort_order

class TestBubbleSort(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_bubble_sort_order(self):
        """Memastikan bubble sort mengurutkan List/Array In-Place (descending total_harga)"""
        # Buat array berisi objek order acak
        arr_orders = [
            Mock(total_harga=150000),
            Mock(total_harga=500000),
            Mock(total_harga=50000)
        ]
        
        # Eksekusi in-place sorting
        bubble_sort_order(arr_orders)  # ty:ignore[invalid-argument-type]
        
        # Verifikasi urutan dari harga tertinggi ke terendah
        self.assertEqual(arr_orders[0].total_harga, 500000)
        self.assertEqual(arr_orders[1].total_harga, 150000)
        self.assertEqual(arr_orders[2].total_harga, 50000)


if __name__ == '__main__':
    unittest.main(verbosity=2)

