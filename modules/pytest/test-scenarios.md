# Pytest Standards Test Scenarios

## Phase 13: Pytest Standards Enforcement

### Test 13.1: Unittest Framework Usage ❌ (Should BLOCK)
**Issue**: AI agents attempt to use unittest.TestCase classes instead of pytest flat functions
```python
import unittest

class TestUserAuthentication(unittest.TestCase):
    def test_user_login(self):
        self.assertTrue(authenticate_user("user", "pass"))
```
**Expected**: Block with "❌ Unittest framework - Using class TestSomething(unittest.TestCase) → Use pytest flat functions: def test_something():"

### Test 13.2: Context Manager Mocking ❌ (Should BLOCK)
**Issue**: Using 'with patch()' instead of @patch decorator
```python
def test_database_query():
    with patch('app.models.database.connect') as mock_connect:
        mock_connect.return_value = "connection"
        result = get_user_data(123)
        assert result["id"] == 123
```
**Expected**: Block with "❌ Context manager mocking - Using 'with patch()' pattern → Use @patch decorator above function definition"

### Test 13.3: Shared Mocks in Test File ❌ (Should BLOCK)
**Issue**: Shared mocks defined in individual test files instead of conftest.py
```python
# test_user_service.py
from unittest.mock import Mock
shared_database_mock = Mock()  # Should be in conftest.py

def test_user_creation():
    result = create_user("test", db=shared_database_mock)
    assert result is not None
```
**Expected**: Block with "❌ Shared mocks in test file - Move shared_database_mock to conftest.py"

### Test 13.4: Multiple Similar Tests Without Parameterization ❌ (Should BLOCK)
**Issue**: Creating separate test functions for similar test cases
```python
def test_discount_gold_customer():
    result = calculate_discount(100, "GOLD")
    assert result == 80

def test_discount_silver_customer():
    result = calculate_discount(100, "SILVER")
    assert result == 90
```
**Expected**: Block with "❌ Multiple similar tests - Use @pytest.mark.parametrize for similar test cases"

### Test 13.5: Valid Pytest with Decorator Mocking ✅ (Should ALLOW)
**Issue**: Proper pytest patterns should be allowed
```python
@patch('app.services.database')
def test_user_registration(mock_db):
    mock_db.save.return_value = True
    result = register_user("test@example.com", "password")
    assert result["status"] == "success"
    mock_db.save.assert_called_once()
```
**Expected**: Should ALLOW - proper pytest with decorator mocking

### Test 13.6: Valid Parameterized Test ✅ (Should ALLOW)
**Issue**: Proper parameterized tests should be allowed
```python
@pytest.mark.parametrize("amount,method,expected", [
    (100, "credit", 3.00),
    (100, "debit", 1.50),
])
def test_payment_fee_calculation(amount, method, expected):
    result = calculate_fee(amount, method)
    assert result == expected
```
**Expected**: Should ALLOW - proper parameterized test

## Success Criteria
- ❌ Block unittest.TestCase classes and self.assert* methods (4 scenarios)
- ❌ Block context manager mocking (with patch()) instead of @patch decorators
- ❌ Block shared mocks in test files instead of conftest.py
- ❌ Block multiple similar tests without @pytest.mark.parametrize
- ✅ Allow proper pytest patterns with decorator mocking and parameterization (2 scenarios)