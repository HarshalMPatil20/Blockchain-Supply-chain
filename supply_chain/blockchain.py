import hashlib
import json
from datetime import datetime
from .models import Block
from time import time

# class Blockchain:
#     def _init_(self):
#         self.chain = []

#     def add_block(self, transaction_data):
#         previous_hash = self.chain[-1]['block_hash'] if self.chain else '0'
#         block = {
#             'previous_hash': previous_hash,
#             'transaction_details': transaction_data,
#             'timestamp': str(datetime.now()),
#         }
#         block['block_hash'] = self.compute_hash(block)
#         self.chain.append(block)
#         return block

#     def compute_hash(self, block):
#         block_string = json.dumps(block, sort_keys=True).encode()
#         return hashlib.sha256(block_string).hexdigest()

#     def get_chain(self):
#         return self.chain
    
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(previous_hash='1', proof=100)  # Create genesis block

    def create_block(self, proof, previous_hash=None):
        block = Block(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.current_transactions,
            previous_hash=previous_hash or self.chain[-1].hash
        )
        self.current_transactions = []  # Reset the current transactions
        self.chain.append(block)
        return block

    def add_transaction(self, sender, recipient, amount, crop_id):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'crop_id': crop_id  # Include crop_id for tracing
        })
        return self.last_block.index + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"  # Adjust the number of leading zeros for difficulty

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Check if the hash of the block is correct
            if current.hash != current.calculate_hash():
                return False

            # Check if the previous block's hash is correct
            if current.previous_hash != previous.hash:
                return False

        return True

    def trace_crop(self, crop_id):
        # This function could be customized to trace crop details
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.get('crop_id') == crop_id:
                    return block
        return None
    
    def create_block_with_proof(self):
        last_block = self.last_block
        last_proof = last_block.index  # You might want to change this to use the last proof
        proof = self.proof_of_work(last_proof)

        # Create a new block with the proof
        previous_hash = last_block.hash
        block = self.create_block(proof, previous_hash)
        return block
    
