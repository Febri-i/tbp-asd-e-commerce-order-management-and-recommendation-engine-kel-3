from typing import cast
import sys
import os
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, src_path)

from data_structures.produk import Produk, TIER, Order

from data_structures.linked_list import LLNode


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

