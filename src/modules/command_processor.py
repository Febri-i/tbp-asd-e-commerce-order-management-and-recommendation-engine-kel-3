import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enum import Enum
import numpy as np, time, random
from typing import Dict, List, cast
from data_structures.produk import Produk, TIER, Order
from data_structures.bst import BSTKatalog
from data_structures.stack import Stack
from data_structures.graph import GraphRekomendasi
from data_structures.queue import Queue
from data_structures.ll import LLNode

from datetime import datetime

queues = {tier: Queue() for tier in TIER}
cust_stacks: Dict[str, Stack] = {}
bst_katalog = BSTKatalog()
graph_rek = GraphRekomendasi()
order_counter = 0
order_stack: Stack = Stack()

np.random.seed(99)
random.seed(99)
class ParamPattern(Enum):
    """
    Enumerasi untuk mendefinisikan pola atau tipe data yang diharapkan 
    dari parameter input antarmuka baris perintah (CLI).
    
    Atribut:
        STRING (int): Mewakili parameter berupa teks alfanumerik (huruf dan/atau angka).
        NUMBER (int): Mewakili parameter berupa teks numerik (hanya angka bulat).
    """
    STRING = 0
    NUMBER = 1

def verify_param(param: List[str], pattern: List[ParamPattern]) -> bool:
    """
    Memvalidasi daftar parameter input berdasarkan aturan pola yang telah ditentukan.
    
    Fungsi ini melakukan dua lapis pengecekan: 
    1. Memastikan jumlah parameter input sama persis dengan jumlah pola yang diminta.
    2. Memeriksa kesesuaian nilai (isi) dari setiap parameter terhadap pola tipe datanya 
       (isnumeric untuk pola NUMBER, isalnum untuk pola STRING).

    Args:
        param (List[str]): Daftar argumen string yang dimasukkan oleh pengguna melalui CLI.
        pattern (List[ParamPattern]): Daftar pola referensi tipe data yang diharapkan.

    Returns:
        bool: True jika seluruh parameter valid dan sesuai dengan pola. 
              False jika jumlah parameter tidak sesuai, atau terdapat parameter 
              yang gagal memenuhi syarat tipe datanya.
    """
    if len(param) != len(pattern):
        return False
    
    for i, data in enumerate(param):
        if pattern[i] == ParamPattern.NUMBER:
            if not data.isnumeric():
                return False
        elif pattern[i] == ParamPattern.STRING:
            # Menggunakan isalnum() agar dapat menerima gabungan huruf dan angka
            # Contoh input yang valid: 'P001', 'C001', 'PREMIUM'
            if not data.isalnum(): 
                return False
                
    return True

def generate_produk(n=100) -> List[Produk]:
    """
    Menghasilkan data dummy produk dengan spesifikasi atribut acak untuk keperluan inisialisasi.

    Args:
        n (int): Jumlah data produk yang akan dihasilkan. Default bernilai 100.

    Returns:
        List[Produk]: Daftar objek Produk yang berisi kode, nama, harga, dan jumlah stok.
    """
    nama_template = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headset',
    'Webcam', 'USB Hub', 'Charger', 'Kabel HDMI', 'Speaker']
    produk_list = []
    for i in range(1, n + 1):
        kode = f'P{i:03d}'
        nama = f'{random.choice(nama_template)} Model-{i}'
        harga = round(random.uniform(50_000, 5_000_000), -3)
        stok = random.randint(0, 200)
        produk_list.append(Produk(kode, nama, harga, stok))
    return produk_list

def init():
    """
    Melakukan inisialisasi status awal sistem. Memasukkan data produk dummy ke dalam 
    Binary Search Tree (BST) katalog dan menyiapkan stack kosong untuk riwayat transaksi masing-masing pelanggan.
    """
    for p in generate_produk(100):
        bst_katalog.insert(p)

    for i in range(1, 51):
        cust_id = f'C{i:03d}'
        cust_stacks[cust_id] = Stack()

    for tier in ["PREMIUM", "REGULAR", "ECONOMY"]:
        while not queues[tier].is_empty():
            queues[tier].dequeue()

