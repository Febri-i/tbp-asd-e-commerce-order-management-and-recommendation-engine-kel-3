from typing import Dict, List
from data_structures.produk import Produk, TIER, Order
from data_structures.bst import BSTKatalog
from data_structures.stack import Stack
from data_structures.graph import GraphRekomendasi
from data_structures.queue import Queue

from datetime import datetime

queues = {tier: Queue() for tier in TIER}
cust_stacks: Dict[str, Stack] = {}
bst_katalog = BSTKatalog()
graph_rek = GraphRekomendasi()
order_counter = 0
order_stack: Stack = Stack();


import numpy as np, time, random

np.random.seed(99)
random.seed(99)

def generate_produk(n=100) -> List[Produk]:
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
    for p in generate_produk(100):
        bst_katalog.insert(p)

    for i in range(1, 51):
        cust_id = f'C{i:03d}'
        cust_stacks[cust_id] = Stack() # Buat stack kosong untuk tiap customer

def order_produk(customer_id: str, produk_id: str,  tier: str, quantity: int):
    global cust_stacks
    global bst_katalog
    global TIER
    global order_counter
    global queues

    if tier not in TIER:
        print(f"Invalid syntax: tier \"{tier}\" is not available.");
        return;
    if customer_id not in cust_stacks:
        print(f"Error: customer with id \"{customer_id}\" is not available.")
        return;
    produk = bst_katalog.search(produk_id)
    if not produk: 
        print(f"Error: product with id \"{produk_id}\" is not available.")
        return;
    if(produk.stok < 1):
        print(f"Error: Stok produk habis.")
        return;

    produk.stok -= quantity;

    queues[tier].enqueue(Order(order_id=order_counter,
                               pelanggan=customer_id,
                               produk_kode=produk_id, 
                               qty= quantity,
                               tier=TIER[tier],
                               total_harga=produk.harga * quantity,
                               waktu_pesan=time.time()));

    order_counter += 1;

def serve():
    global queues
    served: Order | None = None;
    if not (queues['PREMIUM'].is_empty()):
        served:Order = queues['PREMIUM'].dequeue()
    elif not (queues['REGULAR'].is_empty()):
        served:Order = queues['REGULAR'].dequeue();
    elif not (queues['ECONOMY'].is_empty()):
        served:Order = queues['ECONOMY'].dequeue();

    if(served == None):
        print("Tidak ada lagi antrean.");
        return;

    print("\n==== Melayani =====");
    print(f"Order ID: {served.order_id}");
    print(f"Customer ID: {served.pelanggan}");
    print(f"Jumlah: {served.qty}");
    print(f"Total Harga: {served.total_harga}");
    print("=====================\n");

    prev_transaction_node = cust_stacks[served.pelanggan].top
    if prev_transaction_node:
        prev_order :Order|None= prev_transaction_node.data
        if prev_order:
            graph_rek.add_copurchase(prev_order.produk_kode, served.produk_kode)

    cust_stacks[served.pelanggan].push(served);
    order_stack.push(served);

 
def cancel_last():
    last_order: Order | None = order_stack.pop();
    if not (last_order):
        print("Tidak ada lagi order.");
        return;

    canceled: Order = cust_stacks[last_order.pelanggan].pop();
    bst_katalog.update_stok(last_order.produk_kode, last_order.qty);
    print(f"Cancel order id: {canceled.order_id}")

def cari_produk(kode: str):
    result: Produk|None = bst_katalog.search(kode);
    if not result:
        print("Produk tidak ditemukan.")
        return;

    print("======= INFORMASI PRODUK =======")
    print(f"Nama: {result.nama}");
    print(f"Harga: {result.harga}");
    print(f"Stok: {result.stok}");
    print(f"Kode: {result.kode}");
    print("================================")

def update_stok(kode: str, quantity: int):
    result: Produk| None = bst_katalog.search(kode)
    if not result:
        print("Produk tidak ditemukan.")
        return;

    result.stok = quantity;

def rekomendasi(kode:str):
    rekomendasi = graph_rek.rekomendasikan(kode);
    if(len(rekomendasi) < 1):
        print("Tidak ada rekomendasi.")
        return
    print("Rekomendasi produk:")
    for produk_id in rekomendasi :
        produk = bst_katalog.search(produk_id);
        if not produk:
            continue

        print(f"- {produk.kode}: {produk.nama}")
        

def riwayat(cust_id: str):
    if cust_id not in cust_stacks:
        print("Costumer tidak ditemukan.")
        return;

    current_order = cust_stacks[cust_id].top;

    for _ in range(10):
        if not current_order:
            return;
        order: Order | None = current_order.data;

        if not (order):
            return;

        print(f"- {order.order_id}: {order.produk_kode}");
        print(f"\tJumlah: {order.qty} Harga: {order.total_harga}")
        current_order = current_order.next;


def is_today(timestamp):
    return datetime.fromtimestamp(timestamp).date() == datetime.now().date()

def laporan_harian():
    latest = order_stack.top;
    if not latest:
        print("Belum ada order!!");
        return;


    # TODO: Sort.

    while latest is not None:
        order:Order|None = latest.data
        if not order:
            break;

        if not is_today(order.waktu_pesan):
            return;

        print(f"- {order.order_id}: {order.produk_kode}")
        print(f"\tWaktu pesan: {datetime.fromtimestamp(order.waktu_pesan).strftime('%Y-%m-%d %H:%M:%S')}")

        latest = latest.next;

def undo_order(cust_id: str):
    if cust_id not in cust_stacks:
        print("Costumer tidak ditemukan.")
        return;
    
    order: Order | None = cust_stacks[cust_id].pop();

    if not order:
        print("Costumer belum order.");
        return;

    bst_katalog.update_stok(order.produk_kode, order.qty);
    print(f"Undo order #{order.order_id}");
