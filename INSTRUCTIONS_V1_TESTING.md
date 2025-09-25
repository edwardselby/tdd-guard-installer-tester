# TDD Guard Comprehensive Testing Documentation

## Overview
This document outlines systematic testing of TDD Guard validation rules to ensure comprehensive coverage of all blocking scenarios and edge cases. Each test case includes expected outcomes, specific code examples, and success criteria.

---

## Phase 1: Core TDD Workflow Validation

### Test 1.1: Single Test Creation ✅
**Should ALLOW**: Creating one test at a time following TDD principles
```python
def test_task_creation_basic():
    """Test basic task creation functionality."""
    task = Task.create("Test Task")
    assert task['title'] == "Test Task"
```
**Expected**: Should pass without blocking

### Test 1.2: Multiple Test Functions ❌
**Should BLOCK**: Adding multiple test functions simultaneously
```python
def test_first_function():
    assert True

def test_second_function():
    assert True
```
**Expected**: Block with "Multiple test addition violation"

### Test 1.3: Implementation Before Test ❌
**Should BLOCK**: Creating implementation files without failing tests
```python
# Creating app/models/new_feature.py without test
def new_feature():
    return "implemented"
```
**Expected**: Block with "Premature implementation violation"

### Test 1.4: Tests That Pass Immediately ❌
**Should BLOCK**: Tests that don't follow RED phase
```python
def test_always_passes():
    """This test passes without any implementation."""
    assert 2 + 2 == 4  # Always true, not driven by implementation
```
**Expected**: Should require failing test first

---

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

### Test 2.13: Indirection Patterns ❌
```python
def authenticate_user(username, password):
    result = get_auth_result()
    return result

def get_auth_result():
    return "authentication_successful"  # Hidden hardcoding through indirection
```
**Expected**: Block with sophisticated fake detection

### Test 2.14: Database-Like Fake Returns ❌
```python
def find_user_by_email(email):
    return {"id": "usr_12345", "email": email, "status": "active"}  # Fake DB response
```
**Expected**: Block with fake database implementation

### Test 2.15: Configuration-Disguised Fakes ❌
```python
class Config:
    SUCCESS_MESSAGE = "operation_completed"

def process_request(data):
    return Config.SUCCESS_MESSAGE  # Hardcoding disguised as configuration
```
**Expected**: Block with configuration-disguised fake implementation

---

## Phase 3: Test Duplication Prevention

### Test 3.1: Versioned Test Files ❌
```
test_task_model_updated.py  # When test_task_model.py exists
```
**Expected**: Block with "versioning concept" detection

### Test 3.2: "New" Suffixed Files ❌
```
test_task_model_revised.py  # When test_task_model.py exists
```
**Expected**: Block with duplicate test file detection

### Test 3.3: "Refactored" Suffixed Files ❌
```
test_task_model_refactored.py  # When test_task_model.py exists
```
**Expected**: Block with refactor test duplication

### Test 3.4: Similar Test Names ❌
```python
def test_calculate_discount():
    pass

def test_discount_calculation():  # Similar to above
    pass
```
**Expected**: Block with "similar test names"

### Test 3.5: Import-Based Duplicates ❌
```python
# In test_pricing.py
from app.models.task import Task  # Same module as test_task_model.py

def test_pricing_logic():
    task = Task.create("test")
```
**Expected**: Block with "testing same module from different files"

### Test 3.6: Legitimate New Module Test ✅
```python
# test_payment_processor.py - completely new module
from app.models.payment import PaymentProcessor

def test_payment_processing():
    processor = PaymentProcessor()
    assert processor is not None
```
**Expected**: Should ALLOW - genuinely new module

### Test 3.7: Backup File Pattern ❌
```
test_task_model_backup.py  # When test_task_model.py exists
```
**Expected**: Block with "backup implies duplication" detection

### Test 3.8: Alternative File Pattern ❌
```
test_task_model_alternative.py  # When test_task_model.py exists
```
**Expected**: Block with "alternative implies duplicate functionality" detection

---

## Phase 4: Comment Pattern Detection

