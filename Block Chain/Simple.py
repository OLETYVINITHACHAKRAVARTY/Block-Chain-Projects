import hashlib
import time

# Block class to define individual blocks in the blockchain
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

# Function to calculate the hash of a block
def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + previous_hash + str(timestamp) + str(data)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

# Function to create the genesis block (first block in the chain)
def create_genesis_block():
    return Block(0, "0", time.time(), "Genesis Block", calculate_hash(0, "0", time.time(), "Genesis Block"))

# Function to generate a new block
def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = time.time()
    previous_hash = previous_block.hash
    hash = calculate_hash(index, previous_hash, timestamp, data)
    return Block(index, previous_hash, timestamp, data, hash)

# Blockchain class to manage the chain
class Blockchain:
    def __init__(self):
        self.chain = [create_genesis_block()]  # Starting the blockchain with the genesis block

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        new_block = create_new_block(self.get_latest_block(), data)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Validate current block hash
            if current_block.hash != calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data):
                return False

            # Validate previous block hash link
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

# Example usage of the blockchain
def main():
    # Create the blockchain
    blockchain = Blockchain()

    # Add some blocks with dummy data
    blockchain.add_block("First transaction")
    blockchain.add_block("Second transaction")
    blockchain.add_block("Third transaction")

    # Print out the blocks
    for block in blockchain.chain:
        print(f"Block {block.index}:\nHash: {block.hash}\nPrevious Hash: {block.previous_hash}\nData: {block.data}\n")

    # Validate the blockchain
    print("Is blockchain valid?", blockchain.is_chain_valid())

if __name__ == "__main__":
    main()
