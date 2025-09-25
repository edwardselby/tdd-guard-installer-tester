# Fake Implementation Detection Scenarios

## Phase 2: Fake Implementation Detection (Critical)

### Test 2.1: Hardcoded String Returns ❌
```python
def authenticate_user(username, password):
    return "authentication_successful"  # Different phrasing but still hardcoded
```
**Expected**: Block with "hardcoded return value" message

### Test 2.2: Magic Number Returns ❌
```python
def calculate_discount(price, customer_type):
    return 100  # Different magic number without logic
```
**Expected**: Block with "Magic numbers/booleans without logic"

### Test 2.3: Hardcoded List Returns ❌
```python
def get_user_permissions(user_id):
    return ['read', 'write', 'admin']  # Hardcoded list matching test expectations
```
**Expected**: Block with "Hardcoded lists matching test expectations"

### Test 2.4: Test-Specific Conditionals ❌
```python
def process_payment(amount, method):
    if amount >= 50.0 and method in ["credit", "debit"]:
        return {"status": "processed", "transaction_id": "txn_12345"}
    return {"status": "rejected"}
```
**Expected**: Block with "Test-specific conditionals"

### Test 2.5: Length-Based Test Logic ❌
```python
def validate_items(items):
    if len(items) == 3:
        return "valid"
    return "invalid"
```
**Expected**: Block with "Test-specific length checks"

### Test 2.6: User-Specific Logic ❌
```python
def check_permissions(user):
    if user.name == "testuser":
        return True
    return False
```
**Expected**: Block with "Test-specific object checks"

### Test 2.7: Mock Objects in Production ❌
```python
from unittest.mock import Mock

def get_database_connection():
    return Mock()  # Mock in production code
```
**Expected**: Block with "Mock objects in production code"

### Test 2.8: NotImplementedError for Tested Functionality ❌
```python
def calculate_tax(income):
    raise NotImplementedError()  # But tests expect this to work
```
**Expected**: Block with "NotImplementedError for tested functionality"

### Test 2.9: Variable-Disguised Hardcoding ❌
```python
def process_data(input_data):
    expected_result = "success"  # Disguised hardcoding
    processed_value = "processed"
    return expected_result
```
**Expected**: Block with sophisticated fake detection

### Test 2.10: Copy-Paste from Assertions ❌
```python
def get_user_data(user_id):
    return {"id": "507f1f77bcf86cd799439011", "name": "Test User"}  # Copied from test assertion
```
**Expected**: Block with fake implementation detection

### Test 2.11: Valid Business Logic ✅
```python
def calculate_discount(price, customer_type):
    discounts = {"GOLD": 0.20, "SILVER": 0.10, "BRONZE": 0.05}
    discount_rate = discounts.get(customer_type, 0)
    return price * (1 - discount_rate)
```
**Expected**: Should ALLOW - real business logic

### Test 2.12: Complex Algorithm Implementation ✅
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```
**Expected**: Should ALLOW - legitimate algorithm

## Success Criteria
- ❌ Block hardcoded returns, magic numbers, test-specific conditionals (19 scenarios)
- ❌ Block mock objects in production, NotImplementedError patterns
- ❌ Block variable-disguised hardcoding, copy-paste from assertions
- ✅ Allow real business logic implementations (2 scenarios)