### Test 4.1: Implementation State Comments ❌
```python
def test_user_authentication():
    # Function is not ready
    result = authenticate_user("user", "pass")
    assert result is True
```
**Expected**: Block with implementation state comment violation

### Test 4.2: Failure Expectation Comments ❌
```python
def test_feature():
    # This will break until we code it
    # Expected to fail
    assert feature_function() == "success"
```
**Expected**: Block with failure expectation comment violation

### Test 4.3: Phase Marking Comments ❌
```python
def test_implementation():
    # Step 1 of TDD cycle
    # GREEN PHASE implementation
    result = some_function()
    assert result == "expected"
```
**Expected**: Block with phase-marking comment violation

### Test 4.4: TODO Implementation Comments ❌
```python
def test_functionality():
    # TODO: Update when implementation is done
    # FIXME: Update after implementation
    result = process_data("input")
    assert result == "output"
```
**Expected**: Block with TODO comment violation

### Test 4.5: Docstring Evasion Attempt ❌
```python
def test_authentication():
    """
    Test user authentication functionality.

    Note: Expected to fail until implementation is complete.
    Phase: RED - waiting for implementation.
    """
    result = authenticate("user", "pass")
    assert result is True
```
**Expected**: Block with docstring comment violation

### Test 4.6: Legitimate Descriptive Comments ✅
```python
def test_calculate_discount_for_gold_customers():
    """Test that gold customers receive 20% discount."""
    # Test expects this behavior to work correctly
    result = calculate_discount(100, "GOLD")
    assert result == 80
```
**Expected**: Should ALLOW - proper test description

### Test 4.7: Implementation Status Synonyms ❌
```python
def test_data_processing():
    # Currently unimplemented
    result = process_data("input")
    assert result == "processed"
```
**Expected**: Block with implementation awareness detection

### Test 4.8: Dependency Awareness Comments ❌
```python
def test_api_integration():
    # Waiting for backend completion
    result = call_api("/users")
    assert result["status"] == "success"
```
**Expected**: Block with dependency awareness comment violation

---

## Phase 5: Documentation Control

### Test 5.1: README Creation ❌
```markdown
# Project Documentation
This is a comprehensive README for the project...
```
**Expected**: Block with documentation creation violation

### Test 5.2: Features Documentation ❌
```markdown
# Features List
## Authentication System
Our authentication provides...
```
**Expected**: Block with premature documentation

### Test 5.3: API Documentation ❌
```markdown
# API Documentation
## Endpoints
- GET /api/tasks
- POST /api/tasks
```
**Expected**: Block with documentation spam

### Test 5.4: Debug Script Spam ❌
```python
print("🚀 STARTING COMPREHENSIVE DEBUG ANALYSIS")
print("✅ Testing user authentication...")
print("🎉 AUTHENTICATION WORKING PERFECTLY!")
print("💯 PRODUCTION READY!")
```
**Expected**: Block with verbose debug script violation

### Test 5.5: Non-Markdown Documentation ❌
```text
# user_guide.txt
User Guide

Installation:
1. Clone repository
2. Install dependencies
3. Run application
```
**Expected**: Block with "Documentation file creation without user request"

### Test 5.6: Alternative Documentation Formats ❌
```rst
API_REFERENCE.rst
================

Authentication
--------------
All API endpoints require authentication headers.
```
**Expected**: Block with documentation in different format

### Test 5.7: Guide Documentation ❌
```markdown
# INSTALLATION_GUIDE.md

## Setup Instructions
Follow these steps to set up the development environment...
```
**Expected**: Block with "guide" content as documentation

---

## Phase 6: Backend Framework Intelligence

### Test 6.1: Flask Route Definitions ✅
```python
@app.route('/api/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'POST':
        return create_user(request.json)
    return get_users()
```
**Expected**: Should ALLOW - legitimate Flask pattern

### Test 6.2: FastAPI Patterns ✅
```python
@router.get("/items/{item_id}")
async def read_item(item_id: int):
    return await get_item_from_database(item_id)
```
**Expected**: Should ALLOW - legitimate FastAPI pattern

