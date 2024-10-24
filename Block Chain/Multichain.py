from bitcoinlib.wallets import Wallet, WalletError
from web3 import Web3

class MultiChainWallet:
    def __init__(self):
        # Try to create a new Bitcoin wallet or load the existing one
        try:
            self.bitcoin_wallet = Wallet.create('MyBitcoinWallet')
        except WalletError as e:
            if "already exists" in str(e):
                self.bitcoin_wallet = Wallet('MyBitcoinWallet')
            else:
                raise e
        self.ethereum_wallet = None
        self.w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))

    def create_ethereum_wallet(self):
        account = self.w3.eth.account.create()
        self.ethereum_wallet = {
            'address': account.address,
            'private_key': account.key.hex()
        }
        return self.ethereum_wallet

    def get_bitcoin_balance(self):
        return self.bitcoin_wallet.balance()

    def get_ethereum_balance(self):
        if not self.ethereum_wallet:
            print("Ethereum wallet not created.")
            return None
        balance = self.w3.eth.get_balance(self.ethereum_wallet['address'])
        return self.w3.fromWei(balance, 'ether')

    def send_bitcoin(self, to_address, amount):
        transaction = self.bitcoin_wallet.send_to(to_address, amount)
        return transaction

    def send_ethereum(self, to_address, amount):
        if not self.ethereum_wallet:
            print("Ethereum wallet not created.")
            return None
            
        tx = {
            'to': to_address,
            'value': self.w3.toWei(amount, 'ether'),
            'gas': 2000000,
            'gasPrice': self.w3.toWei('50', 'gwei'),
            'nonce': self.w3.eth.getTransactionCount(self.ethereum_wallet['address']),
        }
        
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.ethereum_wallet['private_key'])
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return tx_hash.hex()

if __name__ == "__main__":
    wallet = MultiChainWallet()
    
    eth_wallet = wallet.create_ethereum_wallet()
    print("Ethereum Wallet Address:", eth_wallet['address'])
    
    print("Bitcoin Balance:", wallet.get_bitcoin_balance())
    print("Ethereum Balance:", wallet.get_ethereum_balance())
