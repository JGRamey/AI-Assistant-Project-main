import pytest
from unittest.mock import patch
import json
from utils import log_audit, store_shared_data, get_shared_data


@pytest.fixture
def setup_log_file(tmp_path):
    log_file = tmp_path / "app.log"
    with patch("utils.log_utils.LOG_FILE", str(log_file)):
        yield log_file


@pytest.fixture
def setup_storage_file(tmp_path):
    storage_file = tmp_path / "shared_data.json"
    with open(storage_file, 'w') as f:
        json.dump({}, f)
    with patch("utils.log_utils.STORAGE_PATH", str(storage_file)):
        yield storage_file


def test_log_audit(setup_log_file):
    log_audit("user123", "revenue_event", {"amount": 100, "currency": "USD"})
    with open(setup_log_file, "r") as f:
        log_content = f.read()
    assert "user123" in log_content
    assert "revenue_event" in log_content
    assert "amount: 100" in log_content


def test_store_shared_data(setup_storage_file):
    store_shared_data("revenue_june", {"month": "June", "total": 1000})
    data = get_shared_data("revenue_june")
    assert data["month"] == "June"
    assert data["total"] == 1000