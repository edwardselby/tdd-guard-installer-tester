# TDD Guard Rules

## 🚫 Response Formatting Rules

### ❌ **BLOCK Response Patterns:**

- Including raw code snippets in validation reasoning
- Multi-line quoted code blocks in JSON values
- Unescaped newlines (`\n`) or special characters in reasoning text
- Embedding function/class definitions in responses
- Quoting user's file content verbatim
- Large reasoning text for files >150 lines

### ✅ **ALLOW Response Patterns:**

- Brief code references (e.g., "the test_user_workflow function")
- Summarized behavior descriptions without quotes
- Properly escaped JSON strings
- Compact reasoning (max 200 characters for files >150 lines)
- Line number references instead of code quotes (e.g., "lines 50-100")
- Single-line reasoning preferred

---

## 📋 JSON Response Format Requirements

### For Large Files (150+ lines):
- **Reasoning**: Maximum 200 characters
- **Format**: `{"reasoning": "Brief summary", "allowed": true/false}`
- **NO** code snippets or multi-line content
- Reference by line numbers, not content quotes

### For All Files:
- Properly escape special characters: `\n`, `\r`, `\t`, `"`, `\`
- Use compact summaries, not verbatim quotes
- Single-line reasoning preferred
- Keep JSON structure minimal and clean

---

## ✅ GOOD Response Examples

### Large file validation:
```json
{"reasoning": "Test covers complete workflow (lines 1-307). Violates TDD single-focus principle.", "allowed": false}
```

### Alternative for same scenario:
```json
{"reasoning": "Integration test detected. Recommend splitting into unit tests per step.", "allowed": false}
```

### Allowing a valid test:
```json
{"reasoning": "Single-focus unit test following TDD principles.", "allowed": true}
```

---

## ❌ BAD Response Examples (Causes JSON Parsing Errors)

### Including code snippets (CAUSES ERROR):
```json
{"reasoning": "Function:\ndef test_workflow():\n    \"\"\"Long docstring...\"\"\"\n    query = \"SELECT...\"", "allowed": false}
```
**Error**: Unescaped newlines break JSON parsing at validator.js:25

### Verbatim code quoting (CAUSES ERROR):
```json
{"reasoning": "Test contains:\n    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'\n    This violates...", "allowed": false}
```
**Error**: "Bad control character in string literal in JSON"

### Large unescaped content (CAUSES ERROR):
```json
{"reasoning": "The test function has a 50-line docstring that explains: \"Test Flow:\n1. User Registration...\n2. Email Verification...\"", "allowed": false}
```
**Error**: "Unterminated string in JSON"

---

## 🔧 Module Behavior

**Scope**: Claude CLI validation response formatting only

**Does NOT affect**:
- Code validation logic
- TDD enforcement rules
- Other module behaviors

**Target Error**: "Bad control character in string literal in JSON" at validator.js:25

**Expected Impact**:
- JSON parsing error rate: 67% → <5%
- Overall success rate: 0% → ~60-65%
- TDD violations remain at ~33% (legitimate enforcement)

---

## 📊 Response Strategy by File Size

| File Size | Max Reasoning Length | Strategy |
|-----------|---------------------|----------|
| <50 lines | 500 characters | Normal detailed reasoning |
| 50-150 lines | 300 characters | Concise reasoning with key points |
| >150 lines | 200 characters | Minimal summary, line references only |

---

## 🎯 Key Principles

1. **Never quote code**: Summarize behavior instead
2. **Always escape**: Ensure all JSON strings are properly escaped
3. **Stay compact**: Large files need minimal reasoning
4. **Reference locations**: Use line numbers, not content
5. **Single-line preferred**: Avoid multi-line reasoning text


## 🚨 Test File Duplication Prevention

### Block Patterns
❌ **BLOCK PATTERNS:**
- `test_*_v[0-9]*.py` → Block versioned files (test_module_v2.py)
- `test_*_new.py` → Block "new" suffixed files
- `test_*_refactored.py` → Block "refactored" suffixed files
- `test_*_revised.py` → Block "revised" suffixed files
- `test_enhanced_*.py` → Block "enhanced" prefixed files
- `test_*_enhanced.py` → Block "enhanced" suffixed files

### Similar Test Names Detection
❌ **BLOCK SIMILAR NAMES:**
- **Similar test names** → Block when pattern: test_WORD1_WORD2 + test_WORD2_WORD1
  - Example: `test_calculate_discount` + `test_discount_calculation` = SAME FUNCTIONALITY
  - Example: `test_user_login` + `test_login_user` = DUPLICATE TEST
- **Word-form variations** → Block: test_VERB_NOUN + test_NOUN_VERBING
  - Example: `test_process_payment` + `test_payment_processing` = DUPLICATE
- **Singular/plural variations** → Block: test_WORD + test_WORDs
  - Example: `test_process_payment` + `test_process_payments` = DUPLICATE
  - Pattern: Base words identical, differs only by 's', 'es', 'ies' suffix → BLOCK

### Advanced Duplication Detection
❌ **BLOCK ADVANCED PATTERNS:**
- **Cross-directory duplicates** → Block: identical filenames across test directories
  - Pattern: `tests/*/test_FILENAME.py` = Check filename across ALL test subdirectories
  - Example: `tests/unit/test_task.py` + `tests/integration/test_task.py` = DUPLICATE
- Multiple test functions in single file creation
- **Import-based duplicates** → Block: Multiple test files importing same modules
  - Pattern: Check import statements across test files for identical module imports
  - Example: test_pricing.py imports Task, test_task_model.py imports Task = DUPLICATE
  - Action: "Multiple test files testing same module → Consolidate into single test file"
  - Exception: Different test types allowed: test_user.py (unit), test_user_integration.py (integration)

### Pattern Matching Algorithm
- **Pattern matching priority**: Check base words first, then suffixes, then directory paths
  - Algorithm: Remove `test_` prefix → Compare core words → Check suffix patterns → Check cross-directory

**Action:** Direct to update existing test file instead of creating new ones.

## 🚨 Test Comment Violations

### Implementation Awareness Comments
❌ **BLOCK COMMENTS INDICATING IMPLEMENTATION AWARENESS:**
Comments that reveal knowledge about implementation state violate TDD principles:
- Implementation status comments: "doesn't exist yet", "not implemented", "method doesn't exist", "not ready", "currently unimplemented"
- Phase awareness comments: "should FAIL", "RED PHASE", "GREEN PHASE", "Expected to fail"
- Future implementation comments: "TODO: Update when implementation", "Will fail until implemented"
- Dependency awareness comments: "waiting for backend", "waiting for completion", "pending other work"
- Pattern: Any comment suggesting the test knows about current implementation state

## 🚨 Documentation File Prevention

### Block Documentation Creation
❌ **BLOCK DOCUMENTATION FILE CREATION:**
- `.md`, `.txt` files: `README.md`, `CHANGELOG.md`, `API.md`, `user_guide.txt`, etc.
- ANY documentation file unless user explicitly requests documentation
- Exception: `.rst` files allowed per project requirements
- Assumption: User wants code, not documentation spam

## 🚨 Debug Script Quality Control

### Block Celebration Patterns
❌ **BLOCK CELEBRATION PATTERNS:**
- "🎉", "💯", "PRODUCTION READY", "WORKING PERFECTLY"
- "ALL SYSTEMS OPERATIONAL", "COMPREHENSIVE DEBUG ANALYSIS"
- Excessive formatting, multiple unrelated tests in one script
- Self-congratulatory messages about functionality working

**Requirement:** Debug scripts must test ONE specific thing with clean pass/fail output.

## ⚠️ FAKE IMPLEMENTATION DETECTION

### Hardcoded Return Values
❌ **BLOCK PATTERNS:**
- `return "hardcoded_string"` → Any string literal returns
- `return 42` → Magic numbers without business logic
- `return [exact, test, list]` → Hardcoded lists matching test expectations
- `return {"key": "value"}` → Hardcoded dictionaries from test data

### Test-Specific Logic Patterns
❌ **BLOCK CONDITIONAL PATTERNS:**
- `if input == "test_value": return result` → Test-specific value checks
- `if len(items) == 3: return "valid"` → Test-specific length checks
- `if price == 100.0: return 80.0` → Test-specific calculations
- `if user.name == "testuser": return True` → Test-specific object checks

### Mock/Placeholder Patterns
❌ **BLOCK PLACEHOLDER CODE:**
- `return Mock()`, `return MagicMock()` → Mock objects in production
- `raise NotImplementedError()` → For functionality being tested
- `pass` or `return None` → For complex operations that tests expect to work

## 📋 IMPLEMENTATION REQUIREMENTS

### Real Business Logic Standards
✅ **REQUIRED IMPLEMENTATION APPROACH:**
- Must work for ANY valid input, not just test cases
- Generic solutions using lookup tables, algorithms, validation logic
- Example: `discounts = {"GOLD": 0.20}; return price * (1 - discounts.get(type, 0))`
- Handle edge cases and error conditions appropriately
- Production-ready complexity matching the problem scope

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


## 📋 Backend Framework Patterns (Allowed)

### Legitimate Backend Implementations
✅ **LEGITIMATE BACKEND IMPLEMENTATIONS:**
- Flask routes: `@app.route('/api/users', methods=['GET', 'POST'])`
- Database queries: `User.query.filter_by(id=user_id).first()`
- Request handling: `request.json`, parameter validation
- Authentication: Token validation, session management
- API responses: JSON serialization, proper status codes

### Framework-Specific Patterns

#### Flask Patterns
✅ **ALLOW Flask patterns:**
```python
@app.route('/api/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'POST':
        return create_user(request.json)
    return get_users()
```

#### FastAPI Patterns
✅ **ALLOW FastAPI patterns:**
```python
@router.get("/items/{item_id}")
async def read_item(item_id: int):
    return await get_item_from_database(item_id)
```

#### Database Operations
✅ **ALLOW database operations:**
```python
def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()
```

### What This Module Prevents
❌ **STILL BLOCKS fake backend responses:**
```python
@app.route('/api/users')
def get_users():
    return {"users": [{"id": 1, "name": "Test User"}]}  # Hardcoded response
```

## 🔄 TDD WORKFLOW ENFORCEMENT

### Test Creation Rules
❌ **BLOCK:** More than 3 test functions in single operation
❌ **BLOCK:** Tests for different functions/methods in single operation
❌ **BLOCK:** Tests mixing different behavioral concerns
❌ **BLOCK:** Tests that pass immediately (trivial assertions like `2 + 2 == 4`)
✅ **ALLOW:** 2-3 tests for the SAME function when testing:
  - Boundary values (min, max, edge cases)
  - Error conditions (null, empty, invalid)
  - Type variations (int, string, list)
✅ **ALLOW:** One test at a time for exploratory/complex behaviors

### Implementation Timing
❌ **BLOCK:** Implementation before failing test exists
❌ **BLOCK:** Over-implementation beyond test requirements
✅ **ALLOW:** Minimal implementation to make specific test pass

### Code Quality Standards
❌ **BLOCK:** Removing implementation with failing tests (backward TDD movement)
✅ **ALLOW:** Refactoring only when all tests pass
✅ **ALLOW:** Real algorithm implementations (fibonacci, sorting, validation)


## 🧪 PYTEST STANDARDS ENFORCEMENT

### Test Framework Requirements
❌ **BLOCK:** unittest framework (`class TestSomething`, `self.assert*`)
✅ **REQUIRE:** pytest flat functions (`def test_function()`, `assert condition`)

### Mock Pattern Enforcement
❌ **BLOCK:** `with patch('module.func') as mock:` (context managers)
✅ **REQUIRE:** `@patch('module.func')` decorators above function

### Mock Organization Standards
❌ **BLOCK:** Shared mocks in individual test files
✅ **REQUIRE:** Cross-file mocks in `conftest.py`, file-specific mocks at top

### Test Structure Requirements
❌ **BLOCK:** Multiple similar tests (`test_discount_gold`, `test_discount_silver`)
✅ **REQUIRE:** `@pytest.mark.parametrize` for similar scenarios

### Exception Testing Standards
❌ **BLOCK:** `self.assertRaises(ValueError)`
✅ **REQUIRE:** `with pytest.raises(ValueError):`

## 🔍 Sophisticated Evasion Patterns

### Multi-Level Indirection
❌ **BLOCK:** Functions calling functions hiding hardcoded returns
- `def auth() → get_result() → fetch_status() → "authenticated"`

### Configuration File Abuse
❌ **BLOCK:** Config files hiding hardcoded values
- `config.py: RESPONSES = {"auth": "success"}; return RESPONSES["auth"]`

### Method Chaining & Builder Patterns
❌ **BLOCK:** Builders that assemble hardcoded responses
- `ResponseBuilder().success().data("fake").build()`

### Variable-Disguised Hardcoding
❌ **BLOCK:** Variables that hide hardcoded returns
- `result = "success"; status = result; return status`

### Ternary Operator Fakes
❌ **BLOCK:** Ternary operators with hardcoded outcomes
- `return "success" if True else "failed"`

### Import Alias Duplication
❌ **BLOCK:** Same model imported under different aliases in multiple test files

✅ **ALLOW:** Complex legitimate logic with real calculations, database operations, validation rules

## 🎯 DECISION MATRIX

**When evaluating code, ask in order:**

1. **File Creation:** Is this a duplicate test file or unwanted .md file? → BLOCK
2. **Comment Check:** Contains blocked comment patterns? → BLOCK
3. **Test Framework:** Using unittest patterns instead of pytest? → BLOCK
4. **Mock Patterns:** Using context managers instead of decorators? → BLOCK
5. **Implementation Review:** Hardcoded values or test-specific logic? → BLOCK
6. **Business Logic:** Does this work for any valid input? → ALLOW if yes
7. **TDD Flow:** Following Red-Green-Refactor properly? → ALLOW if yes

## 📝 ERROR RESPONSE TEMPLATE

**Format:** `❌ [VIOLATION TYPE] - [SPECIFIC ISSUE] → [SUGGESTION]`

**Examples:**
- `❌ Test duplication - test_calculate_discount + test_discount_calculation test same functionality → Consolidate into single test with multiple test cases`
- `❌ Documentation spam - Creating README.md without user request → Focus on code implementation, user will request docs when needed`
- `❌ Fake implementation - Hardcoded return "authenticated" → Implement real authentication logic with user validation`
- `❌ Unittest framework - Using class TestSomething(unittest.TestCase) → Use pytest flat functions: def test_something():`
- `❌ Context manager mocking - Using 'with patch()' pattern → Use @patch decorator above function definition`
- `❌ Multiple similar tests - Creating separate test_gold and test_silver functions → Use @pytest.mark.parametrize for similar test cases`

## Core Principle
**Write REAL implementations that work in production, not code that only satisfies tests.**

## Error Quality Requirements
- All blocked actions must include clear explanations
- Constructive suggestions for alternatives
- Specific examples where applicable
- Proper violation categorization
- No false positives on legitimate code

## Integration Notes
- **Meta-Module**: Provides structure for all other modules
- **Decision Flow**: Defines the order of validation checks
- **Error Standards**: Ensures consistent, helpful error messages
- **Always Required**: Core framework for TDD Guard operation
- **Template System**: Standardizes violation reporting across all modules
