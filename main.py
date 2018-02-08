import hashlib
import datetime



class transaction:

    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount




class block:

    def __init__(self, timestamp, data, prevhash=''):
        self.data = data
        self.timestamp = timestamp
        self.prevhash = prevhash
        self.mine_data = 0
        self.hash = self.get_hash()



    def get_hash(self):
        sha = hashlib.sha256()
        if type(self.data) is not str:
            data_string = ''.join('[{}{}{}] '.format(send, receive, amt) for trans.sender, trans.receiver, trans.amount in trans for trans in data)
            sha.update(str(str(self.mine_data)+data_string+self.timestamp+self.prevhash).encode('utf-8'))
        else:
            sha.update(str(str(self.mine_data)+self.data+self.timestamp+self.prevhash).encode('utf-8'))

        return sha.hexdigest()

    def print_block(self):
        print(str(self.data+' '+self.timestamp+' '+self.prevhash+' '+self.hash))

    def mine_block(self, difficulty):
        while self.hash[0:difficulty] != '0'*difficulty:
            self.mine_data += 1
            self.hash = self.get_hash()

        print("Block mined: " + self.hash)


class chain:

    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 8

    def create_genesis_block(self):
        return block('01/01/2018', 'Genesis Block', '')

    def get_latest_block(self):
        return self.chain[len(self.chain) - 1]

    def mine_pending_transctions(self, miner_adress):
        self.pending_transactions.append(transaction(None, miner_adress, self.mining_reward))
        new_block = block(datetime.datetime.now().strftime('%d/%m/%y %M:%H:%S'), self.pending_transactions)
        new_block.mine_block(self.difficulty)

        print('Block successfully mined...')
        self.chain.append(new_block)
        self.pending_transactions = []

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def get_balance(self, adress):
        balance = 0
        for block in self.chain:
            for transaction in block:
                if transaction.sender == adress:
                    balance -= transaction.amount
                elif transaction.receiver == adress:
                    balance += transaction.amount
        return balance

    def validate(self):
        for i in range(1,len(self.chain)-1):
            block_check = self.chain[i]
            previous_block_check = self.chain[i-1]
            if block_check.hash != block_check.get_hash():
                return False
            elif block_check.prevhash != previous_block_check.hash:
                return False
            else:
                return True





jCoin = chain()

jCoin.add_transaction(transaction('adress1','adress2', 16))
print('\n Strarting the miner...')
jCoin.mine_pending_transctions('test-adress')

print('test-adress balance is '+jCoin.get_balance('test-adress'))
print('Is chain valid?' + str(jCoin.validate()))
