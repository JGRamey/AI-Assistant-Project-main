import json
import time
from utils import log_audit, send_message, store_shared_data, get_shared_data, supabase

def handle_crm_request(data, user_id):
    try:
        task = data.get('task')
        task_id = data.get('task_id', f"crm_{int(time.time())}")
        response = {"status": "success", "result": {}, "task_id": task_id}

        if task == "add_contact":
            contact = data.get("contact", {})
            supabase.table('crm_contacts').insert({
                'user_id': user_id,
                'name': contact.get('name'),
                'email': contact.get('email'),
                'phone': contact.get('phone')
            }).execute()
            response["result"] = {"added": True}
        elif task == "list_contacts":
            contacts = supabase.table('crm_contacts').select('*').eq('user_id', user_id).execute()
            response["result"] = contacts.data
        elif task == "send_campaign":
            campaign = data.get("campaign", {})
            store_shared_data(f'crm_campaign_{task_id}', campaign, user_id)
            send_message({"campaign": campaign, "task_id": task_id}, "marketing_manager", user_id)
            response["result"] = {"sent": True}

        store_shared_data(f'crm_{task_id}', response["result"], user_id)
        log_audit(user_id, f"crm_{task}", response)
        return response
    except Exception as e:
        log_audit(user_id, "crm_task", {"error": str(e)})
        return {"status": "error", "result": str(e)}