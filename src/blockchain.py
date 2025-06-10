from utils import log_audit, encrypt_data, decrypt_data
import json
from web3 import Web3




class SmartContractManager:
    def __init__(self, rpc_url, contract_address, abi):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.contract = self.w3.eth.contract(address=contract_address, abi=abi)

    def store_data(self, data, user_id):
        try:
            encrypted_data = encrypt_data(json.dumps(data))
            tx_hash = self.contract.functions.storeFile(
                encrypted_data
            ).transact({'from': user_id})
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
            return {'status': 'stored', 'tx_hash': tx_hash.hex()}
        except Exception as e:
            log_audit(user_id, 'blockchain_storage', {'error': str(e)})
            return {'error': str(e)}

    def retrieve_data(self, data, user_id):
        try:
            encrypted_data = self.contract.functions.getFile(
                data.get('file_id')
            ).call()
            decrypted_data = decrypt_data(encrypted_data)
            return {'data': json.loads(decrypted_data)}
        except Exception as e:
            log_audit(user_id, 'blockchain_retrieval', {'error': str(e)})
            return {'error': str(e)}