### Test 6.3: Database Operations ✅
```python
def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()
```
**Expected**: Should ALLOW - real database query

### Test 6.4: Fake Backend Response ❌
```python
@app.route('/api/users')
def get_users():
    return {"users": [{"id": 1, "name": "Test User"}]}  # Hardcoded response
```
**Expected**: Block with fake implementation in backend context

---

## Phase 7: Edge Cases & Evasion

### Test 7.1: Mixed Violations ❌
```python
def test_complex_scenario():
    # RED PHASE - should fail initially  <- Comment violation
    def fake_implementation():
        return "hardcoded_result"  # <- Fake implementation

    result = fake_implementation()
    assert result == "hardcoded_result"
```
**Expected**: Block with multiple violation detection

### Test 7.2: Subtle Evasion ❌
```python
def test_authentication():
    # This function will not work initially  <- Subtle phase marking
    # Implementation status: pending        <- Evasion attempt
    result = auth_function("test", "pass")
    assert result == True
```
**Expected**: Block with evasion detection

### Test 7.3: Legitimate Complex Code ✅
```python
def complex_business_logic(data, config):
    """Complex but legitimate business logic."""
    processed = []
    for item in data:
        if config.get('validate', True):
            validation_result = validate_item(item, config['rules'])
            if validation_result.is_valid:
                processed.append(transform_item(item, config['transform']))
    return aggregate_results(processed, config['aggregation'])
```
**Expected**: Should ALLOW - complex but real logic

---

## Phase 8: Error Quality Validation

### Test 8.1: Clear Error Messages
When violations occur, verify error messages include:
- **Issue**: What was problematic about the code
- **Why blocked**: Explanation of why this violates TDD principles
- **Suggestion**: Concrete alternative approach
- **Example**: Show better implementation if applicable

### Test 8.2: False Positive Prevention
Ensure legitimate patterns are not incorrectly blocked:
- Complex business logic with valid conditionals
- Framework-specific patterns (Flask, FastAPI, Django)
- Legitimate error handling and validation
- Real algorithm implementations

---

## Phase 9: Stress Testing

### Test 9.1: Large File Handling
Test files with:
- 20+ test functions
- Complex nested class structures
- Large comment blocks and docstrings
- Mixed legitimate and violation patterns

### Test 9.2: Rapid Development Simulation
- Quick successive test creation attempts
- Rapid TDD cycle: test → implementation → test
- Multiple agent coordination scenarios

---

## Success Criteria Summary

### ✅ Must Allow (17+ scenarios)
1. Single test creation following TDD
2. Real business logic implementations
3. Complex but legitimate algorithms
4. Framework-specific patterns (Flask/FastAPI/Django)
5. Proper database operations
6. Legitimate error handling
7. Real API implementations
8. Complex integration scenarios
9. Valid refactoring activities
10. Proper test descriptions and documentation
11. Inline code comments explaining logic
12. Type hints and validation code
13. Helper functions and utilities
14. Configuration and environment handling
15. Proper exception handling
16. **Pytest decorator mocking (@patch patterns)**
17. **Pytest parameterized tests (@pytest.mark.parametrize)**

### ❌ Must Block (54+ scenarios)
**Fake Implementations (19)**:
- Hardcoded returns, magic numbers, test-specific conditionals
- Mock objects in production, NotImplementedError patterns
- Variable-disguised hardcoding, copy-paste from assertions
- Indirection patterns, configuration-disguised fakes

**Test Duplication (10)**:
- Versioned files, "new"/"refactored" suffixes
- Similar test names, import-based duplicates
- Backup/alternative file patterns

**Comment Violations (14)**:
- Implementation state, phase-marking, failure expectations
- TODO patterns, docstring evasion attempts
- Implementation status synonyms, dependency awareness

**Documentation Control (7)**:
- README/CHANGELOG/FEATURES creation
- Debug script spam prevention
- Non-markdown documentation formats

**Sophisticated Evasion (4)**:
- Multi-level indirection, configuration file abuse
- Method chaining evasion, import alias duplication

**Edge Cases (8)**:
- Mixed violations, evasion attempts
- Subtle synonym usage, complex violation patterns

