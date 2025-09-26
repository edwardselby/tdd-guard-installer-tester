# TDD Guard Rules

## ⚡ JSON Response Formatting (For Haiku Model)

**CRITICAL**: When responding to TDD Guard validation requests, ensure proper JSON formatting:

### JSON Escaping Rules
- **Escape quotes in code**: `return "authenticated"` → `return \\"authenticated\\"`
- **Escape newlines**: `\n` → `\\n`
- **Escape backslashes**: `\` → `\\\\`
- **Escape control characters**: Remove or escape tab, carriage return, form feed

### Valid JSON Structure
Always use proper JSON structure for responses:
```json
{
  "violation_type": "string",
  "message": "string",
  "suggestion": "string"
}
```

### Code Content in JSON
When including code snippets in JSON responses:
- Original: `def auth(): return "ok"`
- JSON: `"code": "def auth(): return \\"ok\\""`

### Multi-line Code in JSON
For multi-line code:
- Original:
  ```python
  def authenticate():
      return "authenticated"
  ```
- JSON: `"code": "def authenticate():\\n    return \\"authenticated\\""`

**This module fixes JSON parsing errors that occur when Haiku model processes authentication functions and other string-heavy code patterns.**