def is_today(timestamp):
    """
    Memeriksa apakah sebuah UNIX timestamp merujuk pada tanggal sistem hari ini.

    Args:
        timestamp (float): Nilai waktu dalam format UNIX timestamp.

    Returns:
        bool: Mengembalikan True jika timestamp sama dengan tanggal hari ini, False jika tidak.
    """
    return datetime.fromtimestamp(timestamp).date() == datetime.now().date()

def sorted_insert_order(new_node: LLNode, sorted_head: LLNode | None):
    """
    Menyisipkan sebuah node Linked List secara terurut ke dalam Linked List 
    berdasarkan parameter waktu pemesanan (ascending).

    Args:
        new_node (LLNode): Node Linked List baru yang berisi objek Order.
        sorted_head (LLNode | None): Referensi ke head dari Linked List yang sudah terurut.

    Returns:
        LLNode: Head dari Linked List yang telah diperbarui.
    """
    if sorted_head is None or cast(Order, new_node.data).waktu_pesan <= cast(Order, sorted_head.data).waktu_pesan:
        new_node.next = sorted_head
        return new_node
    
    else:
        curr = sorted_head
        while curr.next is not None and cast(Order, curr.next.data).waktu_pesan < cast(Order, new_node.data).waktu_pesan:
            curr = curr.next
            
        new_node.next = curr.next
        curr.next = new_node
        
        return sorted_head

def insertion_sort_order(head: LLNode):
    """
    Menerapkan algoritma Insertion Sort untuk mengurutkan data bertipe Linked List 
    berdasarkan parameter waktu pesanan (ascending).

    Args:
        head (LLNode): Referensi head dari Linked List yang belum terurut.

    Returns:
        LLNode: Head dari Linked List yang sudah diurutkan.
    """
    sorted_head = None
    curr = head
    
    while curr is not None:
        next_node = curr.next
        sorted_head = sorted_insert_order(curr, sorted_head)
        curr = next_node
        
    return sorted_head

def bubble_sort_order(arr: List[Order]):
    """
    Menerapkan algoritma Bubble Sort secara in-place untuk mengurutkan array berisi objek Order 
    berdasarkan total harga (descending).

    Args:
        arr (List[Order]): Array atau list berisi data transaksi yang akan diurutkan.
    """
    n = len(arr)
    
    for i in range(n):
        swapped = False

        for j in range(0, n-i-1):
            if arr[j].total_harga < arr[j+1].total_harga:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if (swapped == False):
            break

def format_rp(v):
    """
    Memformat representasi angka menjadi string format mata uang Rupiah standar.

    Args:
        v (float | int): Nilai nominal yang akan diformat.

    Returns:
        str: Hasil format mata uang (contoh: "Rp 1.000.000").
    """
    return f"Rp {v:,.0f}".replace(",", ".")

def get_tier_name(tier_id: int):
    """
    Mengonversi identifier numerik tier antrean menjadi representasi string.

    Args:
        tier_id (int): Identifier numerik tier (contoh: 1, 2, 3).

    Returns:
        str: Nama representatif tier (contoh: "PREMIUM", "REGULAR", "ECONOMY").
    """
    mapping = {1: "PREMIUM", 2: "REGULAR", 3: "ECONOMY"}
    return mapping.get(tier_id, "UNKNOWN")

