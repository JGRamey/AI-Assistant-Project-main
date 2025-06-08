import json
import os
import time
import requests
from supabase import create_client, Client
from utils import log_audit, store_shared_data, get_shared_data

supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

def generate_mock_script(keywords, style="informal"):
    """Mock script generation (replace with Grok or other AI model in production)."""
    style_templates = {
        "informal": "Hey everyone, welcome back! Today, we're diving into {keywords}. Let's break it down!",
        "formal": "Greetings, viewers. In this video, we explore {keywords}. Here's a detailed overview.",
        "tutorial": "Welcome to this tutorial on {keywords}. Follow these steps to get started."
    }
    template = style_templates.get(style, style_templates["informal"])
    return {
        "title": f"Exploring {keywords}",
        "intro": template.format(keywords=keywords),
        "body": [
            f"Section 1: Introduction to {keywords}.",
            f"Section 2: Key benefits of {keywords}.",
            "Section 3: Practical applications.",
            "Conclusion: Wrap-up and next steps."
        ],
        "outro": "Thanks for watching! Subscribe for more content like this."
    }

def handle_script_request(data, user_id):
    try:
        task = data.get('task')
        task_id = data.get('task_id', f"script_{int(time.time())}")
        response = {"status": "success", "result": {}, "task_id": task_id}

        if task == "generate_script":
            keywords = data.get('keywords', '').strip()
            if not keywords:
                return {"status": "error", "result": "Keywords cannot be empty"}
            style = data.get('style', 'informal').lower()
            if style not in ["informal", "formal", "tutorial"]:
                return {"status": "error", "result": "Invalid style"}

            # Mock AI generation (replace with Grok API call in production)
            script = generate_mock_script(keywords, style)
            
            # Store script in Supabase
            supabase.table('scripts').insert({
                'user_id': user_id,
                'title': script['title'],
                'content': json.dumps(script),
                'keywords': keywords,
                'style': style,
                'created_at': time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }).execute()
            
            response["result"] = script
            store_shared_data(f'script_{task_id}', script, user_id)

        elif task == "fetch_scripts":
            scripts = supabase.table('scripts').select('id, title, keywords, style, created_at').eq('user_id', user_id).execute()
            response["result"] = scripts.data or []

        elif task == "get_script":
            script_id = data.get('script_id')
            if not script_id:
                return {"status": "error", "result": "Script ID required"}
            script = supabase.table('scripts').select('*').eq('id', script_id).eq('user_id', user_id).single().execute()
            if not script.data:
                return {"status": "error", "result": "Script not found"}
            response["result"] = json.loads(script.data['content'])

        elif task == "suggest_improvements":
            script_content = data.get('script_content', {})
            if not script_content:
                return {"status": "error", "result": "Script content required"}
            # Mock suggestion (replace with Grok API call)
            suggestions = {
                "title": f"Enhanced: {script_content.get('title', 'Untitled')}",
                "improvements": [
                    "Add a call-to-action in the intro.",
                    "Include more examples in the body.",
                    "Shorten the outro for impact."
                ]
            }
            response["result"] = suggestions
            store_shared_data(f'script_suggestions_{task_id}', suggestions, user_id)

        log_audit(user_id, f"script_{task}", response)
        return response
    except Exception as e:
        log_audit(user_id, "script_task", {"error": str(e)})
        return {"status": "error", "result": str(e)}