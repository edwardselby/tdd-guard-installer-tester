# Core TDD Workflow Test Scenarios

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

## Success Criteria
- ✅ Allow single test creation following TDD
- ❌ Block multiple test functions in single operation
- ❌ Block implementation before failing test exists
- ❌ Block tests that pass immediately (trivial assertions)