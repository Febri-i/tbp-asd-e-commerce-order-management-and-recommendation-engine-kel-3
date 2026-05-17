# E-Commerce Order Management & Recommendation Engine
**Topik 3 - Algoritma dan Struktur Data (ELT60213)**
**Tahun Ajaran 2025/2026**

## 📝 Deskripsi Proyek
Proyek ini mensimulasikan sistem manajemen pesanan dan mesin rekomendasi untuk platform belanja online. Sistem ini mencakup manajemen antrian pesanan berdasarkan tier prioritas pelanggan, katalog produk yang dapat dicari dengan cepat, riwayat transaksi per pelanggan, serta sistem rekomendasi produk berbasis pola pembelian bersama (*co-purchase*). 

Projek ini dibangun menggunakan Python 3.12.

## 👥 Anggota Kelompok & Pembagian Tugas

| Nama Anggota | NIM | Modul / Tugas |
| :--- | :--- | :--- |
| **Febri Bayu Nurcahyo** | 25051030018 | Multi-Priority Order Queue, Sorting Laporan Harian, dan Integrasi CLI |
| **Faiz Nabiel Mahendra** | 25051030015 | BST Katalog Produk (Insert, Search, Delete) |
| **Muhammad Zidane Wibowo** | 25051030021 | Graph Rekomendasi |
| **Rifan Dwi Pangestu** | 25051030020 | Stack Riwayat Transaksi & Undo System |
| **Abdullah Taqiyuddin Al Fatih** | 25051030015 | Laporan |

## 🚀 Fitur Utama & Struktur Data
Sistem ini mengintegrasikan 5 struktur data utama:
1.  **Multi-tier Order Queue**: Menggunakan 3 Queue berbasis Linked List untuk melayani tier PREMIUM, REGULAR, dan ECONOMY.
2.  **BST Katalog Produk**: Mengelola 100 produk (P001-P100) dengan pencarian $O(\log n)$ rata-rata.
3.  **Graph Produk**: Memodelkan hubungan *co-purchase* antar produk menggunakan BFS (hop $\le 2$) untuk rekomendasi.
4.  **Stack Riwayat**: Menyimpan maksimal 10 transaksi terakhir per pelanggan untuk fitur *undo*.
5.  **Sorting Modul**: Mengurutkan laporan harian menggunakan Bubble Sort dan Insertion Sort pada Linked List.

## 💻 Cara Menjalankan
Pastikan Anda telah menginstal **Python 3.12** atau versi terbaru.

1. **Clone Repositori**:
   ```bash
   git clone https://github.com/username/tbp-asd-e-commerce-order-management-and-recommendation-engine-kel-3.git
   cd tbp-asd-e-commerce-order-management-and-recommendation-engine-kel-3
   ```

2. **Jalankan Aplikasi (CLI)**:
   ```bash
   python src/main.py
   ```

3. **Menjalankan Unit Test**:
   ```bash
   pytest tests/ -v
   ```

## 📋 Daftar Perintah CLI (Skenario Uji)
Sistem berjalan secara interaktif melalui CLI dengan perintah berikut:

| Perintah | Deskripsi | 
| :--- | :--- | 
| `ORDER` | Menambah pesanan baru ke antrian |
| `SERVE` | Memproses pesanan prioritas tertinggi | 
| `CANCEL_LAST` | Membatalkan pesanan terakhir |
| `CARI_PRODUK`| Mencari detail produk di BST |
| `REKOMENDASI`| Rekomendasi produk berbasis Graph/BFS |
| `RIWAYAT` | Menampilkan 10 transaksi terakhir user |
| `LAPORAN_HARIAN` | Menampilkan urutan order selesai |

## 📋 Contoh Input dan Output
### ORDER
> `ORDER <customer_id> <product_id> <tier> <quantity>`

input:
```
ORDER C001 P005 PREMIUM 10
```
output:
```
Big-O: O(log n) untuk BST Search + O(1) untuk Queue Enqueue
[✓] Order Berhasil Dibuat!
    ID: 0 | C001 memesan 10x Mouse Model-5
    Total: Rp 46.950.000 (PREMIUM)
```

### SERVE
> `SERVE`

