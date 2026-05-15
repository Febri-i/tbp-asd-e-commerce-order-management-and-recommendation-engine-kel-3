TIER = {'PREMIUM': 1, 'REGULAR': 2, 'ECONOMY': 3}

from dataclasses import dataclass, field

@dataclass
class Produk:
    kode: str # P001–P100
    nama: str
    harga: float
    stok: int

@dataclass
class Order:
    order_id: int
    pelanggan: str # C001–C050
    produk_kode: str
    tier: int # 1=PREMIUM, 2=REGULAR, 3=ECONOMY
    qty: int
    total_harga: float
    waktu_pesan: float # time.time()
