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
        return False;
    for i, data in enumerate(param):
        if (pattern[i] == ParamPattern.NUMBER):
            if not (data.isnumeric()):
                break;
        elif (pattern[i] == ParamPattern.STRING):
            if not (data.isalpha()):
                break;


    return False


def process_command(input: str):
    tokens: List[str] = input.split();
    command: str = tokens[0];

    match command:
        case "ORDER":

            pass
        case "SERVE":
            pass
        case "CANCEL_LAST":

            pass
        case "CARI_PRODUK":

            pass
        case "UPDATE_STOK":

            pass
        case "REKOMENDASI":

            pass
        case "RIWAYAT":
            pass
        case "LAPORAN_HARIAN":
            pass
        case "KELUAR":
            print("bye!")
            exit();
        case _:
            return;
    pass

def main():

    init();

    print('E-Commerce Order Management Ketik BANTUAN untuk daftar perintah')
    while True:
        process_command(input("> "));

if __name__ == '__main__':
    main()
