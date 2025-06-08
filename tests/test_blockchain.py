import pytest
from src.Blockchain.SmartContractManager import handle_request

def test_deploy_contract(mocker):
    mocker.patch('web3.Web3')
    result = handle_request({'task': 'deploy'}, 'user123')
    assert 'contract_address' in result['result']

def test_create_task(mocker):
    mocker.patch('web3.Web3')
    result = handle_request({'task': 'create_task', 'agent_address': '0x' + '0' * 40, 'input': 'test'}, 'user123')
    assert 'tx_hash' in result['result']