def order_produk(customer_id: str, produk_id: str, tier: str, quantity: int):
    """
    Memvalidasi dan memproses inisiasi order baru. Jika validasi lolos, stok produk dikurangi 
    dan data order dimasukkan ke dalam antrean (Queue) sesuai tingkatan tier yang diminta.

    Args:
        customer_id (str): Identifier unik pelanggan.
        produk_id (str): Identifier unik produk dari katalog.
        tier (str): Nama tier untuk menentukan prioritas antrean.
        quantity (int): Kuantitas produk yang akan dipesan.
    """
    global order_counter
    
    if tier not in TIER:
        print(f"[!] Gagal: Tier '{tier}' tidak valid.")
        return
    if customer_id not in cust_stacks:
        print(f"[!] Gagal: Customer '{customer_id}' tidak ditemukan.")
        return
        
    produk = bst_katalog.search(produk_id)
    if not produk: 
        print(f"[!] Gagal: Produk '{produk_id}' tidak ditemukan.")
        return
    if produk.stok < quantity:
        print(f"[!] Gagal: Stok tidak mencukupi (Tersisa: {produk.stok}).")
        return

    produk.stok -= quantity
    total = produk.harga * quantity
    
    new_order = Order(
        order_id=order_counter,
        pelanggan=customer_id,
        produk_kode=produk_id, 
        qty=quantity,
        tier=TIER[tier],
        total_harga=total,
        waktu_pesan=time.time()
    )

    queues[tier].enqueue(new_order)
    order_counter += 1
    
    print(f"[✓] Order Berhasil Dibuat!")
    print(f"    ID: {new_order.order_id} | {customer_id} memesan {quantity}x {produk.nama}")
    print(f"    Total: {format_rp(total)} ({tier})")

def serve():
    """
    Mengeksekusi proses dequeuing berdasarkan prioritas antrean (PREMIUM -> REGULAR -> ECONOMY). 
    Fungsi ini juga akan memetakan data transaksi (co-purchase) ke dalam Graph rekomendasi 
    serta memasukkan transaksi ke stack global maupun stack spesifik pelanggan.
    """
    served: Order | None = None
    if not (queues['PREMIUM'].is_empty()):
        served = queues['PREMIUM'].dequeue()
    elif not (queues['REGULAR'].is_empty()):
        served = queues['REGULAR'].dequeue()
    elif not (queues['ECONOMY'].is_empty()):
        served = queues['ECONOMY'].dequeue()

    if served is None:
        print("[!] Antrean kosong. Tidak ada pesanan untuk dilayani.")
        return

    produk = bst_katalog.search(served.produk_kode)
    nama_produk = produk.nama if produk else "Produk Tidak Diketahui"

    print("\n" + "="*30)
    print("      MELAYANI PESANAN")
    print("="*30)
    print(f"Order ID     : {served.order_id}")
    print(f"Pelanggan    : {served.pelanggan}")
    print(f"Tier         : {get_tier_name(served.tier)}")
    print(f"Produk       : {served.produk_kode} - {nama_produk}")
    print(f"Jumlah       : {served.qty}")
    print(f"Total Bayar  : {format_rp(served.total_harga)}")
    print("="*30 + "\n")

    prev_node = cust_stacks[served.pelanggan].top
    if prev_node and prev_node.data:
        graph_rek.add_copurchase(prev_node.data.produk_kode, served.produk_kode)

    cust_stacks[served.pelanggan].push(served)
    order_stack.push(served)

def cancel_last():
    """
    Membatalkan eksekusi layanan pesanan terakhir yang dicatat dalam sistem secara global. 
    Menghapus data pesanan dari stack global, stack historis pelanggan, 
    dan melakukan pemulihan jumlah stok pada katalog (BST).
    """
    last_order: Order | None = order_stack.pop()
    if not last_order:
        print("[!] Tidak ada riwayat pelayanan untuk di-cancel.")
        return

    cust_stacks[last_order.pelanggan].pop()
    bst_katalog.update_stok(last_order.produk_kode, last_order.qty)
    
    print(f"[!] CANCEL BERHASIL: Pesanan #{last_order.order_id} dibatalkan.")
    print(f"    Stok {last_order.produk_kode} telah dikembalikan (+{last_order.qty}).")

