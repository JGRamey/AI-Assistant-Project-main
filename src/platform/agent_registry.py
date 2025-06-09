from agents import (
    coding_agent, email_agent, trading_agent, priority_agent, news_agent, alert_agent,
    portfolio_agent, crm_agent, notes_agent, time_agent, sentiment_agent, snippet_agent,
    stress_agent, social_agent, learning_agent, voice_agent, key_agent,
    journal_agent, update_agent, smart_contract_ai_agent, Financial_Agent
)
from blockchain import SmartContractManager
from platform.content import script_generator
from platform.social import post_scheduler
from platform.marketing import newsletter_automation
from platform.finances import revenue
from platform.analytics import youtube_analytics
from dashboard import render_dashboard
from workflows import execute_workflow

# This registry maps action names to their handler functions
HANDLER_REGISTRY = {
    # Agent actions
    'code': coding_agent.handle_code_request,
    'email': email_agent.handle_email_request,
    'trade': trading_agent.handle_trade_request,
    'priority': priority_agent.handle_priority_request,
    'news': news_agent.handle_news_request,
    'alert': alert_agent.handle_alert_request,
    'portfolio': portfolio_agent.handle_portfolio_request,
    'crm': crm_agent.handle_crm_request,
    'notes': notes_agent.handle_notes_request,
    'time': time_agent.handle_time_request,
    'sentiment': sentiment_agent.handle_sentiment_request,
    'snippet': snippet_agent.handle_snippet_request,
    'stress': stress_agent.handle_stress_request,
    'expense': Financial_Agent.handle_financial_request,
    'social': social_agent.handle_social_request,
    'learn': learning_agent.handle_learning_request,
    'voice': voice_agent.handle_voice_request,
    'key': key_agent.handle_key_request,
    'journal': journal_agent.handle_journal_request,
    'update': update_agent.handle_update_request,
    'smart_contract': smart_contract_ai_agent.handle_contract_request,
    'financial_plan': Financial_Agent.handle_financial_request,

    # Platform and other actions
    'coordinate': execute_workflow,
    'dashboard': render_dashboard,
    'store': lambda data, user_id: SmartContractManager.handle_request({'task': 'create_task', **data}, user_id),
    'retrieve': lambda data, user_id: SmartContractManager.handle_request({'task': 'get_task', **data}, user_id),
    'content_script': script_generator.handle_script_request,
    'social_post': post_scheduler.handle_post_request,
    'newsletter': newsletter_automation.handle_newsletter_request,
    'token_manage': revenue.handle_revenue_request,
    'youtube_analytics': youtube_analytics.handle_analytics_request,
    'blockchain_token': SmartContractManager.handle_request,
}

def get_handler(action_name):
    return HANDLER_REGISTRY.get(action_name)

# This registry maps agent module names to the modules themselves
# This is needed for the SQS and delegate actions that refer to agents by name
AGENT_MODULES = {
    'coding_agent': coding_agent, 'email_agent': email_agent, 'trading_agent': trading_agent,
    'priority_agent': priority_agent, 'news_agent': news_agent, 'alert_agent': alert_agent,
    'portfolio_agent': portfolio_agent, 'crm_agent': crm_agent, 'notes_agent': notes_agent,
    'time_agent': time_agent, 'sentiment_agent': sentiment_agent, 'snippet_agent': snippet_agent,
    'stress_agent': stress_agent, 'social_agent': social_agent, 'learning_agent': learning_agent,
    'voice_agent': voice_agent, 'key_agent': key_agent, 'journal_agent': journal_agent,
    'update_agent': update_agent, 'smart_contract_ai_agent': smart_contract_ai_agent,
    'Financial_Agent': Financial_Agent
}

def get_agent_module(agent_name):
    return AGENT_MODULES.get(agent_name)
