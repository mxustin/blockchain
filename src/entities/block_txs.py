class BlockTxs:
    def __init__(self):
        self._txs: list = []

    def __repr__(self):
        descr = f'The list of transactions (instance of {__class__.__name__})'
        lgt = len(self._txs)
        cnt = f'count: {lgt}' if lgt > 0 else f'the list is empty'
        result = (f'{descr}:'
                  f'\n ▪️ {cnt}.\n')
        return result

    def add_tx(self, tx):
        self._txs.append(tx)
