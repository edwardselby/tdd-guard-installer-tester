# TDD Guard Testing Repository

A dedicated repository for testing and validating the [TDD Guard](https://github.com/nizos/tdd-guard) system using various AI models and instruction configurations.

## 🎯 Purpose

This repository is designed to:
- Test TDD Guard's ability to enforce Test-Driven Development principles
- Validate instruction effectiveness across different AI model capabilities
- Ensure TDD Guard understands TDD concepts rather than just pattern matching
- Provide a controlled environment for TDD Guard development and improvement

## 🚀 Quick Start with Claude Code

### Prerequisites
- [Claude Code](https://claude.ai/code) installed and configured
- [TDD Guard](https://github.com/nizos/tdd-guard) extension enabled in your Claude Code environment

### Basic Setup

1. **Clone this repository:**
   ```bash
   git clone git@github.com:edwardselby/tdd-guard-testing.git
   cd tdd-guard-testing
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure TDD Guard model (optional):**
   - Default model: Claude Sonnet 4.0
   - For testing with less capable models, see [Model Configuration](#model-configuration)

4. **Enable TDD Guard in Claude Code:**
   ```bash
   # Enable TDD Guard for this session
   tdd-guard on

   # Disable TDD Guard when needed
   tdd-guard off
   ```

## 📋 Testing TDD Guard

### Running Test Scenarios

The repository includes comprehensive test scenarios in `INSTRUCTIONS_V1_TESTING.md`. These tests validate:

- **Fake Implementation Detection**: Hardcoded returns, test-specific logic
- **Test Duplication Prevention**: Various forms of duplicate test files
- **Comment Violations**: Implementation-aware comments that violate TDD principles
- **Documentation Control**: Prevention of unnecessary documentation files

### Example Test Session

1. **Enable TDD Guard:**
   ```bash
   tdd-guard on
   ```

2. **Try creating a test with hardcoded implementation:**
   ```python
   # This should be blocked by TDD Guard
   def authenticate_user(username, password):
       return "authentication_successful"  # Hardcoded fake implementation
   ```

3. **Try creating duplicate tests:**
   ```bash
   # These should be blocked as duplicates
   touch tests/test_user_auth.py
   touch tests/test_auth_user.py  # Similar functionality = duplicate
   ```

4. **Try adding implementation-aware comments:**
   ```python
   def test_user_login():
       """This method doesn't exist yet"""  # Should be blocked
       result = login_user("test", "pass")
       assert result == True
   ```

## ⚙️ Model Configuration

### Using Different AI Models

TDD Guard can be configured to use different Claude models for testing instruction robustness:

**Local Configuration (`.claude/settings.local.json`):**
```json
{
  "env": {
    "VALIDATION_CLIENT": "sdk",
    "TDD_GUARD_MODEL_VERSION": "claude-3-5-haiku-20241022"
  }
}
```

**Available Models:**
- `claude-3-5-haiku-20241022` - Fastest, least capable (good for testing instruction clarity)
- `claude-sonnet-4-0` - Default, balanced performance
- `claude-opus-4-1` - Most capable, slowest

### Why Test with Different Models?

- **Haiku**: Tests if instructions are clear enough for less capable models
- **Sonnet**: Standard performance baseline
- **Opus**: Validates complex reasoning scenarios

## 📊 Understanding TDD Guard Results

### ✅ Expected Blocks (TDD Guard Working)
- Hardcoded return values (`return "test_result"`)
- Test-specific conditionals (`if username == "testuser"`)
- Duplicate test files (`test_user_v2.py`, `test_enhanced_user.py`)
- Implementation-aware comments (`"method doesn't exist yet"`)
- Unnecessary documentation files (`README.md`, `API_GUIDE.txt`)

### ❌ Expected Passes (Valid TDD)
- Proper failing tests that drive implementation
- Real business logic implementations
- Appropriate test structure and naming
- Legitimate refactoring of passing code

## 📁 Project Structure

```
tdd-guard-testing/
├── .claude/
│   ├── settings.json           # Claude Code configuration
│   ├── settings.local.json     # Local model configuration (gitignored)
│   └── tdd-guard/
│       └── data/
│           └── instructions.md # Enhanced TDD Guard rules
├── tests/
│   └── unit/
│       └── test_task_model.py  # Original test file
├── app/                        # Sample Flask application
├── INSTRUCTIONS_V1.md          # TDD Guard instruction reference
├── INSTRUCTIONS_V1_TESTING.md # Test scenario documentation
└── README.md                   # This file
```

## 🧪 Advanced Testing

### Custom Test Scenarios

Create your own test scenarios by:

1. **Writing edge cases** that test TDD Guard's understanding
2. **Testing principle violations** in subtle ways
3. **Validating instruction improvements** with specific scenarios

### Instruction Development

The enhanced instructions in `.claude/tdd-guard/data/instructions.md` have been tested and validated to:
- Achieve 100% success rate on comprehensive test scenarios
- Work effectively with less capable AI models
- Focus on TDD principles rather than pattern matching

## 📈 Results and Metrics

Current TDD Guard performance with enhanced instructions:
- **Success Rate**: 100% on 93 test scenarios
- **Model Compatibility**: Tested with Haiku, Sonnet, and Opus
- **Principle-Based Detection**: Successfully catches variations not explicitly listed in patterns

## 🤝 Contributing

This repository serves as a testing ground for TDD Guard improvements. When contributing:

1. **Test new scenarios** thoroughly
2. **Validate across multiple models** (especially Haiku for instruction clarity)
3. **Focus on principles** over patterns
4. **Document findings** and edge cases

## 📚 Reference

- **[TDD Guard GitHub](https://github.com/nizos/tdd-guard)** - Main TDD Guard repository
- **[Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)** - Claude Code usage guide
- **[Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)** - TDD methodology reference

---

**Remember**: The goal is to ensure TDD Guard understands and enforces TDD principles, not just memorizes patterns. Test with intelligence and validate with rigor.