**Pytest Framework Violations (4)**:
- unittest.TestCase class usage instead of flat functions
- Context manager mocking (with patch()) instead of @patch decorators
- Shared mocks in test files instead of conftest.py
- Multiple similar tests without @pytest.mark.parametrize

### Error Quality Requirements
- All blocked actions must include clear explanations
- Constructive suggestions for alternatives
- Specific examples where applicable
- Proper violation categorization
- No false positives on legitimate code

---

## Phase 11: Borderline Cases (New)

### Test 11.1: Legitimate Constants vs Hardcoding ❌/✅
```python
def calculate_tax(income):
    TAX_RATE = 0.20  # Is this legitimate constant or hardcoded test value?
    return income * TAX_RATE
```
**Expected**: Borderline case - depends on context and usage patterns

### Test 11.2: Business Logic vs Test-Specific Conditionals ❌/✅
```python
def categorize_user(user):
    if user.age >= 18:  # Legitimate business rule or test-specific?
        return "adult"
    return "minor"
```
**Expected**: Should ALLOW if genuinely universal business logic

### Test 11.3: Context-Sensitive Mock Usage ❌/✅
```python
# In test file - should be allowed
def test_database_connection():
    mock_db = Mock()
    result = process_with_db(mock_db)

# In implementation file - should be blocked
def get_database():
    return Mock()  # This should be blocked
```
**Expected**: Context determines validity

### Test 11.4: Complex Realistic Business Logic ✅
```python
def calculate_shipping_cost(weight, distance, priority):
    base_rate = 5.00
    weight_multiplier = weight * 0.50
    distance_multiplier = distance * 0.02
    priority_multiplier = 1.5 if priority == "express" else 1.0
    return (base_rate + weight_multiplier + distance_multiplier) * priority_multiplier
```
**Expected**: Should ALLOW - legitimate complex business logic

### Test 11.5: Realistic Database Queries ✅
```python
def find_active_users_by_role(role, limit=50):
    return User.objects.filter(
        role=role,
        is_active=True,
        last_login__gte=timezone.now() - timedelta(days=30)
    ).order_by('-last_login')[:limit]
```
**Expected**: Should ALLOW - realistic database operation

---

## Phase 12: Sophisticated Evasion (New)

### Test 12.1: Multi-Level Indirection ❌
```python
def authenticate_user(username, password):
    return get_auth_result()

def get_auth_result():
    return fetch_auth_status()

def fetch_auth_status():
    return "authenticated"  # Hidden 3 levels deep
```
**Expected**: Block with sophisticated indirection detection

### Test 12.2: Configuration File Abuse ❌
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

### Test 12.3: Class Method Chaining Evasion ❌
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

### Test 12.4: Import Alias Module Duplication ❌
```python
# test_user_management.py
from app.models.user import User as UserModel

# test_account_system.py
from app.models.user import User as AccountUser

# Both testing same User model through aliases
```
**Expected**: Block with aliased import duplication detection

---

## Phase 13: Pytest Standards Enforcement (New)

**Purpose**: Validate that TDD Guard correctly blocks unittest patterns and enforces pytest best practices as defined in INSTRUCTIONS_V1.md Section 5.

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

---

## Phase 10: Advanced Edge Cases (Global Deployment)

Based on sophisticated agent evasion testing, these patterns were identified as critical gaps:

### Test 10.1: Word-Form Test Name Variations ❌ (Should BLOCK)

**Issue Found**: Agents can evade similar name detection by using different word forms
```python
def test_process_payment():
    """Test payment processing."""
    assert process_payment(100, "credit") == "success"

def test_payment_processing():
    """Test the payment processing functionality."""
    assert process_payment(200, "debit") == "success"
```
**Expected**: Block with "Word-form variation: test_process_payment + test_payment_processing test same functionality"

### Test 10.2: Singular/Plural Variations ❌ (Should BLOCK)

**Issue Found**: Simple plural variations bypass detection
```python
def test_process_payment():
    """Test single payment processing."""
    assert process_payment(100) == "success"

def test_process_payments():
    """Test multiple payment processing."""
    assert process_payment(200) == "success"
```
**Expected**: Block with "Singular/plural variation detected"

