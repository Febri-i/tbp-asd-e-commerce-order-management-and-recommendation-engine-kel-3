import unittest
import sys
import os

# Memastikan Python bisa menemukan folder src
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(root_path, 'src')
sys.path.insert(0, root_path)
sys.path.insert(0, src_path)

from data_structures.queue import Queue

class TestQueue(unittest.TestCase):
    def setUp(self):
        """Membuat antrean baru sebelum setiap test."""
        self.queue = Queue()

    def test_inisialisasi_awal(self):
        """Memastikan antrean baru benar-benar kosong dan aman."""
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(len(self.queue), 0)
        self.assertIsNone(self.queue.peek(), "Peek pada antrean kosong harusnya None")
        self.assertIsNone(self.queue.dequeue(), "Dequeue pada antrean kosong harusnya None")

    def test_enqueue_satu_elemen(self):
        """Menguji penambahan satu elemen ke dalam antrean."""
        self.queue.enqueue("Pesanan A")
        
        self.assertFalse(self.queue.is_empty())
        self.assertEqual(len(self.queue), 1)
        self.assertEqual(self.queue.peek(), "Pesanan A")

    def test_fifo_order(self):
        """Memastikan prinsip First-In First-Out (FIFO) berjalan dengan benar."""
        self.queue.enqueue("Pesanan 1")
        self.queue.enqueue("Pesanan 2")
        self.queue.enqueue("Pesanan 3")
        
        self.assertEqual(len(self.queue), 3)
        self.assertEqual(self.queue.peek(), "Pesanan 1", "Elemen paling depan harusnya Pesanan 1")
        
        # Eksekusi Dequeue dan pastikan urutannya tepat
        self.assertEqual(self.queue.dequeue(), "Pesanan 1")
        self.assertEqual(len(self.queue), 2)
        
        self.assertEqual(self.queue.dequeue(), "Pesanan 2")
        self.assertEqual(self.queue.dequeue(), "Pesanan 3")
        
        # Antrean harus kembali kosong
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(len(self.queue), 0)

    def test_kosongkan_dan_isi_ulang(self):
        """
        Memastikan state head dan tail tersetel dengan benar 
        saat antrean dikosongkan dan kemudian diisi lagi.
        """
        # Isi dan kosongkan
        self.queue.enqueue("X")
        self.queue.enqueue("Y")
        self.queue.dequeue()
        self.queue.dequeue()
        
        self.assertTrue(self.queue.is_empty())
        
        # Isi ulang
        self.queue.enqueue("Z")
        self.assertFalse(self.queue.is_empty())
        self.assertEqual(len(self.queue), 1)
        self.assertEqual(self.queue.peek(), "Z")
        self.assertEqual(self.queue.dequeue(), "Z")

    def test_operasi_campuran(self):
        """Menguji stabilitas saat enqueue dan dequeue dilakukan bergantian."""
        self.queue.enqueue("A")
        self.assertEqual(self.queue.dequeue(), "A")  # Sisa: Kosong
        
        self.queue.enqueue("B")
        self.queue.enqueue("C")
        self.assertEqual(self.queue.dequeue(), "B")  # Sisa: C
        
        self.queue.enqueue("D")                      # Sisa: C, D
        self.assertEqual(len(self.queue), 2)
        self.assertEqual(self.queue.peek(), "C")
        
        self.assertEqual(self.queue.dequeue(), "C")  # Sisa: D
        self.assertEqual(self.queue.dequeue(), "D")  # Sisa: Kosong
        
        self.assertIsNone(self.queue.dequeue())

if __name__ == '__main__':
    unittest.main(verbosity=2)
