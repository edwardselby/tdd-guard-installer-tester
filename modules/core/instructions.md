# Core TDD Workflow Enforcement

## Priority Level: 4 (TDD Workflow)

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