import json
import time
from utils import log_audit, store_shared_data, send_message
from Blockchain import SmartContractManager

def handle_request(data, user_id):
    try:
        task = data.get('task')
        task_id = data.get('task_id', f"smart_contract_{int(time.time())}")
        response = {"status": "success", "result": {}, "task_id": task_id}

        if task == "deploy_contract":
            result = SmartContractManager.handle_request({'task': 'deploy'}, user_id)
            response["result"] = result['result']

        elif task == "execute_task":
            code = data.get('code', '')
            agent_address = data.get('agent_address', '0x' + '0' * 40)
            result = SmartContractManager.handle_request({
                'task': 'create_task',
                'agent_address': agent_address,
                'input': code,
                'task_id': task_id
            }, user_id)
            response["result"] = result['result']

        elif task == "get_task_result":
            result = SmartContractManager.handle_request({
                'task': 'get_task',
                'task_id': data.get('task_id', task_id)
            }, user_id)
            response["result"] = result['result']

        store_shared_data(f'smart_contract_{task_id}', response["result"], user_id)
        log_audit(user_id, f"smart_contract_{task}", response)
        return response
    except Exception as e:
        log_audit(user_id, "smart_contract_task", {"error": str(e)})
        return {"status": "error", "result": str(e)}