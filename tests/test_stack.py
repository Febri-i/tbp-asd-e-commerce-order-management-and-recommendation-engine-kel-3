import sys
import os
import time
from dataclasses import dataclass
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data_structures.stack import Stack
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

def jalankan_test_stack():
    print("==========================================================")
    print("   UJI STACK: RIWAYAT TRANSAKSI (Maksimal 10 Data) ")
    print("==========================================================")
    
    stack_riwayat = Stack(kapasitas=10)
    
    print("[*] Pelanggan checkout 12 kali berturut-turut...")
    for i in range(1, 13): 
        order_baru = Order(i, "Faiz", f"P{i:03d}", 2, 1, 150000.0 * i, time.time())
        berhasil = stack_riwayat.push(order_baru)
        if berhasil:
            print(f"    [Tersimpan] Order ID {order_baru.order_id} - Total: Rp{order_baru.total_harga:,}")
        else:
            print(f"    [Ditolak] Order ID {order_baru.order_id} gagal masuk (Kapasitas Stack Penuh!)")
            
    print(f"\n    -> Riwayat Terakhir (Peek): Order ID {stack_riwayat.peek().order_id}")
    
    print("\n[*] Simulasi Pelanggan klik tombol UNDO_ORDER (Pop)...")
    batal = stack_riwayat.pop()
    print(f"    -> Order Dibatalkan (Pop) : Order ID {batal.order_id}")
    print(f"    -> Riwayat Terakhir Sekarang : Order ID {stack_riwayat.peek().order_id}")
    print("==========================================================\n")

if __name__ == "__main__":
    jalankan_test_stack()