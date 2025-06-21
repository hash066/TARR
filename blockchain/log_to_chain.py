import os
import json
from web3 import Web3
from dotenv import load_dotenv

# Load values from .env file
load_dotenv()

# Get secrets from environment variables
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Connect to Web3 provider (Sepolia via Infura)
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
assert w3.is_connected(), "❌ Not connected to Web3. Check INFURA_URL."

# Load ABI from file
with open("D:/RVCE/EL/software/blockchain/abi.json") as f:
    abi = json.load(f)

# Create contract instance
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# Function to log failure event to the blockchain
def log_failure_to_chain(reason, delta_t):
    try:
        nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)
        tx = contract.functions.logFailure(reason, int(delta_t * 100)).build_transaction({
            'from': WALLET_ADDRESS,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': Web3.to_wei('10', 'gwei')
        })
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print("✅ Logged to blockchain:", tx_hash.hex())
    except Exception as e:
        print("❌ Error logging to blockchain:", e)

# Function to confirm repair by the company
def confirm_repair():
    try:
        nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)
        tx = contract.functions.confirmRepair().build_transaction({
            'from': WALLET_ADDRESS,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': Web3.to_wei('10', 'gwei')
        })
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print("✅ Repair confirmed on blockchain:", tx_hash.hex())
    except Exception as e:
        print("❌ Error confirming repair:", e)

# Function to release payment to client after repair
def release_payment():
    try:
        nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)
        tx = contract.functions.releasePayment().build_transaction({
            'from': WALLET_ADDRESS,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': Web3.to_wei('10', 'gwei')
        })
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print("💸 Payment released to client:", tx_hash.hex())
    except Exception as e:
        print("❌ Error releasing payment:", e)
