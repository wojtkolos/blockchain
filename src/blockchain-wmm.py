import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + str(previous_hash) + str(timestamp) + str(data)
    return hashlib.sha256(value.encode()).hexdigest()

def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Block", calculate_hash(0, "0", int(time.time()), "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

def verify_blockchain(blockchain):
    for i in range(1, len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]

        if current_block.hash != calculate_hash(current_block.index, previous_block.hash, current_block.timestamp, current_block.data):
            return False

        if current_block.previous_hash != previous_block.hash:
            return False

    return True

# Creating the blockchain
blockchain = [create_genesis_block()]
print("Genesis Block created.")

# Adding new blocks to the blockchain
block1 = create_new_block(blockchain[-1], "Transaction Data 1")
blockchain.append(block1)
print("Block 1 created.")

block2 = create_new_block(blockchain[-1], "Transaction Data 2")
blockchain.append(block2)
print("Block 2 created.")

# Verifying the blockchain
is_valid = verify_blockchain(blockchain)
print("Is blockchain valid?", is_valid)


"""
This implementation defines a Block class that represents a single block in the blockchain. Each block contains an index, a hash of the previous block, a timestamp, some data (in this case, transaction data), and its own hash. The calculate_hash function calculates the hash of a given block based on its attributes using the SHA-256 algorithm.

The create_genesis_block function creates the initial block (genesis block) with hardcoded data. The create_new_block function creates a new block by taking the previous block as input and generating a new hash for the current block.

Finally, the verify_blockchain function checks the integrity of the blockchain by verifying the hash and previous hash of each block against the calculated values.

In the example code, we create a blockchain by adding a genesis block and two subsequent blocks. Then, we verify the integrity of the blockchain by calling the verify_blockchain function.
"""
