import time
import random
import sys
import os

# Memastikan Python bisa menemukan folder src
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(root_path, 'src')
sys.path.insert(0, root_path)
sys.path.insert(0, src_path)

# Menggunakan mock/dummy class Produk jika belum ada
try:
    from data_structures.produk import Produk
except ImportError:
    class Produk:
        """Dummy class Produk untuk keperluan benchmark"""
        def __init__(self, kode: str, nama: str, harga: int, stok: int):
            self.kode = kode
            self.nama = nama
            self.harga = harga
            self.stok = stok

from data_structures.bst import BSTKatalog  # Sesuaikan dengan nama file aslimu

def generate_dummy_products(num_items: int) -> list[Produk]:
    """Menghasilkan list produk dengan kode acak."""
    products = []
    # Membuat list kode unik
    kodes = random.sample(range(1, num_items * 10), num_items)
    for kode_int in kodes:
        kode_str = f"PRD-{str(kode_int).zfill(6)}"
        products.append(Produk(kode=kode_str, nama="Produk Test", harga=10000, stok=50))
    return products

def run_benchmark():
    print("="*60)
    print(" BENCHMARK BST KATALOG (BINARY SEARCH TREE)")
    print("="*60)

    # Naikkan recursion limit karena worst-case BST bisa sangat dalam (O(n))
    sys.setrecursionlimit(20000)

    NUM_ITEMS = 10_000  # 10 Ribu Produk

    print(f"Menyiapkan {NUM_ITEMS:,} data produk dummy...\n")
    data_acak = generate_dummy_products(NUM_ITEMS)
    
    # Data urut untuk mendemonstrasikan Worst Case O(n)
    data_urut = sorted(data_acak, key=lambda p: p.kode)
    
    bst_acak = BSTKatalog()
    bst_urut = BSTKatalog()

    print("[1] Menguji Performa Insert (Kasus Acak vs Terburuk)")
    
    # Kasus Acak (Pohon Seimbang / O(log n))
    start_time = time.perf_counter()
    for p in data_acak:
        bst_acak.insert(p)  # ty:ignore[invalid-argument-type]
    waktu_insert_acak = time.perf_counter() - start_time
    print(f"  -> Insert Data Acak (O(log n)) : {waktu_insert_acak:.4f} detik")

    # Kasus Terburuk (Data sudah urut, BST jadi Linked List / O(n))
    start_time = time.perf_counter()
    for p in data_urut:
        bst_urut.insert(p)  # ty:ignore[invalid-argument-type]
    waktu_insert_urut = time.perf_counter() - start_time
    print(f"  -> Insert Data Urut (O(n))     : {waktu_insert_urut:.4f} detik")
    print(f"     (Worst case lebih lambat {waktu_insert_urut / waktu_insert_acak:.1f}x lipat!)\n")

    # Benchmark search & update stok (o(LOG N))
    print("[2] Menguji Performa Search & Update Stok")
    sample_kodes = [p.kode for p in random.sample(data_acak, 1000)] # Ambil 1000 sampel acak

    start_time = time.perf_counter()
    for kode in sample_kodes:
        bst_acak.search(kode)
        bst_acak.update_stok(kode, -1)
    waktu_search = time.perf_counter() - start_time
    
    print(f"  -> Waktu total mencari & update 1.000 produk : {waktu_search:.4f} detik")
    print(f"  -> Rata-rata waktu per produk                : {(waktu_search/1000)*1000:.4f} ms\n")

    # benchmark traversal inorder (o(N))
    print("[3] Menguji Performa Inorder Traversal (Menampilkan semua data)")
    start_time = time.perf_counter()
    hasil_inorder = bst_acak.inorder()
    waktu_inorder = time.perf_counter() - start_time
    
    print(f"  -> Waktu Inorder {len(hasil_inorder):,} produk : {waktu_inorder:.4f} detik\n")

    # benchmark delete (o(LOG N))
    print("[4] Menguji Performa Delete")
    start_time = time.perf_counter()
    for kode in sample_kodes:
        bst_acak.delete(kode)
    waktu_delete = time.perf_counter() - start_time
    
    print(f"  -> Waktu menghapus 1.000 produk secara acak : {waktu_delete:.4f} detik")
    print(f"  -> Sisa produk di Katalog BST               : {len(bst_acak):,}")
    print("="*60)

if __name__ == "__main__":
    random.seed(42)
    run_benchmark()
