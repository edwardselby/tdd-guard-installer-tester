# Test Duplication Prevention Scenarios

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

### Test 3.9: Word-Form Test Name Variations ❌
```python
def test_process_payment():
    """Test payment processing."""
    assert process_payment(100, "credit") == "success"

def test_payment_processing():
    """Test the payment processing functionality."""
    assert process_payment(200, "debit") == "success"
```
**Expected**: Block with "Word-form variation: test_process_payment + test_payment_processing test same functionality"

### Test 3.10: Singular/Plural Variations ❌
```python
def test_process_payment():
    """Test single payment processing."""
    assert process_payment(100) == "success"

def test_process_payments():
    """Test multiple payment processing."""
    assert process_payment(200) == "success"
```
**Expected**: Block with "Singular/plural variation detected"

## Success Criteria
- ❌ Block versioned files, "new"/"refactored" suffixes (8 scenarios)
- ❌ Block similar test names, import-based duplicates (2 scenarios)
- ✅ Allow legitimate new module tests (1 scenario)
- ❌ Block word-form and singular/plural variations (2 scenarios)