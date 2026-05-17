import unittest
import sys
import os

# Memastikan Python bisa menemukan folder src
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(root_path, 'src')
sys.path.insert(0, root_path)
sys.path.insert(0, src_path)

from data_structures.stack import Stack

class TestStack(unittest.TestCase):
    def setUp(self):
        """Membuat instance Stack baru sebelum setiap test."""
        # Kita pakai kapasitas kecil (misal 3) agar mudah dites batasnya
        self.stack = Stack(kapasitas=3)

    def test_inisialisasi_awal(self):
        """Memastikan stack baru benar-benar kosong."""
        self.assertIsNone(self.stack.top)
        self.assertEqual(self.stack._size, 0)
        self.assertEqual(self.stack.kapasitas, 3)
        self.assertIsNone(self.stack.peek())
        self.assertIsNone(self.stack.pop())

    def test_push_dan_peek(self):
        """Memastikan elemen baru masuk ke top (paling atas)."""
        hasil_push = self.stack.push("Riwayat 1")
        self.assertTrue(hasil_push)
        self.assertEqual(self.stack._size, 1)
        self.assertEqual(self.stack.peek(), "Riwayat 1")

        # Push lagi, harusnya menutupi yang lama
        self.stack.push("Riwayat 2")
        self.assertEqual(self.stack._size, 2)
        self.assertEqual(self.stack.peek(), "Riwayat 2", "Elemen terbaru harusnya di top")

    def test_pop_lifo_order(self):
        """Memastikan prinsip Last-In-First-Out (LIFO) berjalan benar saat pop."""
        self.stack.push("Data A")
        self.stack.push("Data B")
        self.stack.push("Data C")

        # Urutan keluar harus C -> B -> A
        self.assertEqual(self.stack.pop(), "Data C")
        self.assertEqual(self.stack._size, 2)
        
        self.assertEqual(self.stack.pop(), "Data B")
        self.assertEqual(self.stack.pop(), "Data A")
        
        # Harus kembali kosong
        self.assertEqual(self.stack._size, 0)
        self.assertIsNone(self.stack.pop())

    def test_kapasitas_penuh(self):
        """Memastikan push ditolak (mengembalikan False) jika melebihi kapasitas."""
        self.assertTrue(self.stack.push("1"))
        self.assertTrue(self.stack.push("2"))
        self.assertTrue(self.stack.push("3"))
        
        # Kapasitas harusnya penuh di sini (max 3)
        self.assertEqual(self.stack._size, 3)
        
        # Push ke-4 harus gagal
        hasil_overload = self.stack.push("4 (Harusnya Gagal)")
        self.assertFalse(hasil_overload, "Push harusnya mengembalikan False saat penuh")
        
        # Ukuran tidak boleh bertambah dan top harus tetap "3"
        self.assertEqual(self.stack._size, 3)
        self.assertEqual(self.stack.peek(), "3")

if __name__ == '__main__':
    unittest.main()
