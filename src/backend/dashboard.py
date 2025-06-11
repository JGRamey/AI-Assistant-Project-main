import os
import time
from typing import Dict, Any

from supabase import create_client, Client

def render_dashboard(data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """Render or update the dashboard with user data from Supabase."""
    try:
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        if not url or not key:
            return {'error': 'Supabase credentials not configured on the server.'}, 500
        supabase: Client = create_client(url, key)

        task = data.get('task')

        if task == 'view':
            # Fetch all data from Supabase tables for the user
            tasks_data = supabase.table('tasks').select('*').eq('user_id', user_id).execute().data
            portfolio_data = supabase.table('portfolios').select('*').eq('user_id', user_id).execute().data
            expenses_data = supabase.table('expenses').select('*').eq('user_id', user_id).execute().data
            notes_data = supabase.table('notes').select('*').eq('user_id', user_id).execute().data
            trades_data = supabase.table('trades').select('*').eq('user_id', user_id).execute().data
            budgets_data = supabase.table('budgets').select('*').eq('user_id', user_id).execute().data
            preferences_data = supabase.table('user_preferences').select('*').eq('user_id', user_id).execute().data

            dashboard_data = {
                "tasks": tasks_data,
                "portfolio": portfolio_data,
                "expenses": expenses_data,
                "notes": notes_data,
                "trades": trades_data,
                "budgets": budgets_data,
                "preferences": preferences_data[0] if preferences_data else {}
            }
            return dashboard_data

        elif task == 'update_preferences':
            preferences = data.get('preferences', {})
            if not isinstance(preferences, dict):
                return {"status": "error", "result": "Preferences must be a dictionary"}

            # Use on_conflict to avoid creating a new row if user_id already exists
            supabase.table('user_preferences').upsert({
                'user_id': user_id,
                'preferences': preferences,
                'updated_at': time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }, on_conflict='user_id').execute()

            return {'status': 'preferences_updated'}

        else:
            return {"status": "error", "result": f"Unknown task: {task}"}

    except Exception as e:
        # In a real app, you'd want more specific error logging
        return {'error': str(e)}


if __name__ == '__main__':
    pass
