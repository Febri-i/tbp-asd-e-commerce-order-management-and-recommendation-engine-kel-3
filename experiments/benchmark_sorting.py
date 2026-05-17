import time
import random
import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(root_path, 'src')
sys.path.insert(0, root_path)
sys.path.insert(0, src_path)

from data_structures.produk import Order
from data_structures.ll import LLNode

from command_processor import bubble_sort_order, insertion_sort_order 

def run_benchmark():
    NUM_ITEMS = 3000
    
    print("="*65)
    print(" BENCHMARK ALGORITMA SORTING (BUBBLE SORT vs INSERTION SORT)")
    print("="*65)
    print(f"Menyiapkan {NUM_ITEMS:,} data Order acak...\n")

    arr_orders = []
    
    # Menghasilkan data acak
    for i in range(NUM_ITEMS):
        dummy_order = Order(
            order_id=i,
            pelanggan=f"C{i:03d}",
            produk_kode=f"P{i:03d}",
            qty=1,
            tier=2,
            total_harga=random.randint(10_000, 5_000_000),
            # Acak waktu pesan dari 1 hari terakhir
            waktu_pesan=time.time() - random.randint(0, 86400) 
        )
        arr_orders.append(dummy_order)

    # Menyalin data ke dalam struktur Linked List
    head = None
    curr = None
    for order in arr_orders:
        new_node = LLNode(order)
        if head is None:
            head = new_node
            curr = head
        else:
            curr.next = new_node # type: ignore
            curr = new_node

    # BUBBLE SORT
    print(f"[1] Menguji Bubble Sort (Array) - Descending Harga")
    start_time = time.perf_counter()
    bubble_sort_order(arr_orders)
    bubble_time = time.perf_counter() - start_time
    print(f"    Waktu eksekusi : {bubble_time:.4f} detik\n")

    # INSERTION SORT
    print(f"[2] Menguji Insertion Sort (Linked List) - Ascending Waktu")
    start_time = time.perf_counter()
    sorted_head = insertion_sort_order(head) # type: ignore
    insertion_time = time.perf_counter() - start_time
    print(f"    Waktu eksekusi : {insertion_time:.4f} detik\n")

if __name__ == "__main__":
    random.seed(99)
    run_benchmark()