def cari_produk(kode: str):
    """
    Mengeksekusi query pencarian data produk menggunakan kode produk di dalam 
    Binary Search Tree (BST) dan merender hasil pencarian ke terminal.

    Args:
        kode (str): Identifier kode produk (contoh: 'P001').
    """
    result: Produk | None = bst_katalog.search(kode)
    if not result:
        print(f"[!] Produk {kode} tidak ditemukan di katalog.")
        return

    print("\n" + "╔" + "═"*35 + "╗")
    print(f"║        INFORMASI PRODUK           ")
    print("╠" + "═"*35 + "╣")
    print(f"║ Kode  : {result.kode:<25} ║")
    print(f"║ Nama  : {result.nama[:25]:<25} ║")
    print(f"║ Harga : {format_rp(result.harga):<25} ║")
    print(f"║ Stok  : {result.stok:<25} ║")
    print("╚" + "═"*35 + "╝")

def rekomendasi(kode: str):
    """
    Menganalisis relasi antar produk (co-purchase) yang ada pada Graph Rekomendasi, 
    lalu mencetak daftar produk yang berpotensi relevan bagi pelanggan yang membeli produk tersebut.

    Args:
        kode (str): Identifier kode produk sebagai node asal pencarian.
    """
    rekomendasi_list = graph_rek.rekomendasikan(kode)
    if not rekomendasi_list:
        print(f"[i] Belum ada pola pembelian untuk produk {kode}.")
        return
        
    print(f"\n[★] Pelanggan yang membeli {kode} juga membeli:")
    for p_id in rekomendasi_list:
        p = bst_katalog.search(p_id)
        nama = p.nama if p else "???"
        print(f"    > {p_id} - {nama}")

def riwayat(cust_id: str):
    """
    Melakukan iterasi pada Stack milik pelanggan tertentu untuk menampilkan 
    10 transaksi terakhir yang dilayani oleh sistem.

    Args:
        cust_id (str): Identifier pelanggan yang dicari riwayatnya.
    """
    if cust_id not in cust_stacks:
        print(f"[!] Customer {cust_id} tidak terdaftar.")
        return

    curr = cust_stacks[cust_id].top
    print(f"\n--- 10 Transaksi Terakhir: {cust_id} ---")
    
    count = 0
    while curr and count < 10:
        ord_data: Order = curr.data
        p = bst_katalog.search(ord_data.produk_kode)
        nama = p.nama if p else "???"
        
        print(f"#{ord_data.order_id:03} | {nama[:15]:<15} | {ord_data.qty}x | {format_rp(ord_data.total_harga)}")
        curr = curr.next
        count += 1
    
    if count == 0:
        print("    Belum ada riwayat transaksi.")

