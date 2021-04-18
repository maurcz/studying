import hashlib
import json
from time import time
from urllib.parse import urlparse

import requests


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()  # nodes must be unique

        # Genesis block
        self.add_block(previous_hash=1, proof=100)

    @property
    def last_block(self) -> dict:
        return self.chain[-1]

    @staticmethod
    def generate_hash(block: dict) -> str:
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_block(self, proof: str, previous_hash=None) -> dict:
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.generate_hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender: str, recipient: str, amount: int) -> int:
        """
        `current_transations` go into the next mined Block
        """
        self.current_transactions.append(
            {
                "sender": sender,
                "recipient": recipient,
                "amount": amount,
            }
        )

        return self.last_block["index"] + 1

    def mine(self, last_proof: str) -> int:
        """
        Very basic Proof of Work (PoW) algo: generate hashes until it gets one where
        the last 4 digits are equal to 0.

        Generally, solutions from a Proof of Work algo should be hard to find but easy
        to verify. Even in this naive implementation, increasing the number of characters
        to find in the string increases runtime significantly while still making it super
        easy to validate the "solution".

        Using `last_proof` is important not only to potentially increase the difficulty of
        finding the solution over time, but also to validate the integrity of the chain.
        (see `validate_chain`)

        """
        proof = 0
        while not self._check_valid_proof(last_proof, proof):
            proof += 1

        return proof

    @staticmethod
    def _check_valid_proof(last_proof: int, proof: int) -> bool:
        """
        Finds a hash that ends with 0000, based on the previous
        encountered proof + current.
        """
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    """
    What follows is a simple representation of how nodes can interact with
    each other, validating if chains from neighbors are valid and replacing
    their own chains if they see any conflicts.
    """

    def register_node(self, address: str):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def validate_chain(self, chain: list) -> bool:
        """
        Validates the integrity of the chain by verifying it hashes and proofs are
        consistent across all sequential pairs of blocks.
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            if block["previous_hash"] != self.generate_hash(last_block):
                return False

            if not self._check_valid_proof(last_block["proof"], block["proof"]):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self) -> bool:
        """
        The example in the article is not really resolving conflicts, it just
        replaces the current chain with the longer one found in other nodes.

        It won't take into account concurrent transactions/mining operations that
        might have been made to two or more different nodes - meaning data might be
        lost.
        """

        neighbors = self.nodes
        largest_chain_size = len(self.chain)
        new_chain = None

        for node in neighbors:
            response = requests.get(f"http://{node}/chain")  # implies knowledge about the API...

            if not response.status_code == 200:
                continue

            length = response.json()["length"]
            chain = response.json()["chain"]

            if length > largest_chain_size and self.validate_chain(chain):
                largest_chain_size = length
                new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False
