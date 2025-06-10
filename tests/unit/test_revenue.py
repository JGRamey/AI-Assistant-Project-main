import pytest
from unittest.mock import patch, MagicMock
from utils import log_audit, store_shared_data, get_shared_data

@patch('utils.helpers.supabase')
@patch('utils.helpers.logger')
def test_log_audit(
    mock_logger: MagicMock,
    mock_supabase: MagicMock,
) -> None:
    """Test that log_audit calls Supabase and the logger.

    This test verifies that the log_audit function correctly logs to both
    the logger and Supabase database.

    Args:
        mock_logger: Mocked logger instance
        mock_supabase: Mocked Supabase client
    """
    # Arrange
    mock_supabase.table.return_value.insert.return_value.execute.return_value = MagicMock()

    # Act
    log_audit("user123", "test_action", {"detail": "some_detail"})
    
    # Assert
    mock_logger.info.assert_called_once_with(
        "Audit log: user=user123, action=test_action, details={'detail': 'some_detail'}"
    )
    mock_supabase.table.assert_called_once_with('audit_logs')
    mock_supabase.table().insert.assert_called_once()
    insert_args, _ = mock_supabase.table().insert.call_args
    assert insert_args[0]['user_id'] == 'user123'
    assert insert_args[0]['action'] == 'test_action'

@patch('utils.helpers.dynamodb')
def test_store_and_get_shared_data(
    mock_dynamodb: MagicMock,
) -> None:
    """Test storing and retrieving data from DynamoDB.

    This test verifies that shared data can be stored and retrieved
    correctly from DynamoDB.

    Args:
        mock_dynamodb: Mocked DynamoDB client
    """
    mock_table = MagicMock()
    mock_dynamodb.Table.return_value = mock_table

    # Test storing data
    user_id = "user456"
    key = "test_key"
    value = {"data": "some_value"}
    store_shared_data(key, value, user_id)

    mock_dynamodb.Table.assert_called_with('SharedData')
    mock_table.put_item.assert_called_once()
    args, kwargs = mock_table.put_item.call_args
    assert kwargs['Item']['key'] == f'{user_id}:{key}'
    assert kwargs['Item']['value'] == '{"data": "some_value"}'

    # Test retrieving data
    mock_table.get_item.return_value = {
        'Item': {
            'key': f'{user_id}:{key}',
            'value': '{"data": "retrieved_value"}'
        }
    }
    retrieved_data = get_shared_data(key, user_id)
    
    mock_table.get_item.assert_called_with(Key={'key': f'{user_id}:{key}'})
    assert retrieved_data == {"data": "retrieved_value"}