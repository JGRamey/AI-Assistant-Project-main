import os
from web3 import Web3
from utils import log_audit

class SmartContractManager:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.environ.get('ETH_RPC_URL')))
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Ethereum node")
        self.account = self.w3.eth.account.from_key(os.environ.get('ETH_PRIVATE_KEY'))
        self.chain_id = int(os.environ.get('CHAIN_ID', 11155111))  # Sepolia testnet

    def deploy_contract(self, contract_name: str, constructor_args: list, abi: list, bytecode: str) -> str:
        """Deploy a smart contract to the Ethereum blockchain."""
        try:
            contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
            constructor = contract.constructor(*constructor_args)
            
            # Estimate gas
            gas_estimate = constructor.estimate_gas({
                'from': self.account.address
            })
            
            # Build transaction
            tx = constructor.build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'chainId': self.chain_id,
                'gas': gas_estimate,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign and send transaction
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 1:
                log_audit(self.account.address, "deploy_contract", {
                    "contract_name": contract_name,
                    "address": receipt.contractAddress
                })
                return receipt.contractAddress
            else:
                raise Exception("Contract deployment failed")
                
        except Exception as e:
            log_audit(self.account.address, "deploy_contract_error", {"error": str(e)})
            raise

    def interact_with_contract(self, contract_address: str, abi: list, function_name: str, args: list) -> dict:
        """Interact with a deployed smart contract."""
        try:
            contract = self.w3.eth.contract(address=contract_address, abi=abi)
            function = getattr(contract.functions, function_name)
            
            # Build transaction
            tx = function(*args).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'chainId': self.chain_id,
                'gas': function(*args).estimate_gas({'from': self.account.address}),
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign and send transaction
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 1:
                log_audit(self.account.address, "contract_interaction", {
                    "contract_address": contract_address,
                    "function_name": function_name
                })
                return {"status": "success", "tx_hash": tx_hash.hex()}
            else:
                raise Exception("Contract interaction failed")
                
        except Exception as e:
            log_audit(self.account.address, "contract_interaction_error", {"error": str(e)})
            raise