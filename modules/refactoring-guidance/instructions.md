# Refactoring Guidance - Deprecation-First Protocol

## Priority Level: 3 (Refactoring Safety)

## 🔄 DEPRECATION-FIRST REFACTORING ENFORCEMENT

### The Two-Phase Deletion Rule

**CRITICAL PRINCIPLE:** Code cannot be deleted directly. It MUST pass through a deprecation phase first.

---

## Phase 1: Replace Logic with DeprecationWarning

**MANDATORY FIRST STEP** before any code deletion:

❌ **BLOCK:** Direct deletion of functions, methods, or classes
❌ **BLOCK:** Removing logic without deprecation stub
✅ **ALLOW:** Replacing implementation with `DeprecationWarning` stub

### Pattern: From Implementation to Deprecation Stub

```python
# ❌ BLOCKED: Direct deletion
# def calculate_user_score(user):
#     """Calculate score for user"""
#     return user.points * user.multiplier
# ↑ DELETED - VIOLATION!

# ✅ REQUIRED: Phase 1 - Deprecation stub FIRST
def calculate_user_score(user):
    """DEPRECATED: Use calculate_score(user, 'user') instead

    This function has been consolidated into calculate_score().
    It will be removed in the next refactor phase.
    """
    raise DeprecationWarning(
        "calculate_user_score() is deprecated. "
        "Use calculate_score(user, entity_type='user') instead."
    )
```

### Why This Works

1. **Tests prove it's unused:** If tests pass with `DeprecationWarning`, function isn't called
2. **Tests reveal callers:** If tests fail, you discover what still needs updating
3. **Clear migration path:** Error message tells developers what to use instead
4. **TDD Guard validation:** Passing tests = proof that deletion is safe

---

## Phase 2: Delete Deprecation Stub (Only After Tests Pass)

**PREREQUISITE:** All tests MUST pass with deprecation stub in place.

❌ **BLOCK:** Deleting code while tests are failing
❌ **BLOCK:** Skipping Phase 1 deprecation
✅ **ALLOW:** Deleting deprecation stub after tests pass

### Pattern: Safe Deletion After Deprecation

```python
# Phase 1 code (from above):
def calculate_user_score(user):
    raise DeprecationWarning("Use calculate_score() instead")

# Run pytest → Tests PASS
# ✓ This proves the function is never called
# ✓ Safe to proceed to Phase 2

# Phase 2: Now deletion is ALLOWED
# (Function completely removed - tests already proved it's safe)
```

---

## Common Refactoring Scenarios

### Scenario 1: Consolidating Duplicate Functions (DRY)

```python
# BEFORE: Duplicate logic
def get_user_data(user_id):
    return db.query(User).filter_by(id=user_id).first()

def fetch_user_info(user_id):
    return db.query(User).filter_by(id=user_id).first()

def load_user(user_id):
    return db.query(User).filter_by(id=user_id).first()

# STEP 1: Create consolidated function
def get_entity(entity_type, entity_id):
    """Consolidated database query function"""
    model = {'user': User, 'product': Product}[entity_type]
    return db.query(model).filter_by(id=entity_id).first()

# STEP 2: Phase 1 - Replace each duplicate with deprecation stub
def get_user_data(user_id):
    raise DeprecationWarning("Use get_entity('user', user_id)")

def fetch_user_info(user_id):
    raise DeprecationWarning("Use get_entity('user', user_id)")

def load_user(user_id):
    raise DeprecationWarning("Use get_entity('user', user_id)")

# STEP 3: Run tests
# - Tests PASS → Functions unused, safe to delete (Phase 2)
# - Tests FAIL → Update callers to use get_entity(), then retry

# STEP 4: Phase 2 - Delete all three functions
# (Safe because tests proved they're unused)
```

### Scenario 2: Moving Logic to Utility Module

```python
# BEFORE: Logic embedded in class
class UserService:
    def validate_email(self, email):
        """Email validation logic"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

# STEP 1: Move to shared utility
# utils/validators.py
def validate_email(email):
    """Shared email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# STEP 2: Phase 1 - Deprecation stub in original location
class UserService:
    def validate_email(self, email):
        raise DeprecationWarning(
            "UserService.validate_email() deprecated. "
            "Use utils.validators.validate_email() instead."
        )

# STEP 3: Run tests → Identify and update callers

# STEP 4: Phase 2 - Delete method from UserService
class UserService:
    # validate_email() removed - now using shared utility
    pass
```

### Scenario 3: Removing Obsolete Feature

```python
# BEFORE: Feature being removed
def legacy_report_generator(data):
    """Old reporting system being replaced"""
    # Complex legacy logic...
    return generate_pdf(data)

# STEP 1: Verify new replacement exists
def modern_report_service(data):
    """New reporting system"""
    return ReportBuilder(data).generate()

# STEP 2: Phase 1 - Deprecation stub for old feature
def legacy_report_generator(data):
    raise DeprecationWarning(
        "legacy_report_generator() removed. "
        "Use modern_report_service() instead."
    )

# STEP 3: Run tests
# - If tests pass: Feature truly obsolete (Phase 2)
# - If tests fail: Migration incomplete, update callers first

# STEP 4: Phase 2 - Delete legacy function
# (Only after Phase 1 tests prove it's unused)
```

---

## Enforcement Rules Summary

### What TDD Guard BLOCKS ❌

1. **Direct Deletion:** Removing functions/classes without deprecation phase
2. **Skipping Deprecation:** Going straight from implementation to deletion
3. **Deletion During Failing Tests:** Removing code while tests fail
4. **Silent Removal:** Deleting code without clear migration path

### What TDD Guard ALLOWS ✅

1. **Phase 1:** Replacing implementation with `DeprecationWarning` stub
2. **Phase 2:** Deleting deprecation stub ONLY after tests pass
3. **Clear Guidance:** Deprecation messages explaining what to use instead
4. **Test-Driven Proof:** Using test results to validate safe deletion

---

## Integration with Red-Green-Refactor

This protocol fits naturally into TDD's refactor phase:

```
RED → GREEN → REFACTOR (with deprecation-first protocol)
                ↓
                Phase 1: Add deprecation stubs
                Run tests (prove unused)
                ↓
                Phase 2: Delete stubs
                Run tests (confirm still passing)
```

---

## Benefits

✅ **Test-Driven Proof:** Every deletion proven safe by passing tests
✅ **No Guesswork:** Deprecation warnings reveal all remaining callers
✅ **Agent-Friendly:** Clear two-phase protocol, easy to follow
✅ **Safe Refactoring:** Impossible to accidentally delete needed code
✅ **Documentation:** Deprecation messages provide migration guidance
✅ **TDD Alignment:** Natural fit with Red-Green-Refactor workflow

---

## Quick Reference

**Remember:** Code cannot be deleted directly. It MUST become a `DeprecationWarning` stub first, and tests MUST pass with that stub before final deletion is allowed.

```python
# The Rule:
Implementation → DeprecationWarning (Phase 1) → Tests Pass → Deletion (Phase 2)

# Never:
Implementation → Deletion ❌ BLOCKED
```
