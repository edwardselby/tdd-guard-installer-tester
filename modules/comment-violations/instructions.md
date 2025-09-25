# Test Comment Violations

## Priority Level: 1 (Critical Blocks - Highest Priority)

## 🚨 Test Comment Violations

### Implementation Awareness Comments
❌ **BLOCK COMMENTS INDICATING IMPLEMENTATION AWARENESS:**
Comments that reveal knowledge about implementation state violate TDD principles:
- Implementation status comments: "doesn't exist yet", "not implemented", "method doesn't exist", "not ready", "currently unimplemented"
- Phase awareness comments: "should FAIL", "RED PHASE", "GREEN PHASE", "Expected to fail"
- Future implementation comments: "TODO: Update when implementation", "Will fail until implemented"
- Dependency awareness comments: "waiting for backend", "waiting for completion", "pending other work"
- Pattern: Any comment suggesting the test knows about current implementation state