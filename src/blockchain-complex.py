import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.nonce = nonce

    def calculate_hash(self):
        value = str(self.index) + str(self.previous_hash) + str(self.timestamp) + str(self.data) + str(self.nonce)
        return hashlib.sha256(value.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Number of leading zeros required in the hash

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), "Genesis Block", "", 0)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_last_block().hash
        new_block.hash = new_block.calculate_hash()
        self.proof_of_work(new_block)
        self.chain.append(new_block)

    def proof_of_work(self, block):
        while block.hash[:self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()

    def validate_blockchain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def create_transaction(self, sender, receiver, amount):
        new_transaction = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        }
        return new_transaction

    def validate_transaction(self, transaction):
        sender_balance = self.get_balance(transaction['sender'])

        if sender_balance < transaction['amount']:
            return False

        return True

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            if block.data != "Genesis Block":
                transactions = block.data
                for transaction in transactions:
                    if transaction['sender'] == address:
                        balance -= transaction['amount']
                    if transaction['receiver'] == address:
                        balance += transaction['amount']
        return balance

# Creating a blockchain
blockchain = Blockchain()
print("Blockchain created.")

# Adding blocks and transactions to the blockchain
transaction1 = blockchain.create_transaction("Alice", "Bob", 10)
transaction2 = blockchain.create_transaction("Bob", "Charlie", 5)
transaction3 = blockchain.create_transaction("Alice", "Charlie", 3)

block1 = Block(1, "", int(time.time()), [transaction1, transaction2], "", 0)
blockchain.add_block(block1)
print("Block 1 created.")

block2 = Block(2, "", int(time.time()), [transaction3], "", 0)
blockchain.add_block(block2)
print("Block 2 created.")

# Verifying the blockchain and transactions
is_valid_blockchain = blockchain.validate_blockchain()
is_valid_transaction = blockchain.validate_transaction(transaction1)
print("Is blockchain valid?", is_valid_blockchain)
print("Is transaction valid?", is_valid_transaction)

# Checking balance
balance_alice = blockchain.get_balance("Alice")
balance_bob = blockchain.get_balance("Bob")
balance_charlie = blockchain.get_balance("Charlie")
print("Alice's balance:", balance_alice)
print("Bob's balance:", balance_bob)
print("Charlie's balance:", balance_charlie)

"""
A Blockchain class that contains a list of blocks (chain). Each block has an additional attribute nonce used in the Proof of Work algorithm.

The proof_of_work method is responsible for finding a suitable nonce value that satisfies the difficulty level (number of leading zeros) defined in the Blockchain class.

The validate_blockchain method ensures the integrity of the blockchain by verifying the hash and previous hash of each block. If any block is tampered with, the method returns False.

The create_transaction method creates a new transaction with a sender, receiver, and amount.

The validate_transaction method checks if a transaction is valid by verifying the sender's balance. If the sender has enough balance, the method returns True; otherwise, it returns False.

The get_balance method calculates the balance of a given address by iterating through all blocks and transactions in the blockchain.

In the example code, we create a blockchain, add blocks with transactions, and validate the blockchain and transactions. Finally, we check the balances of three addresses: Alice, Bob, and Charlie.
"""
