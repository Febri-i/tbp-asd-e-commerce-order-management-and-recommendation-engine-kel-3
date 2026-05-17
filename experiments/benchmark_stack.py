import time
import sys
import os

# Memastikan Python bisa menemukan folder src
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(root_path, 'src')
sys.path.insert(0, root_path)
sys.path.insert(0, src_path)

from data_structures.stack import Stack

def run_benchmark():
    NUM_ITEMS = 500_000 
    
    print("="*60)
    print(" BENCHMARK STACK (PEMBUKTIAN O(1))")
    print("="*60)
    print(f"Menguji Stack (Tumpukan) dengan {NUM_ITEMS:,} elemen...\n")
    
    # Kapasitas disesuaikan dengan NUM_ITEMS agar data tidak ditolak
    stack = Stack(kapasitas=NUM_ITEMS)

    # Mengukur Push O(1)
    start_time = time.perf_counter()
    for i in range(NUM_ITEMS):
        stack.push(f"Data-{i}")
    push_time = time.perf_counter() - start_time
    
    print(f"[+] Waktu Push total      : {push_time:.4f} detik")
    print(f"    Rata-rata per Push    : {(push_time / NUM_ITEMS) * 1_000_000:.4f} mikrosekon\n")

    # Mengukur Pop O(1)
    start_time = time.perf_counter()
    while stack.peek() is not None:
        stack.pop()
    pop_time = time.perf_counter() - start_time
    
    print(f"[-] Waktu Pop total       : {pop_time:.4f} detik")
    print(f"    Rata-rata per Pop     : {(pop_time / NUM_ITEMS) * 1_000_000:.4f} mikrosekon")
    print("="*60)

if __name__ == "__main__":
    run_benchmark()
