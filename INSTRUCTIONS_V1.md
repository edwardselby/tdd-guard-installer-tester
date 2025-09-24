# TDD Guard Rules - AI Processing Optimized

## 🚨 CRITICAL BLOCKS - CHECK FIRST (Highest Priority)

### Test File Duplication Prevention
❌ **BLOCK PATTERNS:**
- `test_*_v[0-9]*.py` → Block versioned files (test_module_v2.py)
- `test_*_new.py` → Block "new" suffixed files
- `test_*_refactored.py` → Block "refactored" suffixed files
- `test_*_revised.py` → Block "revised" suffixed files
- `test_enhanced_*.py` → Block "enhanced" prefixed files
- `test_*_enhanced.py` → Block "enhanced" suffixed files
- **Similar test names** → Block when pattern: test_WORD1_WORD2 + test_WORD2_WORD1
  - Example: `test_calculate_discount` + `test_discount_calculation` = SAME FUNCTIONALITY
  - Example: `test_user_login` + `test_login_user` = DUPLICATE TEST
- **Word-form variations** → Block: test_VERB_NOUN + test_NOUN_VERBING
  - Example: `test_process_payment` + `test_payment_processing` = DUPLICATE
- **Singular/plural variations** → Block: test_WORD + test_WORDs
  - Example: `test_process_payment` + `test_process_payments` = DUPLICATE
  - Pattern: Base words identical, differs only by 's', 'es', 'ies' suffix → BLOCK
- **Cross-directory duplicates** → Block: identical filenames across test directories
  - Pattern: `tests/*/test_FILENAME.py` = Check filename across ALL test subdirectories
  - Example: `tests/unit/test_task.py` + `tests/integration/test_task.py` = DUPLICATE
- Multiple test functions in single file creation
- **Import-based duplicates** → Block: Multiple test files importing same modules
  - Pattern: Check import statements across test files for identical module imports
  - Example: test_pricing.py imports Task, test_task_model.py imports Task = DUPLICATE
  - Action: "Multiple test files testing same module → Consolidate into single test file"
  - Exception: Different test types allowed: test_user.py (unit), test_user_integration.py (integration)
- **Pattern matching priority**: Check base words first, then suffixes, then directory paths
  - Algorithm: Remove `test_` prefix → Compare core words → Check suffix patterns → Check cross-directory

**Action:** Direct to update existing test file instead of creating new ones.

### Documentation File Prevention
❌ **BLOCK DOCUMENTATION FILE CREATION:**
- `.md`, `.txt` files: `README.md`, `CHANGELOG.md`, `API.md`, `user_guide.txt`, etc.
- ANY documentation file unless user explicitly requests documentation
- Exception: `.rst` files allowed per project requirements
- Assumption: User wants code, not documentation spam

### Test Comment Violations
❌ **BLOCK COMMENTS INDICATING IMPLEMENTATION AWARENESS:**
Comments that reveal knowledge about implementation state violate TDD principles:
- Implementation status comments: "doesn't exist yet", "not implemented", "method doesn't exist", "not ready", "currently unimplemented"
- Phase awareness comments: "should FAIL", "RED PHASE", "GREEN PHASE", "Expected to fail"
- Future implementation comments: "TODO: Update when implementation", "Will fail until implemented"
- Dependency awareness comments: "waiting for backend", "waiting for completion", "pending other work"
- Pattern: Any comment suggesting the test knows about current implementation state

### Debug Script Quality Control
❌ **BLOCK CELEBRATION PATTERNS:**
- "🎉", "💯", "PRODUCTION READY", "WORKING PERFECTLY"
- "ALL SYSTEMS OPERATIONAL", "COMPREHENSIVE DEBUG ANALYSIS"
- Excessive formatting, multiple unrelated tests in one script
- Self-congratulatory messages about functionality working

**Requirement:** Debug scripts must test ONE specific thing with clean pass/fail output.

## ⚠️ FAKE IMPLEMENTATION DETECTION (Second Priority)

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

## 📋 IMPLEMENTATION REQUIREMENTS (Third Priority)

### Real Business Logic Standards
✅ **REQUIRED IMPLEMENTATION APPROACH:**
- Must work for ANY valid input, not just test cases
- Generic solutions using lookup tables, algorithms, validation logic
- Example: `discounts = {"GOLD": 0.20}; return price * (1 - discounts.get(type, 0))`
- Handle edge cases and error conditions appropriately
- Production-ready complexity matching the problem scope

### Backend Framework Patterns (Allowed)
✅ **LEGITIMATE BACKEND IMPLEMENTATIONS:**
- Flask routes: `@app.route('/api/users', methods=['GET', 'POST'])`
- Database queries: `User.query.filter_by(id=user_id).first()`
- Request handling: `request.json`, parameter validation
- Authentication: Token validation, session management
- API responses: JSON serialization, proper status codes

## 🔄 TDD WORKFLOW ENFORCEMENT (Fourth Priority)

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

## 🎯 DECISION MATRIX

**When evaluating code, ask in order:**

1. **File Creation:** Is this a duplicate test file or unwanted .md file? → BLOCK
2. **Comment Check:** Contains blocked comment patterns? → BLOCK
3. **Implementation Review:** Hardcoded values or test-specific logic? → BLOCK
4. **Business Logic:** Does this work for any valid input? → ALLOW if yes
5. **TDD Flow:** Following Red-Green-Refactor properly? → ALLOW if yes

## 📝 ERROR RESPONSE TEMPLATE

**Format:** `❌ [VIOLATION TYPE] - [SPECIFIC ISSUE] → [SUGGESTION]`

**Examples:**
- `❌ Test duplication - test_calculate_discount + test_discount_calculation test same functionality → Consolidate into single test with multiple test cases`
- `❌ Documentation spam - Creating README.md without user request → Focus on code implementation, user will request docs when needed`
- `❌ Fake implementation - Hardcoded return "authenticated" → Implement real authentication logic with user validation`

---

**Core Principle:** Write REAL implementations that work in production, not code that only satisfies tests.