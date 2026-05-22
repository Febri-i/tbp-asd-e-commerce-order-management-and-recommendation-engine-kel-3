import sys
import os
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, src_path)

from data_structures.produk import Produk, TIER, Order
from typing import List


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
