# Quality Control Standards

## Priority Level: 1 (Critical Blocks - Highest Priority)

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