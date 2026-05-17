import sys
import os
import time
import random
from dataclasses import dataclass
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data_structures.ll import LLNode
from data_structures.produk import Produk

@dataclass
class Order:
    order_id: int
    pelanggan: str
    produk_kode: str
    tier: int
    qty: int
    total_harga: float
    waktu_pesan: float

# A. BUBBLE SORT LINKED LIST (Ascending Waktu Pesan)
def bubble_sort_waktu(head: LLNode):
    if not head: return None
    swapped = True
    while swapped:
        swapped = False
        curr = head
        while curr.next:
            if curr.data.waktu_pesan > curr.next.data.waktu_pesan:
                curr.data, curr.next.data = curr.next.data, curr.data
                swapped = True
            curr = curr.next
    return head

# B. INSERTION SORT LINKED LIST (Ascending Waktu Pesan)
def insertion_sort_waktu(head: LLNode):
    if not head or not head.next: return head
    sorted_list = None
    curr = head
    while curr:
        next_node = curr.next
        if not sorted_list or sorted_list.data.waktu_pesan >= curr.data.waktu_pesan:
            curr.next = sorted_list
            sorted_list = curr
        else:
            search = sorted_list
            while search.next and search.next.data.waktu_pesan < curr.data.waktu_pesan:
                search = search.next
            curr.next = search.next
            search.next = curr
        curr = next_node
    return sorted_list

def buat_data_hampir_terurut(n: int) -> LLNode:
    random.seed(99)
    head = tail = None
    batas_terurut = int(n * 0.90)
    
    # 90% Data lama yang sudah terurut otomatis berdasarkan waktu
    for i in range(1, batas_terurut + 1):
        o = Order(i, "C001", "P001", 2, 1, 100000.0, float(i))
        new_node = LLNode(o)
        if not head: head = tail = new_node
        else: tail.next = new_node; tail = new_node
        
    # 10% Data order baru acak yang ditambahkan di akhir hari
    for i in range(batas_terurut + 1, n + 1):
        waktu_acak = random.uniform(1.0, float(batas_terurut))
        o = Order(i, "C001", "P001", 2, 1, 100000.0, waktu_acak)
        new_node = LLNode(o)
        tail.next = new_node; tail = new_node
        
    return head

def jalankan_eksperimen():
    print("==============================================================")
    print(" BUKTI EKSPERIMEN RUNTIME: 90%  DATA TERURUT, 10% ACak ")
    print("==============================================================")
    print("  N   | Bubble Sort (Detik) | Insertion Sort (Detik) ")
    print("--------------------------------------------------------------")
    
    for n in [50, 100, 300]:
        ll_bubble = buat_data_hampir_terurut(n)
        start_b = time.time()
        bubble_sort_waktu(ll_bubble)
        waktu_bubble = time.time() - start_b
        
        ll_insertion = buat_data_hampir_terurut(n)
        start_i = time.time()
        insertion_sort_waktu(ll_insertion)
        waktu_insertion = time.time() - start_i
        
        print(f" {n:<4} |       {waktu_bubble:.6f}      |       {waktu_insertion:.6f} ")
    print("==============================================================\n")

if __name__ == "__main__":
    jalankan_eksperimen()