import time
import sys
import os

# Memastikan Python bisa menemukan folder src
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(root_path, 'src')
sys.path.insert(0, root_path)
sys.path.insert(0, src_path)

from data_structures.queue import Queue

def run_benchmark():
    NUM_ITEMS = 500_000 
    
    print("="*60)
    print(" BENCHMARK QUEUE (PEMBUKTIAN O(1))")
    print("="*60)
    print(f"Menguji Queue (Antrean) dengan {NUM_ITEMS:,} elemen...\n")
    
    queue = Queue()

    # Mengukur Enqueue O(1)
    start_time = time.perf_counter()
    for i in range(NUM_ITEMS):
        queue.enqueue(f"Data-{i}")
    enqueue_time = time.perf_counter() - start_time
    
    print(f"[+] Waktu Enqueue total   : {enqueue_time:.4f} detik")
    print(f"    Rata-rata per Enqueue : {(enqueue_time / NUM_ITEMS) * 1_000_000:.4f} mikrosekon\n")

    # Mengukur Dequeue O(1)
    start_time = time.perf_counter()
    while not queue.is_empty():
        queue.dequeue()
    dequeue_time = time.perf_counter() - start_time
    
    print(f"[-] Waktu Dequeue total   : {dequeue_time:.4f} detik")
    print(f"    Rata-rata per Dequeue : {(dequeue_time / NUM_ITEMS) * 1_000_000:.4f} mikrosekon")
    print("="*60)

if __name__ == "__main__":
    run_benchmark()
