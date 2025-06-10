import os
from web3 import Web3
from solcx import compile_source

class SmartContractManager:
    def __init__(self):
        self.w3 = None
        self.contract = None
        self.account = None
        self.chain_id = int(os.getenv('CHAIN_ID', 11155111))  # Sepolia testnet
        self.eth_rpc_url = os.getenv('ETH_RPC_URL', 'https://rpc.sepolia.org')
        self.eth_private_key = os.getenv('ETH_PRIVATE_KEY', 'mock-private-key')

    def connect(self):
        if os.getenv('TESTING') == 'True':
            return True
        self.w3 = Web3(Web3.HTTPProvider(self.eth_rpc_url))
        if not self.w3.is_connected():
            raise Exception("Failed to connect to Ethereum node")
        self.account = self.w3.eth.account.from_key(self.eth_private_key)
        return True

    def compile_contract(self, contract_source, contract_name):
        compiled = compile_source(contract_source, output_values=['abi', 'bin'])
        contract_id = f'<stdin>:{contract_name}'
        return compiled[contract_id]['abi'], compiled[contract_id]['bin']

    def deploy_contract(self, abi, bytecode, constructor_args):
        if os.getenv('TESTING') == 'True':
            return "0xContractAddress"
        contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        tx = contract.constructor(*constructor_args).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': contract.constructor(*constructor_args).estimate_gas(),
            'chainId': self.chain_id
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.eth_private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 0:
            raise Exception("Contract deployment failed")
        return receipt.contractAddress

    def handle_request(self, data, user_id):
        task = data.get('task')
        if task == 'create_task':
            return {'status': 'success', 'result': {'task_id': 'mock-task-id'}}
        elif task == 'get_task':
            return {'status': 'success', 'result': {'task': 'mock-task'}}
        return {'status': 'error', 'message': 'Invalid task'}