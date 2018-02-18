from block import block
from transaction import transaction


class chain:

    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 6
        self.pending_transactions = []
        self.mining_reward = 8

    def create_genesis_block(self):
        return block('01/01/2018', transaction('Genesis Block', 'Genesis Block', 0), '')

    def get_latest_block(self):
        return self.chain[len(self.chain) - 1]

    def mine_pending_transctions(self, miner_adress, chain):
        self.pending_transactions.append(transaction('None', miner_adress, self.mining_reward))
        new_block = block(datetime.datetime.now().strftime(
            '%d/%m/%y %M:%H:%S'), self.pending_transactions, chain.chain[len(chain.chain)-1].hash)
        new_block.mine_block(self.difficulty)

        print('Block successfully mined...')
        self.chain.append(new_block)
        self.pending_transactions = []

    def add_transaction(self, transaction):
        if(self.get_balance(transaction.sender) >= transaction.amount):
            self.pending_transactions.append(transaction)
        else:
            print('Error transaction invalid')

    def get_balance(self, adress):
        balance = 0
        for block in self.chain:
            if type(block.data) is list:
                for transaction in block.data:
                    if transaction.sender == adress:
                        balance -= transaction.amount
                    elif transaction.receiver == adress:
                        balance += transaction.amount
            else:
                if block.data.sender == adress:
                    balance -= transaction.amount
                elif block.data.receiver == adress:
                    balance += transaction.amount
        return balance

    def validate(self):
        for i in range(1, len(self.chain)-1):
            block_check = self.chain[i]
            previous_block_check = self.chain[i-1]
            if block_check.hash != block_check.get_hash():
                return False
            elif block_check.prevhash != previous_block_check.hash:
                return False
            else:
                return True
