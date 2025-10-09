# Core TDD Workflow Enforcement (Flexible)

## Priority Level: 4 (TDD Workflow)

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
