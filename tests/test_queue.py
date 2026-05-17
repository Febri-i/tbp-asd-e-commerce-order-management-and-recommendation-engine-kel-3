import sys
import os
import time
from dataclasses import dataclass
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data_structures.queue import Queue
from data_structures.produk import Produk
@dataclass
class Order:
    order_id: int
    pelanggan: str
    produk_kode: str
    tier: int # 1=PREMIUM, 2=REGULAR, 3=ECONOMY
    qty: int
    total_harga: float
    waktu_pesan: float

def jalankan_test_queue():
    print("==========================================================")
    print("   UJI QUEUE: ANTREAN ORDER E-COMMERCE ")
    print("==========================================================")
    
    queue_premium = Queue()
    
    # Bikin pesanan simulasi
    order1 = Order(1, "Faiz", "P005", 1, 1, 5000000.0, time.time())
    order2 = Order(2, "Rizky", "P012", 1, 2, 300000.0, time.time() + 1)
    
    print("[*] Menambahkan Order ke Antrean (Enqueue)...")
    queue_premium.enqueue(order1)
    queue_premium.enqueue(order2)
    
    print(f"    -> Total Antrean: {len(queue_premium)}")
    print(f"    -> Antrean Terdepan (Peek) : Order ID {queue_premium.peek().order_id} atas nama {queue_premium.peek().pelanggan}")
    
    print("\n[*] Memproses Antrean Terdepan (Dequeue)...")
    proses = queue_premium.dequeue()
    print(f"    -> Order Selesai Diproses: ID {proses.order_id} senilai Rp{proses.total_harga:,}")
    print(f"    -> Sisa Antrean  : {len(queue_premium)}")
    print("==========================================================\n")

if __name__ == "__main__":
    jalankan_test_queue()