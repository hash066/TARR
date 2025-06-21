from web3 import Web3
import os
import json
from dotenv import load_dotenv

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Load ABI
with open("D:/RVCE/EL/software/blockchain/abi.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

def get_all_failures():
    try:
        # Create a filter for the FailureLogged event
        event_filter = contract.events.FailureLogged.create_filter(fromBlock=0, toBlock='latest')

        # Get event logs
        logs = event_filter.get_all_entries()

        # Format logs for dashboard
        formatted_logs = []
        for log in logs:
            formatted_logs.append({
                "sender": log['args']['sender'],
                "reason": log['args']['reason'],
                "deltaT": log['args']['deltaT'],
                "timestamp": log['args']['timestamp']
            })
        return formatted_logs
    except Exception as e:
        print("❌ Error fetching failures:", e)
        return []
