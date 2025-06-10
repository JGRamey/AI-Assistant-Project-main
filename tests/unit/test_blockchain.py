import pytest
from unittest.mock import patch, MagicMock
import json
from blockchain import SmartContractManager

# Mock configuration values
MOCK_RPC_URL = "http://mock-rpc.com"
MOCK_CONTRACT_ADDRESS = "0xMockContractAddress"
MOCK_ABI = '[]'
MOCK_USER_ID = "0xMockUserAddress"

@pytest.fixture
def manager():
    """Fixture to create a SmartContractManager instance with a mocked Web3 dependency."""
    with patch('blockchain.Web3') as mock_web3_class:
        mock_w3_instance = MagicMock()
        mock_contract_instance = MagicMock()
        mock_w3_instance.eth.contract.return_value = mock_contract_instance
        mock_web3_class.return_value = mock_w3_instance

        # Instantiate the manager with mock config
        manager_instance = SmartContractManager(
            rpc_url=MOCK_RPC_URL,
            contract_address=MOCK_CONTRACT_ADDRESS,
            abi=MOCK_ABI
        )
        # Attach mocks to the instance for easy access in tests
        manager_instance.mock_w3 = mock_w3_instance
        manager_instance.mock_contract = mock_contract_instance
        yield manager_instance

@patch('blockchain.encrypt_data')
def test_store_data(mock_encrypt_data, manager):
    """Test the store_data method of SmartContractManager."""
    # Arrange
    mock_encrypt_data.return_value = b'encrypted_data'
    tx_hash = '0x12345'
    manager.mock_contract.functions.storeFile().transact.return_value = tx_hash.encode('utf-8')
    manager.mock_w3.eth.wait_for_transaction_receipt.return_value = {'status': 1}
    
    data_to_store = {'key': 'value'}
    
    # Act
    result = manager.store_data(data_to_store, MOCK_USER_ID)
    
    # Assert
    mock_encrypt_data.assert_called_once_with(json.dumps(data_to_store))
    manager.mock_contract.functions.storeFile.assert_called_once_with(b'encrypted_data')
    manager.mock_contract.functions.storeFile().transact.assert_called_once_with({'from': MOCK_USER_ID})
    manager.mock_w3.eth.wait_for_transaction_receipt.assert_called_once_with(tx_hash.encode('utf-8'))
    assert result['status'] == 'stored'
    assert result['tx_hash'] == tx_hash.encode('utf-8').hex()

@patch('blockchain.decrypt_data')
def test_retrieve_data(mock_decrypt_data, manager):
    """Test the retrieve_data method of SmartContractManager."""
    # Arrange
    file_id = 'file123'
    encrypted_data_from_contract = b'encrypted_data_from_contract'
    decrypted_data_dict = {'key': 'retrieved_value'}
    
    manager.mock_contract.functions.getFile().call.return_value = encrypted_data_from_contract
    mock_decrypt_data.return_value = json.dumps(decrypted_data_dict)
    
    # Act
    result = manager.retrieve_data({'file_id': file_id}, MOCK_USER_ID)
    
    # Assert
    manager.mock_contract.functions.getFile.assert_called_once_with(file_id)
    manager.mock_contract.functions.getFile().call.assert_called_once()
    mock_decrypt_data.assert_called_once_with(encrypted_data_from_contract)
    assert result['data'] == decrypted_data_dict

@patch('blockchain.log_audit')
def test_store_data_failure(mock_log_audit, manager):
    """Test store_data failure handling."""
    # Arrange
    manager.mock_contract.functions.storeFile().transact.side_effect = Exception("Blockchain error")
    
    # Act
    result = manager.store_data({'key': 'value'}, MOCK_USER_ID)
    
    # Assert
    assert 'error' in result
    assert result['error'] == "Blockchain error"
    mock_log_audit.assert_called_once()
    args, _ = mock_log_audit.call_args
    assert args[0] == MOCK_USER_ID
    assert args[1] == 'blockchain_storage'
    assert 'error' in args[2]
    assert args[2]['error'] == "Blockchain error"