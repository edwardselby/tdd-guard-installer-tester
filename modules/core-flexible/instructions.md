# Core TDD Workflow Enforcement (Flexible - Batch Mode)

## Priority Level: 4 (TDD Workflow)

## 🔄 TDD WORKFLOW ENFORCEMENT

### Test Creation Rules (Batch-Based TDD)
❌ **BLOCK:** More than 3 test functions in single operation
❌ **BLOCK:** Tests that pass immediately (trivial assertions like `2 + 2 == 4`)
✅ **ALLOW:** Up to 3 tests per batch for ANY scenario:
  - Multiple tests for the same function (boundary values, error conditions, type variations)
  - Tests for different functions in the same module
  - Tests for different classes/methods
  - Mix of unit tests across related functionality
  - Any combination that makes logical sense for the feature being developed
✅ **ALLOW:** Flexible batching - agent decides best grouping (1-3 tests) based on context
✅ **ALLOW:** Single test when appropriate for complex/exploratory behaviors

### Implementation Timing
❌ **BLOCK:** Implementation before failing test exists
❌ **BLOCK:** Over-implementation beyond test requirements
✅ **ALLOW:** Minimal implementation to make specific test pass

### Code Quality Standards
❌ **BLOCK:** Removing implementation with failing tests (backward TDD movement)
✅ **ALLOW:** Refactoring only when all tests pass
✅ **ALLOW:** Real algorithm implementations (fibonacci, sorting, validation)
