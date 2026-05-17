from data_structures.ll import LLNode
from typing import Optional, Any

class Stack:
    """
    Implementasi struktur data Stack (Tumpukan) menggunakan prinsip Last-In-First-Out (LIFO) 
    berbasis Linked List. Dilengkapi dengan batasan kapasitas (limit).

    Biasanya digunakan untuk menyimpan riwayat pesanan (history) atau fitur undo.

    Attributes:
        top (Optional[LLNode]): Pointer yang menunjuk ke elemen paling atas (terbaru) di stack.
        _size (int): Jumlah elemen yang saat ini ada di dalam stack.
        kapasitas (int): Batas maksimal elemen yang bisa ditampung di dalam stack.
    """

    def __init__(self, kapasitas: int = 10):
        """
        Menginisialisasi Stack baru yang kosong dengan kapasitas tertentu.

        Args:
            kapasitas (int, optional): Batas maksimal elemen. Default adalah 10.
        """
        self.top: Optional[LLNode] = None
        self._size: int = 0
        self.kapasitas: int = kapasitas

    def push(self, data: Any) -> bool:
        """
        Menambahkan elemen baru ke posisi paling atas (top) dari stack.
        Jika jumlah elemen sudah mencapai kapasitas maksimal, penambahan ditolak.

        Kompleksitas Waktu: 
            $O(1)$ - Karena penambahan langsung di posisi top (head).

        Args:
            data (Any): Data atau objek yang ingin dimasukkan ke stack.

        Returns:
            bool: True jika berhasil ditambahkan, False jika gagal karena kapasitas penuh.
        """
        if self._size >= self.kapasitas:
            # Penuh, tolak penambahan (atau opsi lain: hapus elemen terbawah)
            return False
            
        new_node = LLNode(data)
        new_node.next = self.top
        self.top = new_node
        self._size += 1
        return True

    def pop(self) -> Any | None:
        """
        Menghapus dan mengembalikan elemen yang berada di posisi paling atas (top).

        Kompleksitas Waktu: 
            $O(1)$ - Karena pengambilan langsung dari posisi top.

        Returns:
            Any | None: Data dari elemen teratas, atau None jika stack sedang kosong.
        """
        if self.top is None:
            return None
            
        data = self.top.data
        # Geser top ke elemen di bawahnya
        self.top = self.top.next
        self._size -= 1
        return data

    def peek(self) -> Any | None:
        """
        Melihat data pada elemen paling atas tanpa menghapus/mengeluarkannya dari stack.

        Kompleksitas Waktu: 
            $O(1)$

        Returns:
            Any | None: Data elemen teratas, atau None jika stack sedang kosong.
        """
        if self.top is None:
            return None
        return self.top.data
