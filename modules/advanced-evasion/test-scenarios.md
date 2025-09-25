# Advanced Evasion Test Scenarios

## Phases 7-12: Edge Cases, Evasion, Stress Testing

### Phase 7: Edge Cases & Evasion

#### Test 7.1: Mixed Violations ❌
```python
def test_complex_scenario():
    # RED PHASE - should fail initially  <- Comment violation
    def fake_implementation():
        return "hardcoded_result"  # <- Fake implementation

    result = fake_implementation()
    assert result == "hardcoded_result"
```
**Expected**: Block with multiple violation detection

#### Test 7.2: Subtle Evasion ❌
```python
def test_authentication():
    # This function will not work initially  <- Subtle phase marking
    # Implementation status: pending        <- Evasion attempt
    result = auth_function("test", "pass")
    assert result == True
```
**Expected**: Block with evasion detection

### Phase 10: Advanced Edge Cases

#### Test 10.1: Word-Form Test Name Variations ❌
```python
def test_process_payment():
    """Test payment processing."""
    assert process_payment(100, "credit") == "success"

def test_payment_processing():
    """Test the payment processing functionality."""
    assert process_payment(200, "debit") == "success"
```
**Expected**: Block with "Word-form variation: test_process_payment + test_payment_processing test same functionality"

#### Test 10.2: Sophisticated Variable-Disguised Fakes ❌
```python
def authenticate_user_advanced(username, password):
    # Variables to disguise hardcoding
    expected_result = "success"
    processed_value = "authenticated"
    status_code = expected_result
    return status_code
```
**Expected**: Block with "Variable-disguised fake implementation"

### Phase 11: Borderline Cases

#### Test 11.1: Legitimate Constants vs Hardcoding ❌/✅
```python
def calculate_tax(income):
    TAX_RATE = 0.20  # Is this legitimate constant or hardcoded test value?
    return income * TAX_RATE
```
**Expected**: Borderline case - depends on context and usage patterns

#### Test 11.2: Complex Realistic Business Logic ✅
```python
def calculate_shipping_cost(weight, distance, priority):
    base_rate = 5.00
    weight_multiplier = weight * 0.50
    distance_multiplier = distance * 0.02
    priority_multiplier = 1.5 if priority == "express" else 1.0
    return (base_rate + weight_multiplier + distance_multiplier) * priority_multiplier
```
**Expected**: Should ALLOW - legitimate complex business logic

### Phase 12: Sophisticated Evasion

#### Test 12.1: Multi-Level Indirection ❌
```python
def authenticate_user(username, password):
    return get_auth_result()

def get_auth_result():
    return fetch_auth_status()

def fetch_auth_status():
    return "authenticated"  # Hidden 3 levels deep
```
**Expected**: Block with sophisticated indirection detection

#### Test 12.2: Configuration File Abuse ❌
```python
# config.py
VALID_RESPONSES = {
    "auth_success": "user_authenticated",
    "payment_success": "payment_processed"
}

# implementation.py
from config import VALID_RESPONSES

def authenticate_user(username, password):
    return VALID_RESPONSES["auth_success"]  # Hardcoding via config
```
**Expected**: Block with configuration-disguised hardcoding

#### Test 12.3: Method Chaining Evasion ❌
```python
class ResponseBuilder:
    def success(self):
        self._status = "success"
        return self

    def with_data(self, data):
        self._data = data
        return self

    def build(self):
        return {"status": self._status, "data": self._data}

def process_request(data):
    return ResponseBuilder().success().with_data("processed").build()  # Disguised fake
```
**Expected**: Block with method chaining fake detection

### Phase 8: Error Quality Validation & Phase 9: Stress Testing

#### Test 8.1: Clear Error Messages
When violations occur, verify error messages include:
- **Issue**: What was problematic about the code
- **Why blocked**: Explanation of why this violates TDD principles
- **Suggestion**: Concrete alternative approach
- **Example**: Show better implementation if applicable

#### Test 9.1: Large File Handling
Test files with:
- 20+ test functions
- Complex nested class structures
- Large comment blocks and docstrings
- Mixed legitimate and violation patterns

## Success Criteria
- ❌ Block mixed violations, evasion attempts (8+ scenarios)
- ❌ Block sophisticated indirection, configuration abuse (4+ scenarios)
- ❌ Block method chaining evasion, word-form variations (4+ scenarios)
- ✅ Allow complex legitimate business logic (2+ scenarios)
- **Error Quality**: All violations include constructive guidance
- **Stress Testing**: Handle large, complex files appropriately