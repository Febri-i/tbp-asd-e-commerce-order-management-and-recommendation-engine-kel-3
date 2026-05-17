from typing import Dict, List, Tuple
from data_structures.queue import Queue  

class GraphRekomendasi:
    """
    Struktur data Graf Tak Berarah (Undirected Weighted Graph) untuk merepresentasikan
    relasi co-purchase (produk yang dibeli bersamaan) dalam sistem rekomendasi e-commerce.
    
    Implementasi menggunakan Adjacency List (Daftar Ketetanggaan) berbasis Dictionary.
    """
    
    def __init__(self):
        """
        BigO = O(1)
        Inisialisasi graf kosong.
        
        Atribut:
            adj (Dict[str, List[Tuple[str, int]]]): Dictionary yang memetakan kode_produk 
            ke daftar tetangganya. Format: { 'kode_sumber': [('kode_tujuan', frekuensi_dibeli_bersama)] }
        """
        self.adj: Dict[str, List[Tuple[str, int]]] = {}

    def _add_directed_edge(self, src: str, dest: str) -> None:
        """
        BigO = O(d)
        Fungsi helper internal (private) untuk menambahkan edge/sisi satu arah.
        
        Jika edge sudah ada, bobot (frekuensi) akan ditambahkan 1. 
        Jika belum ada, edge baru akan dibuat dengan frekuensi 1.

        Args:
            src (str): Kode produk sumber.
            dest (str): Kode produk tujuan.
            
        Kompleksitas Waktu: 
            O(deg(V)) di mana deg(V) adalah jumlah tetangga (derajat) dari node sumber.
        """
        if src not in self.adj:
            self.adj[src] = []
        
        # Cari apakah edge/relasi sudah ada
        for i, (node, freq) in enumerate(self.adj[src]):
            if node == dest:
                # Jika sudah ada, tingkatkan bobot (frekuensi co-purchase)
                self.adj[src][i] = (node, freq + 1)
                return
        
        # Jika relasi belum ada, tambahkan edge baru dengan frekuensi 1
        self.adj[src].append((dest, 1))

    def add_copurchase(self, kode_a: str, kode_b: str) -> None:
        """
        BigO = O(da+db)
        Mencatat bahwa dua produk dibeli secara bersamaan dalam satu pesanan.
        Membentuk relasi tak berarah (undirected edge) antara kedua produk.

        Args:
            kode_a (str): Kode produk pertama.
            kode_b (str): Kode produk kedua.
            
        Kompleksitas Waktu: 
            O(deg(V)) untuk mencari dan memperbarui edge.
        """
        if kode_a == kode_b:
            return # Mencegah self-loop (produk direkomendasikan dengan dirinya sendiri)
            
        # Karena ini co-purchase (dibeli bersamaan), graf bersifat dua arah (undirected)
        self._add_directed_edge(kode_a, kode_b)
        self._add_directed_edge(kode_b, kode_a)

    def rekomendasikan(self, kode_produk: str, max_hop: int = 2) -> List[str]:
        """
        BigO = O(V+E)
        Menghasilkan daftar rekomendasi produk menggunakan algoritma 
        Breadth-First Search (BFS) berdasarkan relasi co-purchase.

        Args:
            kode_produk (str): Kode produk yang sedang dilihat/dibeli pengguna.
            max_hop (int, optional): Kedalaman pencarian maksimal (derajat koneksi). 
                                     Default adalah 2 (teman dari teman).

        Returns:
            List[str]: Daftar kode produk yang direkomendasikan. Mengembalikan list 
                       kosong jika produk tidak memiliki riwayat co-purchase.
                       
        Kompleksitas Waktu:
            O(V + E) di mana V adalah jumlah vertex dan E adalah jumlah edge 
            yang dikunjungi dalam batasan max_hop.
        """
        if kode_produk not in self.adj:
            return [] # Produk belum pernah dibeli bersamaan dengan apa pun

        # Menggunakan class Queue berbasis Linked List milik kelompok
        queue = Queue() 
        
        # Masukkan node awal ke antrean dengan format Tuple: (kode_produk, jumlah_hop)
        queue.enqueue((kode_produk, 0))
        
        # Himpunan untuk mencatat node yang sudah dikunjungi agar tidak terjadi infinite loop
        visited = {kode_produk}
        rekomendasi_hasil: List[str] = []

        while not queue.is_empty():
            # Ambil data dari antrean paling depan (O(1))
            item = queue.dequeue()
            
            # Keamanan tambahan jika antrean kosong
            if item is None:
                break
                
            curr_node, current_hop = item

            # Jika kedalaman pencarian BFS sudah mencapai max_hop, hentikan pencarian di cabang ini
            if current_hop >= max_hop:
                continue

            # Telusuri semua produk tetangga (yang pernah dibeli bersama curr_node)
            for tetangga, _freq in self.adj.get(curr_node, []):
                if tetangga not in visited:
                    visited.add(tetangga)
                    rekomendasi_hasil.append(tetangga) # Catat sebagai hasil rekomendasi
                    
                    # Masukkan ke antrean untuk dicek tetangganya nanti (hop bertambah 1)
                    queue.enqueue((tetangga, current_hop + 1))

        return rekomendasi_hasil
