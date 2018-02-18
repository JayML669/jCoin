import hashlib
import datetime
from transaction import transaction


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
