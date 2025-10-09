# Refactoring Guidance - Test Scenarios

## Scenario 1: Valid DRY Consolidation (SHOULD PASS)

### Context
Developer consolidates three duplicate database query functions into one.

### Code Changes

**Step 1: Create consolidated function**
```python
# New consolidated function
def get_entity(entity_type, entity_id):
    models = {'user': User, 'product': Product, 'order': Order}
    return db.query(models[entity_type]).filter_by(id=entity_id).first()
```

**Step 2: Phase 1 - Deprecation stubs**
```python
def get_user_data(user_id):
    raise DeprecationWarning("Use get_entity('user', user_id)")

def fetch_product(product_id):
    raise DeprecationWarning("Use get_entity('product', product_id)")

def load_order(order_id):
    raise DeprecationWarning("Use get_entity('order', order_id)")

# Run pytest → All tests pass ✅
```

**Step 3: Phase 2 - Delete stubs**
```python
# All three functions deleted
# (Safe because Phase 1 tests proved they're unused)
```

### Expected Result: ✅ ALLOWED
TDD Guard allows this because:
- Phase 1 created deprecation stubs first
- Tests passed with deprecation stubs (proof of safety)
- Phase 2 deletion only after test validation

---

## Scenario 2: Direct Deletion Without Deprecation (SHOULD BLOCK)

### Context
Developer tries to delete duplicate functions directly.

### Code Changes

```python
# BEFORE: Three duplicate functions exist
def get_user_data(user_id): ...
def fetch_product(product_id): ...
def load_order(order_id): ...

# AFTER: Functions directly deleted
# (All three removed in one step)

# New consolidated function added
def get_entity(entity_type, entity_id): ...
```

### Expected Result: ❌ BLOCKED

**TDD Guard Response:**
```
❌ VIOLATION: Direct code deletion without deprecation phase

You attempted to delete these functions directly:
- get_user_data()
- fetch_product()
- load_order()

REQUIRED PROTOCOL:
Phase 1: Replace each function with DeprecationWarning stub
         Run tests to prove they're unused
Phase 2: Delete stubs only after tests pass

WHY: Tests must prove deletion is safe before it's allowed.
```

---

## Scenario 3: Deleting Deprecation Stub While Tests Fail (SHOULD BLOCK)

### Context
Developer created deprecation stubs, but tests are failing with them.

### Code Changes

**Step 1: Deprecation stubs created**
```python
def calculate_discount(price):
    raise DeprecationWarning("Use PricingService.calculate_discount()")

# Run pytest → 3 tests FAIL
# ERROR: calculate_discount() is deprecated
```

**Step 2: Developer tries to delete function anyway**
```python
# Function deleted despite failing tests
```

### Expected Result: ❌ BLOCKED

**TDD Guard Response:**
```
❌ VIOLATION: Deletion attempted with failing tests

Tests are currently failing. You cannot proceed to Phase 2 (deletion).

CURRENT STATUS:
- Phase 1: ✓ Deprecation stub created
- Tests: ❌ 3 tests failing
- Phase 2: ❌ BLOCKED until tests pass

REQUIRED ACTIONS:
1. Fix the 3 failing tests by updating callers
2. Ensure all tests pass with deprecation stub
3. THEN deletion is allowed (Phase 2)

WHY: Failing tests mean code is still in use.
```

---

## Scenario 4: Refactoring Method to Utility (SHOULD PASS)

### Context
Moving validation logic from class method to shared utility.

### Code Changes

**Step 1: Create utility function**
```python
# utils/validators.py
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

**Step 2: Phase 1 - Deprecate original method**
```python
class UserService:
    def validate_email(self, email):
        raise DeprecationWarning(
            "UserService.validate_email() deprecated. "
            "Use utils.validators.validate_email()"
        )

# Run pytest → Tests pass ✅
```

**Step 3: Phase 2 - Remove method**
```python
class UserService:
    # validate_email() deleted
    # (Tests proved it's unused)
    pass
```

### Expected Result: ✅ ALLOWED
Proper deprecation-first protocol followed.

---

## Scenario 5: Replacing Deprecated Stub with New Implementation (SHOULD BLOCK)

### Context
Developer tries to replace deprecation stub with new implementation instead of deleting it.

### Code Changes

**Current State:**
```python
def legacy_function(data):
    raise DeprecationWarning("Use new_function()")
