import json
import os
import time
from web3 import Web3
from solcx import compile_standard
from utils import log_audit, store_shared_data, get_shared_data

# Initialize Web3 with retry mechanism
def init_web3():
    rpc_url = os.environ.get('ETH_RPC_URL', 'https://sepolia.infura.io/v3/your-infura-project-id')
    max_retries = 3
    for attempt in range(max_retries):
        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            if w3.is_connected():
                return w3
            raise ConnectionError("Failed to connect to Ethereum node")
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(2 ** attempt)  # Exponential backoff
    return None

w3 = init_web3()
chain_id = int(os.environ.get('CHAIN_ID', 11155111))  # Default to Sepolia testnet

# Smart contract source code
CONTRACT_SOURCE = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AITaskManager {
    address public owner;
    mapping(bytes32 => Task) public tasks;
    
    struct Task {
        address agent;
        string input;
        string result;
        bool completed;
    }
    
    event TaskCreated(bytes32 taskId, address agent, string input);
    event TaskCompleted(bytes32 taskId, string result);
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    function createTask(bytes32 taskId, address agent, string memory input) public onlyOwner {
        require(tasks[taskId].agent == address(0), "Task already exists");
        tasks[taskId] = Task(agent, input, "", false);
        emit TaskCreated(taskId, agent, input);
    }
    
    function completeTask(bytes32 taskId, string memory result) public {
        require(tasks[taskId].agent == msg.sender, "Not assigned agent");
        require(!tasks[taskId].completed, "Task already completed");
        tasks[taskId].result = result;
        tasks[taskId].completed = true;
        emit TaskCompleted(taskId, result);
    }
    
    function getTask(bytes32 taskId) public view returns (address, string memory, string memory, bool) {
        Task memory task = tasks[taskId];
        return (task.agent, task.input, task.result, task.completed);
    }
}
"""

def compile_contract():
    try:
        compiled = compile_standard({
            "language": "Solidity",
            "sources": {"AITaskManager.sol": {"content": CONTRACT_SOURCE}},
            "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}}
        }, solc_version="0.8.0")
        return compiled['contracts']['AITaskManager.sol']['AITaskManager']['abi'], compiled['contracts']['AITaskManager.sol']['AITaskManager']['evm']['bytecode']['object']
    except Exception as e:
        raise ValueError(f"Contract compilation failed: {str(e)}")

def deploy_contract(user_id):
    try:
        if not w3:
            raise ConnectionError("Web3 not initialized")
        
        abi, bytecode = compile_contract()
        contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        private_key = os.environ.get('ETH_PRIVATE_KEY')
        if not private_key:
            raise ValueError("ETH_PRIVATE_KEY not set")
        
        account = w3.eth.account.from_key(private_key)
        nonce = w3.eth.get_transaction_count(account.address)
        
        # Estimate gas with buffer
        gas_estimate = contract.constructor().estimate_gas() * 1.2
        tx = contract.constructor().build_transaction({
            'from': account.address,
            'nonce': nonce,
            'gas': int(gas_estimate),
            'gasPrice': w3.eth.gas_price * 1.1,  # 10% buffer
            'chainId': chain_id
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        if tx_receipt.status == 0:
            raise RuntimeError("Transaction failed")
            
        contract_address = tx_receipt.contractAddress
        store_shared_data(f'contract_{user_id}', {'address': contract_address, 'abi': abi}, user_id)
        log_audit(user_id, 'deploy_contract', {'contract_address': contract_address})
        return {'status': 'success', 'contract_address': contract_address}
    except Exception as e:
        log_audit(user_id, 'deploy_contract', {'error': str(e)})
        return {'status': 'error', 'error': str(e)}

def handle_request(data, user_id):
    try:
        task = data.get('task')
        task_id = data.get('task_id', f"blockchain_{int(time.time())}")
        response = {"status": "success", "result": {}, "task_id": task_id}

        if not w3:
            return {'status': 'error', 'error': 'Web3 connection failed'}

        contract_data = get_shared_data(f'contract_{user_id}', user_id)
        if not contract_data and task != 'deploy':
            return {'status': 'error', 'error': 'No contract deployed'}

        if task == 'deploy':
            response['result'] = deploy_contract(user_id)
            return response

        contract = w3.eth.contract(address=contract_data['address'], abi=contract_data['abi'])
        private_key = os.environ.get('ETH_PRIVATE_KEY')
        if not private_key:
            return {'status': 'error', 'error': 'ETH_PRIVATE_KEY not set'}
        
        account = w3.eth.account.from_key(private_key)
        task_hash = w3.keccak(text=f"{task_id}:{user_id}")

        if task == 'create_task':
            agent_address = data.get('agent_address')
            if not w3.is_address(agent_address):
                return {'status': 'error', 'error': 'Invalid agent address'}
            input_data = data.get('input', '')
            nonce = w3.eth.get_transaction_count(account.address)
            gas_estimate = contract.functions.createTask(task_hash, agent_address, input_data).estimate_gas() * 1.2
            tx = contract.functions.createTask(task_hash, agent_address, input_data).build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': int(gas_estimate),
                'gasPrice': w3.eth.gas_price * 1.1,
                'chainId': chain_id
            })
            signed_tx = w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            response['result'] = {'tx_hash': tx_hash.hex()}

        elif task == 'complete_task':
            result = data.get('result', '')
            nonce = w3.eth.get_transaction_count(account.address)
            gas_estimate = contract.functions.completeTask(task_hash, result).estimate_gas() * 1.2
            tx = contract.functions.completeTask(task_hash, result).build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': int(gas_estimate),
                'gasPrice': w3.eth.gas_price * 1.1,
                'chainId': chain_id
            })
            signed_tx = w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            response['result'] = {'tx_hash': tx_hash.hex()}

        elif task == 'get_task':
            task_data = contract.functions.getTask(task_hash).call()
            response['result'] = {
                'agent': task_data[0],
                'input': task_data[1],
                'result': task_data[2],
                'completed': task_data[3]
            }

        store_shared_data(f'blockchain_{task_id}', response['result'], user_id)
        log_audit(user_id, f"blockchain_{task}", response)
        return response
    except Exception as e:
        log_audit(user_id, 'blockchain_task', {'error': str(e)})
        return {'status': 'error', 'error': str(e)}