import web3
from utils import log_audit, encrypt_data, decrypt_data
import json
from web3 import Web3

def store_data(data, user_id):
    try:
        w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
        contract = w3.eth.contract(address='0xYourContract', abi='Your ABI')
        encrypted_data = encrypt_data(json.dumps(data))
        tx_hash = contract.functions.storeFile(encrypted_data).transact({'from': user_id})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return {'status': 'stored', 'tx_hash': tx_hash.hex()}
    except Exception as e:
        log_audit(user_id, 'blockchain_storage', {'error': str(e)})
        return {'error': str(e)}

def retrieve_data(data, user_id):
    try:
        w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
        contract = w3.eth.contract(address='0xYourContract', abi='Your ABI')
        encrypted_data = contract.functions.getFile(data.get('file_id')).call()
        decrypted_data = decrypt_data(encrypted_data)
        return {'data': json.loads(decrypted_data)}
    except Exception as e:
        log_audit(user_id, 'blockchain_retrieval', {'error': str(e)})
        return {'error': str(e)}