```

**Attempted Change:**
```python
def legacy_function(data):
    """Let me just update this instead of deleting"""
    return new_function(data)  # Redirecting instead of removing
```

### Expected Result: ❌ BLOCKED

**TDD Guard Response:**
```
❌ VIOLATION: Deprecation stub replaced with implementation

You're trying to restore implementation to a deprecated function.

DEPRECATION IS ONE-WAY:
Implementation → DeprecationWarning → Deletion

You cannot go backwards:
DeprecationWarning → Implementation ❌ BLOCKED

CORRECT APPROACH:
If this function is still needed:
1. Revert the deprecation
2. Keep the function active
3. Reconsider your refactoring strategy

WHY: Deprecation signals intent to delete, not to modify.
```

---

## Scenario 6: Batch Refactoring Multiple Modules (SHOULD PASS)

### Context
Large refactoring consolidating utility functions across multiple files.

### Code Changes

**Step 1: Create new consolidated utilities**
```python
# utils/string_helpers.py
def normalize_text(text): ...
def sanitize_input(text): ...
def format_display(text): ...
```

**Step 2: Phase 1 - Deprecate all old implementations**
```python
# services/user_service.py
def normalize_username(username):
    raise DeprecationWarning("Use utils.string_helpers.normalize_text()")

# services/product_service.py
def sanitize_product_name(name):
    raise DeprecationWarning("Use utils.string_helpers.sanitize_input()")

# services/display_service.py
def format_product_display(text):
    raise DeprecationWarning("Use utils.string_helpers.format_display()")

# Run pytest → All 47 tests pass ✅
```

**Step 3: Phase 2 - Delete all deprecated functions**
```python
# All deprecated functions removed across 3 files
# (Safe because comprehensive test suite validated Phase 1)
```

### Expected Result: ✅ ALLOWED
Demonstrates deprecation-first protocol works at scale.

---

## Scenario 7: Premature Deletion (Catching Incomplete Migration)

### Context
Developer thinks migration is complete but tests reveal hidden dependencies.

### Code Changes

**Step 1: Phase 1 deprecation**
```python
def get_config_value(key):
    raise DeprecationWarning("Use ConfigService.get()")

# Run pytest
# ✅ 45 tests pass
# ❌ 2 integration tests fail (ran in different test suite)
```

**Step 2: Developer tries Phase 2 deletion**
```python
# Attempts to delete function
```

### Expected Result: ❌ BLOCKED

**TDD Guard Response:**
```
❌ VIOLATION: Deletion attempted with test failures

You cannot delete while tests are failing.

FAILING TESTS:
- test_integration.py::test_legacy_config_import
- test_integration.py::test_backwards_compatibility

RESOLUTION:
1. Fix the 2 failing integration tests
2. Update code to use ConfigService.get()
3. Ensure ALL tests pass
4. THEN proceed with deletion

WHY: These failures reveal hidden dependencies.
Deletion would break production code.
```

---

## Key Testing Insights

### What Makes Tests Pass in Phase 1?

✅ **Function truly unused** → Tests pass, deletion is safe
❌ **Function still called** → Tests fail, must update callers first

### The Two-Phase Safety Net

**Phase 1 (Deprecation):** Reveals what still depends on old code
**Phase 2 (Deletion):** Only allowed after Phase 1 proves safety

### Why This Protocol Works

1. **No silent failures:** Deprecation warnings make dependencies explicit
2. **Test-driven proof:** Can't delete until tests prove it's safe
3. **Gradual migration:** Update callers at your own pace
4. **Rollback safety:** Easy to revert Phase 1 if needed
5. **Documentation:** Deprecation messages guide migration

---

## Summary: The Refactoring Rule

```
Code Lifecycle During Refactoring:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Active Implementation
        ↓
Phase 1: DeprecationWarning stub
        ↓
Run Tests
        ↓
    ┌───────────┐
    │ Tests     │
    │ Status?   │
    └─────┬─────┘
          │
    ┌─────┴──────┐
    │            │
 PASS ✅      FAIL ❌
    │            │
    │        Update callers
    │        Re-run tests
    │            │
    └────┬───────┘
         │
    All tests pass
         ↓
Phase 2: Deletion allowed
         ↓
Code completely removed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Remember:** Deprecation is not a suggestion—it's a mandatory checkpoint that tests must validate before deletion is permitted.
