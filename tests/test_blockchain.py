import pytest
from Blockchain import SmartContractManager
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_web3():
    with patch('Blockchain.SmartContractManager.Web3') as mock_web3:
        mock_instance = MagicMock()
        mock_web3.return_value = mock_instance
        mock_instance.is_connected.return_value = True
        mock_instance.eth.account.from_key.return_value = MagicMock(address='0xMockAddress')
        mock_instance.eth.get_transaction_count.return_value = 1
        mock_instance.eth.contract.return_value.constructor.return_value.estimate_gas.return_value = 100000
        mock_instance.eth.contract.return_value.constructor.return_value.build_transaction.return_value = {'nonce': 1, 'gas': 100000}
        mock_instance.eth.account.sign_transaction.return_value = MagicMock(rawTransaction='mock-tx')
        mock_instance.eth.send_raw_transaction.return_value = 'mock-tx-hash'
        mock_instance.eth.wait_for_transaction_receipt.return_value = {'status': 1, 'contractAddress': '0xContractAddress'}
        yield mock_instance

@pytest.fixture
def smart_contract_manager(mock_web3):
    manager = SmartContractManager()
    manager.w3 = mock_web3
    return manager

def test_compile_contract(smart_contract_manager):
    contract_source = """
    pragma solidity ^0.8.0;
    contract TestContract {
        uint public value;
        constructor(uint _value) {
            value = _value;
        }
    }
    """
    abi, bytecode = smart_contract_manager.compile_contract(contract_source, "TestContract")
    assert isinstance(abi, list)
    assert isinstance(bytecode, str)
    assert len(bytecode) > 0

def test_deploy_contract(smart_contract_manager, mock_web3):
    contract_source = """
    pragma solidity ^0.8.0;
    contract TestContract {
        uint public value;
        constructor(uint _value) {
            value = _value;
        }
    }
    """
    abi, bytecode = smart_contract_manager.compile_contract(contract_source, "TestContract")
    address = smart_contract_manager.deploy_contract(abi, bytecode, [42])
    assert address == "0xContractAddress"
    mock_web3.eth.send_raw_transaction.assert_called()