### Test 10.3: Non-Markdown Documentation ❌ (Should BLOCK)

**Issue Found**: .txt, .rst, and other documentation formats were allowed
```text
# documentation.txt
Project Documentation
Setup instructions and API details...
```
**Expected**: Block with "Documentation file creation without user request"

**Fix Applied**: Removed `*.txt` from config.json ignore patterns

### Test 10.4: Cross-Directory Test Duplication ❌ (Should BLOCK)

**Issue Found**: Same module tested from different directories
```
tests/unit/test_task_model.py      # Testing Task model
tests/integration/test_task_model.py  # Same Task model tests
```
**Expected**: Block with "Cross-directory duplicate: same module tested from multiple directories"

### Test 10.5: Sophisticated Variable-Disguised Fakes ❌ (Should BLOCK)

**Confirmed Working**: Advanced fake implementations correctly blocked
```python
def authenticate_user_advanced(username, password):
    # Variables to disguise hardcoding - CORRECTLY BLOCKED
    expected_result = "success"
    processed_value = "authenticated"
    status_code = expected_result
    return status_code
```
**Expected**: Block with "Variable-disguised fake implementation"

### Test 10.6: Ternary Operator Evasion ❌ (Should BLOCK)

**Confirmed Working**: Ternary operator fakes correctly blocked
```python
def authenticate_user(username, password):
    return "success" if True else "failed"  # CORRECTLY BLOCKED
```
**Expected**: Block with "Hardcoded ternary operator fake"

### Test 10.7: Comment Synonym Evasion ❌ (Should BLOCK)

**Confirmed Working**: Synonym comment patterns correctly blocked
```python
def test_user_registration():
    # Not implemented yet        # CORRECTLY BLOCKED
    # Pending implementation     # CORRECTLY BLOCKED
    # To be implemented         # CORRECTLY BLOCKED
    assert register_user() == "success"
```
**Expected**: Block with "Comment indicating implementation awareness"

### Test 10.8: Legitimate Backend Framework Patterns ✅ (Should ALLOW)

**Confirmed Working**: Real Flask/Django patterns correctly allowed after TDD steps
```python
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200  # CORRECTLY ALLOWED
```
**Expected**: Allow after proper failing test → minimal stub → real implementation cycle

---

## Updated Test Execution Checklist

- [ ] Phase 1: Core TDD Workflow (4 tests)
- [ ] Phase 2: Fake Implementation Detection (19 tests) - **Enhanced**
- [ ] Phase 3: Test Duplication Prevention (10 tests) - **Enhanced**
- [ ] Phase 4: Comment Pattern Detection (14 tests) - **Enhanced**
- [ ] Phase 5: Documentation Control (7 tests) - **Enhanced**
- [ ] Phase 6: Backend Framework Intelligence (6 tests)
- [ ] Phase 7: Edge Cases & Evasion (8 tests)
- [ ] Phase 8: Error Quality Validation (4 tests)
- [ ] Phase 9: Stress Testing (4 tests)
- [ ] Phase 10: Advanced Edge Cases (8 tests)
- [ ] **Phase 11: Borderline Cases (5 tests)** - **New**
- [ ] **Phase 12: Sophisticated Evasion (4 tests)** - **New**
- [ ] **Phase 13: Pytest Standards Enforcement (6 tests)** - **New**

**Total: 99 comprehensive test scenarios** (increased from 93)

---

## Configuration Updates Applied

### config.json Changes:
```json
// BEFORE (*.txt was ignored):
"ignorePatterns": ["*.log", "*.txt", "**/*.json", ...]

// AFTER (*.txt now validated):
"ignorePatterns": ["*.log", "**/*.json", ...]
```

### instructions.md Enhancements:
Added sophisticated test name detection patterns:
- Word-form variations (verb/noun forms)
- Singular/plural variations
- Cross-directory duplicate detection
- Explicit examples for each pattern type

---

*This document serves as the definitive reference for TDD Guard validation testing and should be updated as new edge cases or violations are discovered.*