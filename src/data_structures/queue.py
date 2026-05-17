from data_structures.ll import LLNode
from typing import Optional, Any

class Queue:
    """
    Implementasi struktur data Queue (Antrean) menggunakan prinsip First-In-First-Out (FIFO) 
    berbasis Linked List.
    
    Attributes:
        head (Optional[LLNode]): Pointer yang menunjuk ke elemen pertama (paling depan) di antrean.
        tail (Optional[LLNode]): Pointer yang menunjuk ke elemen terakhir (paling belakang) di antrean.
        _size (int): Jumlah elemen yang saat ini ada di dalam antrean.
    """

    def __init__(self):
        """Menginisialisasi Queue baru yang kosong."""
        self.head: Optional[LLNode] = None
        self.tail: Optional[LLNode] = None
        self._size: int = 0

    def enqueue(self, data: Any) -> None:
        """
        Menambahkan pesanan/elemen baru ke posisi paling belakang (tail) dari antrean.
        
        Kompleksitas Waktu:
            $O(1)$ - Karena menggunakan pointer tail, penyisipan dilakukan secara instan.

        Args:
            data (Any): Data atau objek pesanan yang ingin dimasukkan ke antrean.
        """
        new_node = LLNode(data)
        if self.is_empty() or not self.tail:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def dequeue(self) -> Any | None:
        """
        Menghapus dan mengembalikan elemen yang berada di posisi paling depan (head) dari antrean.
        
        Kompleksitas Waktu:
            $O(1)$ - Pengambilan langsung dari pointer head tanpa perlu menggeser elemen lain.

        Returns:
            Any | None: Data dari elemen yang diproses, atau None jika antrean kosong.
        """
        if self.is_empty() or not self.head:
            return None
            
        data = self.head.data
        self.head = self.head.next
        
        if self.head is None:
            self.tail = None
            
        self._size -= 1
        return data

    def peek(self) -> Any | None:
        """
        Melihat data elemen paling depan dari antrean tanpa menghapusnya/memprosesnya.

        Kompleksitas Waktu:
            $O(1)$

        Returns:
            Any | None: Data elemen terdepan, atau None jika antrean kosong.
        """
        return self.head.data if self.head else None

    def is_empty(self) -> bool:
        """
        Memeriksa apakah antrean sedang dalam keadaan kosong.

        Kompleksitas Waktu:
            $O(1)$

        Returns:
            bool: True jika antrean kosong (size == 0), False jika ada isinya.
        """
        return self._size == 0

    def __len__(self) -> int:
        """
        Mengembalikan jumlah elemen yang saat ini berada di dalam antrean.
        Dapat dipanggil menggunakan fungsi bawaan len(queue).

        Kompleksitas Waktu:
            $O(1)$

        Returns:
            int: Jumlah elemen di antrean.
        """
        return self._size
