# Advanced Evasion Detection

## Priority Level: 6 (Advanced Patterns)

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