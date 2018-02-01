import hashlib

sha = hashlib.sha256()


class block:

    def __init__(self, index, timestamp, data, prevhash=''):
        self.index = index
        self.data = data
        self.timestamp = timestamp
        self.prevhash = prevhash
        self.hash = self.get_hash()

    def get_hash(self):
        if type(self.data) is not str:
            data_string = ''.join('{}{}'.format(key, val) for key, val in self.data.items())
            sha.update(str(str(self.index)+data_string+self.timestamp+self.prevhash).encode('utf-8'))
        else:
            sha.update(str(str(self.index)+self.data+self.timestamp+self.prevhash).encode('utf-8'))

        return sha.hexdigest()

    def print_block(self):
        print(str(str(self.index)+' '+self.data+' '+self.timestamp+' '+self.prevhash+' '+self.hash))


class chain:

    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return block(0, '01/01/2018', 'Genesis Block', '')

    def get_latest_block(self):
        return self.chain[len(self.chain) - 1]

    def add_block(self, new_block):
        new_block.prevhash = self.get_latest_block().hash
        new_block.hash = new_block.get_hash()
        self.chain.append(new_block)


jCoin = chain()

jCoin.add_block(block(1, '01/31/2018', {'amount': 4}))
jCoin.add_block(block(2, '02/01/2018', {'amount': 4}))
