# Meta Integration Test Scenarios

## Integration and Meta-Validation Scenarios

### Integration Test: Complete Decision Matrix Flow ✅
**Test**: Validate that all modules work together following the decision matrix order
```python
# File that should trigger multiple validation steps:
# 1. File creation check (pass - not duplicate)
# 2. Comment check (pass - no implementation awareness)
# 3. Test framework check (pass - using pytest)
# 4. Mock patterns check (pass - using @patch)
# 5. Implementation review (pass - real business logic)
# 6. Business logic check (pass - works for any input)
# 7. TDD flow check (pass - proper test structure)

@patch('payment.gateway')
def test_payment_processing(mock_gateway):
    """Test payment processing with different methods."""
    mock_gateway.process.return_value = {"status": "success"}

    result = process_payment(100, "credit")

    assert result["status"] == "success"
    mock_gateway.process.assert_called_once_with(100, "credit")
```
**Expected**: Should ALLOW - follows all module requirements

### Error Template Validation Test ❌
**Test**: Verify error messages follow standard format
```python
# This should trigger a fake implementation error with proper template
def authenticate_user(username, password):
    return "always_authenticated"  # Hardcoded fake
```
**Expected**: Error should follow format: `❌ [VIOLATION TYPE] - [SPECIFIC ISSUE] → [SUGGESTION]`

### Multi-Module Violation Test ❌
**Test**: File that violates multiple modules simultaneously
```python
# test_user_v2.py - Violates test-duplication when test_user.py exists
import unittest

class TestUserAuth(unittest.TestCase):  # Violates pytest standards
    def test_login(self):
        # This will fail until implemented  # Violates comment standards
        with patch('auth.service') as mock:  # Violates pytest mock patterns
            mock.return_value = "success"   # Violates fake implementation
            self.assertTrue(authenticate("user", "pass"))  # unittest assertion
```
**Expected**: Should trigger multiple violations with appropriate priority ordering

### Priority Ordering Validation ✅
**Test**: Verify that critical priority violations are caught first
```python
# Should catch test duplication (Priority 1) before pytest issues (Priority 5)
# If test_user.py exists, this should be blocked for duplication, not pytest issues
import unittest

class TestUser(unittest.TestCase):
    def test_something(self):
        pass
```
**Expected**: Should block with test duplication message, not unittest framework message

### Success Criteria Integration ✅
**Test**: Validate that all "Must Allow" scenarios from each module work together
```python
# Combines: Core TDD + Pytest + Backend Framework + Real Implementation
@pytest.mark.parametrize("user_type,expected", [
    ("admin", True),
    ("user", False),
])
@patch('auth.database')
def test_admin_access(mock_db, user_type, expected):
    """Test admin access control."""
    mock_db.get_user.return_value = User(type=user_type)

    result = check_admin_access("test_user")

    assert result == expected
    mock_db.get_user.assert_called_once_with("test_user")
```
**Expected**: Should ALLOW - combines all valid patterns from multiple modules

## Meta-Validation Requirements
- **Decision Matrix**: All modules follow proper validation order
- **Error Consistency**: All modules use standard error template format
- **Priority Enforcement**: Higher priority violations block lower priority checks
- **Integration Compatibility**: Modules work together without conflicts
- **Coverage Completeness**: All original INSTRUCTIONS_V1.md functionality preserved