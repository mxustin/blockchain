from src.ground import cnst
from src.entities import block_header


def test_positive_create_instance():
    bh = block_header.BlockHeader()
    assert bh.version == cnst.CURRENT_PROTOCOL_VERSION
    assert not bh.fully_initialized()


def test_positive_create_genesis():
    bh = block_header.BlockHeader(True)
    assert bh.genesis_str == 'True'
    assert bh.prev_hash == cnst.ZERO_HASH
