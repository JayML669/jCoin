import pickle
import csv
import os
import time
from block import block
from blockchain import chain
from transaction import transaction


if __name__ == '__main__':

    dir = os.path.dirname(__file__)

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

    if not os.path.exists('pending_blocks'):
        os.mkdir('pending_blocks')

    while True:
        with open('block_chain.pickle', 'wb') as f:
            pickle.dump(jCoin, f)

        if os.stat('pending_transactions.csv').st_size != 0:
            with open('pending_transactions.csv') as file:
                reader = csv.reader(file)
                for row in reader:
                    add_transaction(transaction(row[0], row[1], row[2]))

                file.turnicate()

        for filename in os.listdir('pending_blocks'):
            if filename.endswith('.pickle'):
                with open('block_chain.pickle', 'rb') as f:
                    test_chain = pickle.load(f)
                with open('pending_blocks/'+filename, 'r') as f:
                    test_block = pickle.load(f)
                test_chain.chain.append(test_block)
                if test_chain.validate() == True:
                    jCoin.append(test_block)
