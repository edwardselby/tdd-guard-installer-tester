# Comment Violations Test Scenarios

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

### Test 4.9: Comment Synonym Evasion ❌
```python
def test_user_registration():
    # Not implemented yet        # Should be blocked
    # Pending implementation     # Should be blocked
    # To be implemented         # Should be blocked
    assert register_user() == "success"
```
**Expected**: Block with "Comment indicating implementation awareness"

## Success Criteria
- ❌ Block implementation state, phase-marking, failure expectations (14 scenarios)
- ❌ Block TODO patterns, docstring evasion attempts
- ❌ Block implementation status synonyms, dependency awareness
- ✅ Allow proper test descriptions and legitimate comments (1 scenario)