# Test File Duplication Prevention

## Priority Level: 1 (Critical Blocks - Highest Priority)

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