input:
```
SERVE
```
output:
```
Big-O: O(1) untuk Dequeue

==============================
      MELAYANI PESANAN
==============================
Order ID     : 0
Pelanggan    : C001
Tier         : PREMIUM
Produk       : P005 - Mouse Model-5
Jumlah       : 10
Total Bayar  : Rp 46.950.000
==============================
```

### CANCEL_LAST
> `CANCEL_LAST`

input:
```
CANCEL_LAST
```

output:
```
Big-O: O(1) Stack Pop + O(log n) update stok BST
[!] CANCEL BERHASIL: Pesanan #0 dibatalkan.
    Stok P005 telah dikembalikan (+10).
```

### CARI_PRODUK
> `CARI_PRODUK <product_id>`

input:
```
CARI_PRODUK P004
```

output:
```
╔═══════════════════════════════════╗
║        INFORMASI PRODUK           ║
╠═══════════════════════════════════╣
║ Kode  : P004                      ║
║ Nama  : Kabel HDMI Model-4        ║
║ Harga : Rp 3.437.000              ║
║ Stok  : 137                       ║
╚═══════════════════════════════════╝
```

### REKOMENDASI
> `REKOMENDASI <product_id>`

input:
```
REKOMENDASI P005
```

output:
```
Big-O: O(V + E) untuk Graph Adjacency List Traversal

[★] Pelanggan yang membeli P005 juga membeli:
    > P004 - Kabel HDMI Model-4
```

### RIWAYAT
> `RIWAYAT <customer_id>`

input:
```
RIWAYAT C001
```

output:
```
Big-O: O(1) iterasi terbatas pada 10 node Stack teratas

--- 10 Transaksi Terakhir: C001 ---
#000 | Mouse Model-5   | 10x | Rp 46.950.000
```

### LAPORAN_HARIAN
> `LAPORAN_HARIAN`

input:
```
LAPORAN_HARIAN
```

output:
```
Big-O: O(n^2) menggunakan Linked List Insertion/Bubble Sort

=================================================================
    LAPORAN TRANSAKSI HARIAN (Diurutkan per Waktu Pemesanan)     
                           17 May 2026                           
=================================================================
ID    | Produk     | Qty  | Total          | Waktu
-----------------------------------------------------------------
0     | P001       | 10   | Rp 19.350.000  | 21:08:52
1     | P001       | 2    | Rp 3.870.000   | 21:09:16
=================================================================

=================================================================
     LAPORAN TRANSAKSI HARIAN (Diurutkan per Harga Termahal)     
                           17 May 2026                           
=================================================================
ID    | Produk     | Qty  | Total          | Waktu
-----------------------------------------------------------------
0     | P001       | 10   | Rp 19.350.000  | 21:08:52
1     | P001       | 2    | Rp 3.870.000   | 21:09:16
-----------------------------------------------------------------
TOTAL TRANSAKSI : 2
TOTAL OMZET     : Rp 23.220.000
=================================================================
```

## 📂 Struktur Folder
```text
tbp-asd-kelompok-XX/
├── src/                    # Kode sumber modul
│   ├── data_structures/    # Implementasi Struktur Data (Linked List, BST, dll)
│   ├── modules/            # Modul aplikasi
│   └── main.py             # Entry point aplikasi CLI
├── tests/                  # Unit testing per modul
├── docs/                   # Laporan PDF & Slide Presentasi
├── experiments/            # Skrip & data eksperimen Big-O
├── AI_Log/                 # Log prompt & screenshot penggunaan AI
└── README.md
```

## 📊 Analisis Kompleksitas (Ringkasan)
Setiap operasi utama telah dianalisis efisiensinya:
*   **Enqueue/Serve Order**: $O(1)$.
*   **BFS Katalog**: $O(\log n)$ (rata-rata).
*   **Graf Rekomendasi**: $O(V + E)$.
*   **Sorting Laporan**: $O(n^2)$.

## 🤖 Penggunaan AI Assistant
Proyek ini menggunakan AI untuk bantuan *debugging*/*refactoring*. Seluruh log percakapan dan screenshot bukti penggunaan telah disertakan pada folder `AI_Log/` sesuai ketentuan.

---
*Dibuat untuk memenuhi tugas Team Based Project mata kuliah Algoritma dan Struktur Data 2025/2026.*
