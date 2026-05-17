import time
import random
import sys
import os

# Memastikan Python bisa menemukan folder src
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(root_path, 'src')
sys.path.insert(0, root_path)
sys.path.insert(0, src_path)

from data_structures.queue import Queue
# Asumsikan GraphRekomendasi ada di src/data_structures/graph.py
# Sesuaikan import di bawah ini dengan lokasi file aslinya
from data_structures.graph import GraphRekomendasi 

def generate_dummy_data(num_products: int, num_transactions: int):
    """Menghasilkan data produk dan transaksi acak untuk pengujian."""
    products = [f"P{str(i).zfill(5)}" for i in range(num_products)]
    transactions = []
    
    for _ in range(num_transactions):
        # Pilih 2 produk acak yang dibeli bersamaan
        a, b = random.sample(products, 2)
        transactions.append((a, b))
        
    return products, transactions

def run_benchmark():
    print("="*50)
    print(" BENCHMARK GRAPH REKOMENDASI (CO-PURCHASE)")
    print("="*50)

    # 1. Konfigurasi Data (Silakan ubah angka ini untuk test lebih berat)
    NUM_PRODUCTS = 5_000      # 5 Ribu Produk
    NUM_TRANSACTIONS = 50_000 # 50 Ribu relasi co-purchase
    
    print(f"Menyiapkan {NUM_PRODUCTS:,} produk dan {NUM_TRANSACTIONS:,} transaksi acak...")
    products, transactions = generate_dummy_data(NUM_PRODUCTS, NUM_TRANSACTIONS)
    
    graph = GraphRekomendasi()

    # 2. Benchmark Insert (add_copurchase)
    print("\n[1] Menjalankan Benchmark Insert (Membangun Graf)...")
    start_time = time.perf_counter()
    
    for a, b in transactions:
        graph.add_copurchase(a, b)
        
    end_time = time.perf_counter()
    insert_duration = end_time - start_time
    print(f"Waktu Insert {NUM_TRANSACTIONS:,} relasi : {insert_duration:.4f} detik")
    print(f"Rata-rata waktu per relasi        : {(insert_duration/NUM_TRANSACTIONS)*1000:.4f} ms")

    # 3. Benchmark BFS (rekomendasikan) pada berbagai kedalaman hop
    print("\n[2] Menjalankan Benchmark Rekomendasi (BFS)...")
    
    # Ambil sampel 100 produk secara acak untuk dites
    sample_products = random.sample(products, 100)
    
    for hop in [1, 2, 3]:
        start_time = time.perf_counter()
        total_rekomendasi = 0
        
        for p in sample_products:
            hasil = graph.rekomendasikan(p, max_hop=hop)
            total_rekomendasi += len(hasil)
            
        end_time = time.perf_counter()
        bfs_duration = end_time - start_time
        
        print(f"  -> max_hop = {hop}")
        print(f"     Waktu total (100 produk)  : {bfs_duration:.4f} detik")
        print(f"     Rata-rata waktu per pencarian: {(bfs_duration/100)*1000:.4f} ms")
        print(f"     Rata-rata hasil ditemukan : {total_rekomendasi//100} produk")
        print("-" * 40)

if __name__ == "__main__":
    # Fix seed agar hasil random konsisten setiap kali script dijalankan
    random.seed(42) 
    run_benchmark()
