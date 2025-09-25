# Fake Implementation Detection

## Priority Level: 2 (Second Priority)

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