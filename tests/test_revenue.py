import pytest
from src.platform.finances.revenue import handle_revenue_request

def test_fetch_sales(mocker):
    mocker.patch('stripe.Charge.list', return_value={'data': [{'amount': 10000}]})
    result = handle_revenue_request({'task': 'fetch_sales'}, 'user123')
    assert 'total' in result['result']
    assert result['result']['total'] == 100.0

def test_financial_report(mocker):
    mocker.patch('supabase.table', return_value={'select': lambda: {'eq': lambda x, y: {'execute': lambda: {'data': [{'amount': 100}]}}}})
    mocker.patch('src.platform.finances.revenue.financial_handle', return_value={'result': [{'amount': 50}]})
    result = handle_revenue_request({'task': 'generate_financial_report'}, 'user123')
    assert 'net_profit' in result['result']