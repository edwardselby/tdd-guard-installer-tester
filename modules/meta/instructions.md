# Meta: Decision Matrix & Error Templates

## Priority Level: 7 (Meta-Rules)

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