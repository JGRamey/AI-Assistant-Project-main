import time
import os
from utils import log_audit, store_shared_data, get_config
from blockchain import SmartContractManager


def handle_contract_request(data, user_id):
    """Handles smart contract related tasks."""
    try:
        rpc_url = get_config('ETH_RPC_URL') or os.environ.get('ETH_RPC_URL')
        contract_address = get_config('CONTRACT_ADDRESS') or '0xYourContract'
        contract_abi = get_config('CONTRACT_ABI') or 'Your ABI'

        if not rpc_url:
            return {"status": "error", "result": "ETH_RPC_URL not configured"}

        manager = SmartContractManager(
            rpc_url=rpc_url,
            contract_address=contract_address,
            abi=contract_abi
        )

        task = data.get('task')
        task_id = data.get('task_id', f"smart_contract_{int(time.time())}")
        response = {"status": "success", "result": {}, "task_id": task_id}
        result = {}

        if task == "deploy_contract":
            result = {"status": "error", "message": "Deploy contract not implemented"}

        elif task == "execute_task":
            code = data.get('code', '')
            result = manager.store_data({'code': code, 'task_id': task_id}, user_id)

        elif task == "get_task_result":
            result = manager.retrieve_data({'file_id': data.get('task_id')}, user_id)

        response["result"] = result
        store_shared_data(
            f'smart_contract_{task_id}', response["result"], user_id
        )
        log_audit(user_id, f"smart_contract_{task}", response)
        return response
    except Exception as e:
        log_audit(user_id, "smart_contract_task", {"error": str(e)})
        return {"status": "error", "result": str(e)}