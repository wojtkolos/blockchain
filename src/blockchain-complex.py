import hashlib
import time
import binascii
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

class Client:
    def __init__(self, balance : float = 10):
        random = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)
        self.balance = balance

    @property
    def identity(self) -> str:
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')

class Transaction:
    def __init__(self, sender : Client, recipient : Client, value : float):
        self.sender : Client = sender
        self.recipient : Client = recipient
        self.value : float = value
        self.time = int(time.time())
    
    def to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity

        return {
            'sender': identity,
            'recipient': self.recipient,
            'value': self.value,
            'time' : self.time
        }

    def sign_transaction(self) -> str:
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')
    
class Block:
    def __init__(self, index : int, previous_hash : str, timestamp : int, data : str | list[Transaction], hash : str, nonce : int):
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

    def add_block(self, new_block : Block):
        new_block.previous_hash = self.get_last_block().hash
        new_block.hash = new_block.calculate_hash()
        self.proof_of_work(new_block)
        self.chain.append(new_block)

    def proof_of_work(self, block : Block):
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

    def create_transaction(self, sender : Client, receiver : Client.identity, amount : float):
        new_transaction = Transaction(
            sender,
            receiver,
            amount
        )
        return new_transaction

    def validate_transaction(self, transaction : Transaction):
        sender_balance = self.get_balance(transaction.sender)

        if sender_balance < transaction.value:
            return False

        return True

    def get_balance(self, address : Client):
        balance = 0
        for block in self.chain:
            if block.data != "Genesis Block":
                transactions = block.data
                for transaction in transactions:
                    if transaction.sender.identity == address.identity:
                        balance -= transaction.value
                    if transaction.recipient == address.identity:
                        balance += transaction.value
        return balance

# Creating a blockchain
blockchain = Blockchain()
print("Blockchain created.")

# Create clients
Alice = Client()
Bob = Client()
Alice = Client()
Charlie = Client()


# Create transactions and sign them
transaction1 = Transaction(
    Alice,
    Bob.identity,
    10.0
)
transaction2 = Transaction(
    Bob,
    Charlie.identity,
    5.0
)
transaction3 = Transaction(
    Alice,
    Charlie.identity,
    3.0
)
transaction1.sign_transaction()
transaction2.sign_transaction()
transaction3.sign_transaction()

# Create blocks and add then into blockchain
block1 = Block(1, "", int(time.time()), [transaction1, transaction2], "", 0)
blockchain.add_block(block1)
print("Block 1 created.")

block2 = Block(2, "", int(time.time()), [transaction3], "", 0)
blockchain.add_block(block2)
print("Block 2 created.")

# Verifying the blockchain and transactions
is_valid_blockchain = blockchain.validate_blockchain()
is_valid_transaction = blockchain.validate_transaction(transaction2)
print("Is blockchain valid?", is_valid_blockchain)
print("Is transaction valid?", is_valid_transaction)

# Checking balance
balance_alice = blockchain.get_balance(Alice)
balance_bob = blockchain.get_balance(Bob)
balance_charlie = blockchain.get_balance(Charlie)
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
