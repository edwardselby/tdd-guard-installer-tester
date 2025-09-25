# TDD Guard Rules

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
❌ **BLOCK:** Multiple test functions in single operation
❌ **BLOCK:** Tests that pass immediately (trivial assertions like `2 + 2 == 4`)
✅ **ALLOW:** One failing test at a time following Red-Green-Refactor

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
