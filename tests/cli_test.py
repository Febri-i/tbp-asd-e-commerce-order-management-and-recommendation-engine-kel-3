import sys
import os
import unittest

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

src_path = os.path.join(root_path, 'src')

sys.path.insert(0, root_path)
sys.path.insert(0, src_path)

from src.command_processor import (
    verify_param, ParamPattern, format_rp, get_tier_name,
    order_produk, serve, init, bst_katalog, queues, cust_stacks, order_counter, cancel_last, update_stok, undo_order
)

class TestCLIApp(unittest.TestCase):
    
    def setUp(self):
        init() 
    
    def test_format_rp(self):
        """Memastikan fungsi format mata uang berjalan benar"""
        self.assertEqual(format_rp(1500000), "Rp 1.500.000")
        self.assertEqual(format_rp(50000), "Rp 50.000")

    def test_verify_param_valid(self):
        """Memastikan validasi param bisa mendeteksi format yang BENAR"""
        params = ["C001", "P001", "PREMIUM", "2"]
        pola = [ParamPattern.STRING, ParamPattern.STRING, ParamPattern.STRING, ParamPattern.NUMBER]
        self.assertTrue(verify_param(params, pola))

    def test_verify_param_invalid(self):
        """Memastikan validasi param gagal jika diisi format yang SALAH"""
        params = ["C001", "P001", "PREMIUM", "DUA"] 
        pola = [ParamPattern.STRING, ParamPattern.STRING, ParamPattern.STRING, ParamPattern.NUMBER]
        self.assertFalse(verify_param(params, pola))
        
        self.assertFalse(verify_param(["C001"], pola))

    def test_order_produk_sukses(self):
        """Memastikan order_produk mengurangi stok dan masuk ke Queue"""
        produk_awal = bst_katalog.search("P001")

        self.assertIsNotNone(produk_awal, "Produk P001 gagal dimuat ke dalam BST")

        stok_awal = produk_awal.stok  # ty:ignore[unresolved-attribute]

        order_produk("C001", "P001", "PREMIUM", 5)
        
        self.assertEqual(produk_awal.stok, stok_awal - 5, "Stok produk tidak berkurang dengan benar")  # ty:ignore[unresolved-attribute]
        self.assertFalse(queues["PREMIUM"].is_empty(), "Queue Premium masih kosong padahal sudah ada order")

    def test_order_produk_stok_habis(self):
        """Memastikan order gagal jika jumlah melebihi stok"""
        produk_awal = bst_katalog.search("P001")
        
        self.assertIsNotNone(produk_awal, "Produk P001 gagal dimuat ke dalam BST")
        
        stok_awal = produk_awal.stok  # ty:ignore[unresolved-attribute]
        
        order_produk("C001", "P001", "REGULAR", 500)
        
        self.assertEqual(produk_awal.stok, stok_awal, "Stok ikut berkurang padahal order gagal")  # ty:ignore[unresolved-attribute]
        self.assertTrue(queues["REGULAR"].is_empty(), "Order tetap masuk queue padahal stok habis")

    def test_serve_order(self):
        """Memastikan pesanan dilayani, masuk ke stack history, dan antrean berkurang"""
        order_produk("C002", "P005", "REGULAR", 1)
        
        serve()
        
        self.assertTrue(queues["REGULAR"].is_empty())
        
        top_node = cust_stacks["C002"].top
        
        self.assertIsNotNone(top_node, "Riwayat pelanggan C002 tidak tercatat")
        
        assert top_node is not None 
        
        self.assertEqual(top_node.data.produk_kode, "P005")

    def test_cancel_last(self):
        """Memastikan CANCEL_LAST menghapus riwayat global/pelanggan dan mengembalikan stok"""

        produk_awal = bst_katalog.search("P001")
        self.assertIsNotNone(produk_awal)
        stok_awal = produk_awal.stok # type: ignore

        order_produk("C003", "P001", "PREMIUM", 3)
        serve()

        self.assertEqual(produk_awal.stok, stok_awal - 3) # type: ignore

        cancel_last()

        self.assertEqual(produk_awal.stok, stok_awal, "Stok tidak kembali setelah di-cancel") # type: ignore
        self.assertIsNone(cust_stacks["C003"].top, "Riwayat pelanggan tidak terhapus setelah cancel")


    def test_update_stok_sukses(self):
        """Memastikan UPDATE_STOK benar-benar mengubah nilai stok di BST Katalog"""

        produk_awal = bst_katalog.search("P002")
        self.assertIsNotNone(produk_awal)

        update_stok("P002", 999)

        produk_setelah_update = bst_katalog.search("P002")
        self.assertIsNotNone(produk_setelah_update)
        self.assertEqual(produk_setelah_update.stok, 999, "Stok gagal diperbarui di BST") # type: ignore


    def test_undo_order_pelanggan(self):
        """Memastikan UNDO_ORDER menghapus pesanan spesifik pelanggan dan mengembalikan stok"""

        produk_awal = bst_katalog.search("P003")
        self.assertIsNotNone(produk_awal)
        stok_awal = produk_awal.stok # type: ignore

        order_produk("C004", "P003", "REGULAR", 2)
        serve()

        undo_order("C004")

        self.assertEqual(produk_awal.stok, stok_awal, "Stok tidak kembali setelah undo_order") # type: ignore
        self.assertIsNone(cust_stacks["C004"].top, "Pesanan gagal di-undo dari stack pelanggan")

if __name__ == '__main__':
    unittest.main(verbosity=2)
