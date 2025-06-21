import os
import json
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
assert w3.is_connected(), "❌ Web3 not connected"

with open("D:/RVCE/EL/software/blockchain/abi.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)


def get_all_failures():
    try:
        failure_event = contract.events.FailureLogged()
        logs = failure_event.create_filter(fromBlock=0).get_all_entries()
        result = []
        for e in logs:
            result.append({
                "sender": e["args"]["sender"],
                "reason": e["args"]["reason"],
                "deltaT": e["args"]["deltaT"] / 100,
                "timestamp": e["args"]["timestamp"]
            })
        return result
    except Exception as e:
        print("❌ Error fetching logs:", e)
        return []
