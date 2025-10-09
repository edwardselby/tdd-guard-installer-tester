# Core TDD Workflow Test Scenarios (Flexible Mode)

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

### Test 1.2: Multiple Related Tests (2-3) ✅
**Should ALLOW**: Adding 2-3 tests for the SAME function testing related scenarios
```python
def test_calculate_discount_min_boundary():
    assert calculate_discount(0) == 0

def test_calculate_discount_max_boundary():
    assert calculate_discount(100) == 100

def test_calculate_discount_midpoint():
    assert calculate_discount(50) == 50
```
**Expected**: Should ALLOW (same function, boundary values)

### Test 1.3: Multiple Error Conditions ✅
**Should ALLOW**: Testing related error conditions for same function
```python
def test_validate_email_null():
    with pytest.raises(ValueError):
        validate_email(None)

def test_validate_email_empty():
    with pytest.raises(ValueError):
        validate_email("")

def test_validate_email_invalid():
    with pytest.raises(ValueError):
        validate_email("not-valid")
```
**Expected**: Should ALLOW (same function, error conditions)

### Test 1.4: More Than 3 Tests ❌
**Should BLOCK**: Exceeding the 3-test limit
```python
def test_func_one():
    assert True

def test_func_two():
    assert True

def test_func_three():
    assert True

def test_func_four():
    assert True
```
**Expected**: Block with "Exceeds maximum 3 tests per operation"

### Test 1.5: Tests for Different Functions ❌
**Should BLOCK**: Tests targeting different functions/methods
```python
def test_create_user():
    user = create_user("John")
    assert user.name == "John"

def test_delete_task():
    task = delete_task(1)
    assert task.deleted == True
```
**Expected**: Block with "Tests for different functions not allowed"

### Test 1.6: Implementation Before Test ❌
**Should BLOCK**: Creating implementation files without failing tests
```python
# Creating app/models/new_feature.py without test
def new_feature():
    return "implemented"
```
**Expected**: Block with "Premature implementation violation"

### Test 1.7: Tests That Pass Immediately ❌
**Should BLOCK**: Tests that don't follow RED phase
```python
def test_always_passes():
    """This test passes without any implementation."""
    assert 2 + 2 == 4  # Always true, not driven by implementation
```
**Expected**: Should require failing test first

## Success Criteria
- ✅ Allow single test creation following TDD
- ✅ Allow 2-3 tests for SAME function (boundaries/errors/types)
- ❌ Block more than 3 test functions in single operation
- ❌ Block tests for different functions/methods
- ❌ Block tests mixing different concerns
- ❌ Block implementation before failing test exists
- ❌ Block tests that pass immediately (trivial assertions)
