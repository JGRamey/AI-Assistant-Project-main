import os
from . import (
    priority_agent,
    news_agent,
    alert_agent,
    key_agent,
    update_agent
)
from .communication import (
    email_agent,
    social_agent,
    texts_agent,
    notes_agent,
    voice_agent
)
from .coding import (
    coding_agent
)
from .financial import (
    trading_agent,
    portfolio_agent,
    financial_agent
)

from src.dashboard.dashboard import render_dashboard
from src.workflows import execute_workflow
from src.utils import get_config





# This registry maps action names to their handler functions
HANDLER_REGISTRY = {
    # Agent actions
    'code': coding_agent.handle_code_request,
    'email': email_agent.handle_email_request,
    'text': texts_agent.handle_texts_request,
    'trade': trading_agent.handle_trade_request,
    'priority': priority_agent.handle_priority_request,
    'news': news_agent.handle_news_request,
    'alert': alert_agent.handle_alert_request,
    'portfolio': portfolio_agent.handle_portfolio_request,
    'notes': notes_agent.handle_notes_request,
    'expense': financial_agent.handle_request,
    'social': social_agent.handle_social_request,
    'voice': voice_agent.handle_voice_request,
    'key': key_agent.handle_key_request,
    'update': update_agent.handle_update_request,
    'financial_plan': financial_agent.handle_request,

    # Platform and other actions
    'coordinate': execute_workflow,
    'dashboard': render_dashboard,
}


def get_handler(action_name):
    """Retrieve handler function for a given action."""
    return HANDLER_REGISTRY.get(action_name)


# This registry maps agent module names to the modules themselves
# This is needed for the SQS and delegate actions that refer to agents by name
AGENT_MODULES = {
    'coding_agent': coding_agent,
    'trading_agent': trading_agent,
    'priority_agent': priority_agent,
    'news_agent': news_agent,
    'alert_agent': alert_agent,
    'portfolio_agent': portfolio_agent,
    'notes_agent': notes_agent,
    'voice_agent': voice_agent,
    'key_agent': key_agent,
    'update_agent': update_agent,
    'financial_agent': financial_agent,
    'email_agent': email_agent,
    'social_agent': social_agent,
    'texts_agent': texts_agent
}


def get_agent_module(agent_name):
    """Retrieve agent module by name."""
    return AGENT_MODULES.get(agent_name)


# This registry maps agent names to their handler functions
AGENT_HANDLERS = {
    'coding_agent': coding_agent.handle_code_request,
    'email_agent': email_agent.handle_email_request,
    'texts_agent': texts_agent.handle_texts_request,
    'trading_agent': trading_agent.handle_trade_request,
    'priority_agent': priority_agent.handle_priority_request,
    'news_agent': news_agent.handle_news_request,
    'alert_agent': alert_agent.handle_alert_request,
    'portfolio_agent': portfolio_agent.handle_portfolio_request,
    'notes_agent': notes_agent.handle_notes_request,
    'financial_agent': financial_agent.handle_request,
    'social_agent': social_agent.handle_social_request,
    'voice_agent': voice_agent.handle_voice_request,
    'key_agent': key_agent.handle_key_request,
    'update_agent': update_agent.handle_update_request
}


def get_agent_handler(agent_name):
    """Retrieve handler function for a given agent."""
    return AGENT_HANDLERS.get(agent_name)


if __name__ == '__main__':
    pass
