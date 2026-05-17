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

| Perintah | Deskripsi | Contoh Input |
| :--- | :--- | :--- |
| `ORDER` | Menambah pesanan baru ke antrian | `ORDER C001 P005 PREMIUM` |
| `SERVE` | Memproses pesanan prioritas tertinggi | `SERVE` |
| `CANCEL_LAST` | Membatalkan pesanan terakhir | `CANCEL_LAST` |
| `CARI_PRODUK`| Mencari detail produk di BST | `CARI_PRODUK P010` |
| `REKOMENDASI`| Rekomendasi produk berbasis Graph/BFS | `REKOMENDASI P001` |
| `RIWAYAT` | Menampilkan 10 transaksi terakhir user | `RIWAYAT C001` |
| `LAPORAN_HARIAN` | Menampilkan urutan order selesai | `LAPORAN_HARIAN` |

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