def laporan_harian():
    """
    Menghasilkan dan menampilkan laporan agregat seluruh transaksi harian. Laporan dicetak 
    dalam dua mode: (1) Diurutkan berdasarkan kronologi menggunakan Insertion Sort pada Linked List; 
    (2) Diurutkan secara descending berdasarkan nilai transaksi menggunakan Bubble Sort pada tipe data Array.
    """
    node = order_stack.top
    if not node:
        print("[!] Belum ada pesanan yang dilayani.")
        return

    laporan_hari_ini_arr: List[Order] = []
    head_waktu: LLNode = node
    
    curr = node
    while curr is not None:
        order: Order = curr.data
        if is_today(order.waktu_pesan):
            laporan_hari_ini_arr.append(order)
            
            new_node = LLNode(order)
            new_node.next = head_waktu
            head_waktu = new_node
            
        curr = curr.next

    if len(laporan_hari_ini_arr) == 0:
        print("[!] Belum ada pesanan yang dilayani hari ini.")
        return

    sorted_waktu_head = insertion_sort_order(head_waktu)
    
    print(f"\n{'='*65}")
    print(f"{'LAPORAN TRANSAKSI HARIAN (Diurutkan per Waktu Pemesanan)':^65}")
    print(f"{datetime.now().strftime('%d %B %Y'):^65}")
    print(f"{'='*65}")
    print(f"{'ID':<5} | {'Produk':<10} | {'Qty':<4} | {'Total':<14} | {'Waktu'}")
    print(f"{'-'*65}")

    curr_waktu = sorted_waktu_head
    while curr_waktu:
        ord_data: Order = curr_waktu.data
        waktu_str = datetime.fromtimestamp(ord_data.waktu_pesan).strftime('%H:%M:%S')
        print(f"{ord_data.order_id:<5} | {ord_data.produk_kode:<10} | {ord_data.qty:<4} | {format_rp(ord_data.total_harga):<14} | {waktu_str}")
        curr_waktu = curr_waktu.next
    print(f"{'='*65}\n")


    bubble_sort_order(laporan_hari_ini_arr)
    
    print(f"{'='*65}")
    print(f"{'LAPORAN TRANSAKSI HARIAN (Diurutkan per Harga Termahal)':^65}")
    print(f"{datetime.now().strftime('%d %B %Y'):^65}")
    print(f"{'='*65}")
    print(f"{'ID':<5} | {'Produk':<10} | {'Qty':<4} | {'Total':<14} | {'Waktu'}")
    print(f"{'-'*65}")

    total_omzet = 0
    for ord_data in laporan_hari_ini_arr:
        waktu_str = datetime.fromtimestamp(ord_data.waktu_pesan).strftime('%H:%M:%S')
        print(f"{ord_data.order_id:<5} | {ord_data.produk_kode:<10} | {ord_data.qty:<4} | {format_rp(ord_data.total_harga):<14} | {waktu_str}")
        total_omzet += ord_data.total_harga

    print(f"{'-'*65}")
    print(f"TOTAL TRANSAKSI : {len(laporan_hari_ini_arr)}")
    print(f"TOTAL OMZET     : {format_rp(total_omzet)}")
    print(f"{'='*65}\n")

def undo_order(cust_id: str):
    """
    Melakukan operasi rollback spesifik terhadap satu pesanan terakhir yang dimiliki 
    oleh pelanggan tertentu. Mengeluarkan elemen dari stack pelanggan tersebut dan 
    merestorasi nilai stok produk yang bersangkutan.

    Args:
        cust_id (str): Identifier unik pelanggan yang transaksinya akan dibatalkan.
    """
    if cust_id not in cust_stacks:
        print(f"[!] Gagal: Customer {cust_id} tidak ditemukan.")
        return
    
    order: Order | None = cust_stacks[cust_id].pop()
    if not order:
        print(f"[!] Gagal: {cust_id} tidak memiliki riwayat pesanan.")
        return

    bst_katalog.update_stok(order.produk_kode, order.qty)
    print(f"[✓] Undo Berhasil: Pesanan #{order.order_id} milik {cust_id} telah dihapus.")


def update_stok(kode: str, quantity: int):
    """
    Memperbarui atau menetapkan ulang jumlah stok dari suatu produk 
    di dalam katalog (Binary Search Tree).

    Args:
        kode (str): Identifier unik produk yang ingin diubah stoknya (contoh: 'P001').
        quantity (int): Jumlah stok absolut yang baru untuk produk tersebut.
    """
    result: Produk | None = bst_katalog.search(kode)

    if not result:
        print(f"[!] Gagal: Produk dengan kode '{kode}' tidak ditemukan di katalog.")
        return

    stok_lama = result.stok
    
    result.stok = quantity
    
    print("\n" + "-"*40)
    print(f"{'UPDATE STOK BERHASIL':^40}")
    print("-"*40)
    print(f" Produk    : {result.kode} - {result.nama[:20]}")
    print(f" Stok Lama : {stok_lama}")
    print(f" Stok Baru : {result.stok}  <-- (Telah Diperbarui)")
    print("-"*40 + "\n")
