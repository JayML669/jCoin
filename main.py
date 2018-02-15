import hashlib
import datetime
import pickle
import csv
import os
import time

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
            data_string = self.get_data_string(self.data)
            sha.update(str(str(self.mine_data)+data_string +
                           self.timestamp+self.prevhash).encode('utf-8'))
        else:
            sha.update(str(str(self.mine_data)+self.data +
                           self.timestamp+self.prevhash).encode('utf-8'))

        return sha.hexdigest()

    def print_block(self):
        print(str(self.data+' '+self.timestamp+' '+self.prevhash+' '+self.hash))

    def mine_block(self, difficulty):
        while self.hash[0:difficulty] != '0'*difficulty:
            self.mine_data += 1
            self.hash = self.get_hash()

        print("Block mined: " + self.hash)

    def get_data_string(self, data):
        string = ''
        if type(data) is list:
            for trans in data:
                s = '[{} {} {}] '.format(trans.sender, trans.receiver, trans.amount)
                string += s

        else:
            string = '[{} {} {}] '.format(data.sender, data.receiver, data.amount)

        return string


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





if os.path.exists('block_chain.pickle'):
    print('Loading the blockchain...')
    pickle_in = open('block_chain.pickle', 'rb')
    jCoin = pickle.load(pickle_in)
else:
    print('Creating the blockchain...')
    jCoin = chain()
    with open('block_chain.pickle', 'wb') as f:
        pickle.dump(jCoin, f)

if not os.path.exists('pending_transactions.csv'):
    f = open('pending_transactions.csv', 'w')
    f.close()

if not os.path.exists('/pending_blocks'):
    os.makedirs('/pending_blocks')




if __name__ == '__main__':
    while True:
        with open('block_chain.pickle', 'wb') as f:
            pickle.dump(jCoin, f)

        if os.stat('pending_transactions.csv').st_size !=0:
            with open('pending_transactions.csv') as file:
                reader = csv.reader(file)
                for row in reader:
                    add_transaction(transaction(row[0],row[1],row[2]))

                file.turnicate()

        for filename in os.listdir('/pending_blocks'):
            if filename.endswith('.pickle'):
                with open('block_chain.pickle', 'rb') as f:
                    test_chain = pickle.load(f)
                with open(filename, 'r') as f:
                    test_block = pickle.load(f)
                test_chain.chain.append(test_block)
                if test_chain.validate() == True:
                    jCoin.append(test_block)
