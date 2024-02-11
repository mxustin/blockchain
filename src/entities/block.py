from src.entities import block_header as hdr
from src.entities import block_txs as txs


class Block:
    def __init__(self, genesis: bool):
        self._magic_number: int = 0
        self._header = hdr.BlockHeader(genesis=genesis)
        self._content = txs.BlockTxs()
