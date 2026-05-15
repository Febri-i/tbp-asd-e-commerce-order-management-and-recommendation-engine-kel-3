from os import abort
from dataclasses import dataclass, field
from typing import List, Dict
from command_processor import *

from enum import Enum, auto

class ParamPattern(Enum):
    STRING = 0
    NUMBER = 1

def verify_param(param: List[str], pattern: List[ParamPattern]) -> bool:
    if len(param) != len(pattern):
        return False
    
    for i, data in enumerate(param):
        if pattern[i] == ParamPattern.NUMBER:
            if not data.isnumeric():
                return False
        elif pattern[i] == ParamPattern.STRING:
            if not data.isalnum(): # Ganti isalpha() jadi isalnum() agar P001 / C001 lolos
                return False
                
    return True # Ganti dari False ke True (jika semua pengecekan lolos)

def process_command(input_str: str):
    tokens: List[str] = input_str.split()
    if not tokens:
        return
        
    command: str = tokens[0].upper()
    args: List[str] = tokens[1:] # Ambil parameter setelah command

    match command:
        case "BANTUAN":
            print("\n==== DAFTAR PERINTAH CLI E-COMMERCE ====")
            print("1. ORDER <cust_id> <prod_id> <tier> <qty>")
            print("   -> Memesan produk (Tier: PREMIUM, REGULAR, ECONOMY)")
            print("2. SERVE")
            print("   -> Melayani order di antrean berdasarkan prioritas tier")
            print("3. CANCEL_LAST")
            print("   -> Membatalkan pesanan terakhir yang dilayani (pop dari stack global)")
            print("4. CARI_PRODUK <kode_produk>")
            print("   -> Mencari informasi produk berdasarkan kode")
            print("5. UPDATE_STOK <kode_produk> <jumlah_baru>")
            print("   -> Mengubah jumlah stok produk tertentu")
            print("6. REKOMENDASI <kode_produk>")
            print("   -> Menampilkan rekomendasi produk berdasarkan co-purchase")
            print("7. RIWAYAT <cust_id>")
            print("   -> Menampilkan 10 riwayat pesanan terakhir dari seorang pelanggan")
            print("8. LAPORAN_HARIAN")
            print("   -> Menampilkan laporan pesanan hari ini yang diurutkan berdasarkan harga")
            print("9. UNDO_ORDER <cust_id>")
            print("   -> Membatalkan pesanan terakhir dari pelanggan tertentu")
            print("10. BANTUAN")
            print("   -> Menampilkan daftar perintah ini")
            print("11. KELUAR")
            print("   -> Keluar dari aplikasi")
            print("========================================\n")
        case "ORDER":
            # Format: ORDER <cust_id> <prod_id> <tier> <qty>
            if verify_param(args, [ParamPattern.STRING, ParamPattern.STRING, ParamPattern.STRING, ParamPattern.NUMBER]):
                print("Big-O: O(log n) untuk BST Search + O(1) untuk Queue Enqueue")
                order_produk(args[0], args[1], args[2].upper(), int(args[3]))
            else:
                print("Format salah! Gunakan: ORDER <cust_id> <prod_id> <tier> <qty>")

        case "SERVE":
            # Format: SERVE
            if verify_param(args, []):
                print("Big-O: O(1) untuk Dequeue")
                serve()
            else:
                print("Format salah! Gunakan: SERVE")

        case "CANCEL_LAST":
            # Format: CANCEL_LAST
            if verify_param(args, []):
                print("Big-O: O(1) Stack Pop + O(log n) update stok BST")
                cancel_last()
            else:
                print("Format salah! Gunakan: CANCEL_LAST")

        case "CARI_PRODUK":
            # Format: CARI_PRODUK <kode>
            if verify_param(args, [ParamPattern.STRING]):
                print("Big-O: O(log n) untuk BST Search")
                cari_produk(args[0])
            else:
                print("Format salah! Gunakan: CARI_PRODUK <kode_produk>")

        case "UPDATE_STOK":
            # Format: UPDATE_STOK <kode> <qty>
            if verify_param(args, [ParamPattern.STRING, ParamPattern.NUMBER]):
                print("Big-O: O(log n) untuk update node BST")
                update_stok(args[0], int(args[1]))
            else:
                print("Format salah! Gunakan: UPDATE_STOK <kode_produk> <jumlah>")

        case "REKOMENDASI":
            # Format: REKOMENDASI <kode>
            if verify_param(args, [ParamPattern.STRING]):
                print("Big-O: O(V + E) untuk Graph Adjacency List Traversal")
                rekomendasi(args[0])
            else:
                print("Format salah! Gunakan: REKOMENDASI <kode_produk>")

        case "RIWAYAT":
            # Format: RIWAYAT <cust_id>
            if verify_param(args, [ParamPattern.STRING]):
                print("Big-O: O(1) iterasi terbatas pada 10 node Stack teratas")
                riwayat(args[0])
            else:
                print("Format salah! Gunakan: RIWAYAT <cust_id>")

        case "LAPORAN_HARIAN":
            # Format: LAPORAN_HARIAN
            if verify_param(args, []):
                print("Big-O: O(n^2) menggunakan Linked List Insertion/Bubble Sort")
                laporan_harian()
            else:
                print("Format salah! Gunakan: LAPORAN_HARIAN")
                
        case "UNDO_ORDER":
            # Format: UNDO_ORDER <cust_id>
            if verify_param(args, [ParamPattern.STRING]):
                print("Big-O: O(1) untuk Stack Pop + O(log n) Update BST")
                undo_order(args[0])
            else:
                print("Format salah! Gunakan: UNDO_ORDER <cust_id>")

        case "KELUAR":
            print("bye!")
            exit()

        case _:
            print(f"Perintah tidak dikenali: {command}. Coba lagi.")
def main():

    init();

    print('E-Commerce Order Management Ketik BANTUAN untuk daftar perintah')
    while True:
        process_command(input("> "));

if __name__ == '__main__':
    main()
