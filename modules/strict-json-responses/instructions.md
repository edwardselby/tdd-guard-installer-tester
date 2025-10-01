# Strict JSON Response Format

## Priority Level: 0 (Auto-included with Claude 3.5 Haiku)

This module enforces strict JSON formatting in all validation responses to prevent JSON parsing errors when validating large or complex files.

---

## 🚫 Response Formatting Rules

### ❌ **BLOCK Response Patterns:**

- Including raw code snippets in validation reasoning
- Multi-line quoted code blocks in JSON values
- Unescaped newlines (`\n`) or special characters in reasoning text
- Embedding function/class definitions in responses
- Quoting user's file content verbatim
- Large reasoning text for files >150 lines

### ✅ **ALLOW Response Patterns:**

- Brief code references (e.g., "the test_user_workflow function")
- Summarized behavior descriptions without quotes
- Properly escaped JSON strings
- Compact reasoning (max 200 characters for files >150 lines)
- Line number references instead of code quotes (e.g., "lines 50-100")
- Single-line reasoning preferred

---

## 📋 JSON Response Format Requirements

### For Large Files (150+ lines):
- **Reasoning**: Maximum 200 characters
- **Format**: `{"reasoning": "Brief summary", "allowed": true/false}`
- **NO** code snippets or multi-line content
- Reference by line numbers, not content quotes

### For All Files:
- Properly escape special characters: `\n`, `\r`, `\t`, `"`, `\`
- Use compact summaries, not verbatim quotes
- Single-line reasoning preferred
- Keep JSON structure minimal and clean

---

## ✅ GOOD Response Examples

### Large file validation:
```json
{"reasoning": "Test covers complete workflow (lines 1-307). Violates TDD single-focus principle.", "allowed": false}
```

### Alternative for same scenario:
```json
{"reasoning": "Integration test detected. Recommend splitting into unit tests per step.", "allowed": false}
```

### Allowing a valid test:
```json
{"reasoning": "Single-focus unit test following TDD principles.", "allowed": true}
```

---

## ❌ BAD Response Examples (Causes JSON Parsing Errors)

### Including code snippets (CAUSES ERROR):
```json
{"reasoning": "Function:\ndef test_workflow():\n    \"\"\"Long docstring...\"\"\"\n    query = \"SELECT...\"", "allowed": false}
```
**Error**: Unescaped newlines break JSON parsing at validator.js:25

### Verbatim code quoting (CAUSES ERROR):
```json
{"reasoning": "Test contains:\n    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'\n    This violates...", "allowed": false}
```
**Error**: "Bad control character in string literal in JSON"

### Large unescaped content (CAUSES ERROR):
```json
{"reasoning": "The test function has a 50-line docstring that explains: \"Test Flow:\n1. User Registration...\n2. Email Verification...\"", "allowed": false}
```
**Error**: "Unterminated string in JSON"

---

## 🔧 Module Behavior

**Scope**: Claude CLI validation response formatting only

**Does NOT affect**:
- Code validation logic
- TDD enforcement rules
- Other module behaviors

**Target Error**: "Bad control character in string literal in JSON" at validator.js:25

**Expected Impact**:
- JSON parsing error rate: 67% → <5%
- Overall success rate: 0% → ~60-65%
- TDD violations remain at ~33% (legitimate enforcement)

---

## 📊 Response Strategy by File Size

| File Size | Max Reasoning Length | Strategy |
|-----------|---------------------|----------|
| <50 lines | 500 characters | Normal detailed reasoning |
| 50-150 lines | 300 characters | Concise reasoning with key points |
| >150 lines | 200 characters | Minimal summary, line references only |

---

## 🎯 Key Principles

1. **Never quote code**: Summarize behavior instead
2. **Always escape**: Ensure all JSON strings are properly escaped
3. **Stay compact**: Large files need minimal reasoning
4. **Reference locations**: Use line numbers, not content
5. **Single-line preferred**: Avoid multi-line reasoning text
