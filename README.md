# TDD Guard Configuration Wizard

A comprehensive interactive wizard for generating custom TDD Guard instructions with full Claude IDE integration. This tool enables developers to create tailored TDD enforcement rules through a modular, intelligent configuration system.

## 🎯 Project Overview

The **TDD Guard Configuration Wizard** transforms TDD Guard setup from manual configuration to an intelligent, interactive process. The wizard provides:

1. **Interactive Module Selection** - Choose from 9 specialized TDD modules with smart defaults
2. **Claude IDE Integration** - Seamless setup of hooks, model configuration, and ignore patterns
3. **Configuration Persistence** - Save and restore complete wizard settings
4. **Enforcement Controls** - Advanced security settings for guard protection

**Key Features:**
- 🎛️ **Interactive Wizard** - Step-by-step configuration with intelligent defaults
- 🧩 **Modular Architecture** - 9 specialized modules covering all TDD violation types
- 🔧 **Claude IDE Integration** - Automatic hooks, instructions, and ignore pattern setup
- 🔐 **Security Enforcement** - Guard settings protection and file bypass blocking
- 💾 **Configuration Management** - Complete settings persistence and restoration
- ✅ **Production Ready** - Comprehensive test suite and validation

### Prerequisites
- Python 3.8+ installed
- [TDD Guard](https://github.com/nizos/tdd-guard) CLI tool available
- [Claude Code](https://claude.ai/code) (optional, for IDE integration)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/tdd-guard-test.git
   cd tdd-guard-test
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the interactive wizard:**
   ```bash
   python install.py
   ```

### Basic Usage

The wizard provides a step-by-step interactive experience:

```bash
$ python install.py

TDD Guard Configuration Wizard
==================================================

Load previous configuration? [*] Yes  [ ] No (y/n):

Module Selection (ordered by priority):
----------------------------------------
[*] Test File Duplication Prevention (+45 lines)
    Prevents creation of duplicate test files and similar test functions
Include this module? [*] Yes  [ ] No (y/n): y

Model Selection:
----------------------------------------
  1. [*] Claude 3.5 Haiku (Fast, efficient model for quick TDD validation)
  2. [ ] Claude 3.5 Sonnet (Balanced performance and capability)
  3. [ ] Claude Opus (Most capable model for complex scenarios)
Select model [1-3] (press Enter for default):

Claude IDE Integration:
----------------------------------------
Enable TDD Guard hooks in Claude IDE? [*] Yes  [ ] No (y/n): y
Copy instructions to Claude IDE custom instructions? [*] Yes  [ ] No (y/n): y
Configure ignore patterns for Claude IDE? [*] Yes  [ ] No (y/n): y

Enforcement Configuration:
----------------------------------------
Enable Guard Settings Protection? [*] Yes  [ ] No (y/n): y
Block File Operation Bypass? [ ] Yes  [*] No (y/n): n

Generate test scenarios? [*] Yes  [ ] No (y/n): y
```

## 🎛️ Command Line Options

The wizard supports multiple usage modes:

### Interactive Mode (Default)
```bash
python install.py
```
Launches the full interactive wizard with step-by-step configuration.

### CLI Mode
```bash
# Include all available modules
python install.py --all

# Select specific modules
python install.py core pytest test-duplication

# List available modules
python install.py --list
```

### Help Documentation
```bash
python install.py --help
```
Display comprehensive help including all available options and workflow steps.

## 🧩 Available Modules

The wizard includes 9 specialized TDD enforcement modules:

| Module | Priority | Default | Description |
|--------|----------|---------|-------------|
| **test-duplication** | 1 | ✅ Yes | Prevents duplicate test files and similar test functions |
| **comment-violations** | 1 | ✅ Yes | Blocks implementation-aware comments violating TDD principles |
| **quality-control** | 1 | ✅ Yes | Prevents documentation spam and celebration debug scripts |
| **fake-implementation** | 2 | ✅ Yes | Detects hardcoded returns and test-specific logic patterns |
| **backend-frameworks** | 3 | ✅ Yes | Allows legitimate Flask/FastAPI patterns while blocking fakes |
| **core** | 4 | ✅ Yes | Enforces Red-Green-Refactor cycle and proper TDD timing |
| **pytest** | 5 | ❌ No | Enforces pytest patterns over unittest framework |
| **advanced-evasion** | 6 | ❌ No | Catches sophisticated fake implementation patterns |
| **meta** | 7 | ✅ Yes | Provides error templates and validation decision flow |

## 🔧 Claude IDE Integration Features

### Automatic Configuration
The wizard automatically configures Claude IDE for optimal TDD Guard integration:

#### 1. Model Selection
- **Claude 3.5 Haiku** - Fast validation for quick feedback
- **Claude 3.5 Sonnet** - Balanced performance (recommended)
- **Claude Opus** - Advanced reasoning for complex scenarios

#### 2. Hooks Configuration
Updates `.claude/settings.local.json` with TDD Guard hooks:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit|TodoWrite",
        "hooks": [{"type": "command", "command": "tdd-guard"}]
      }
    ]
  }
}
```

#### 3. Ignore Patterns Management
Intelligently configures which files TDD Guard should validate:
- **Default Ignored**: `*.log`, `*.json`, `*.yml`, `*.html`, `*.css`
- **Module-Specific Removal**: Some modules remove patterns (e.g., quality-control removes `*.md` and `*.txt`)

#### 4. Enforcement Configuration
- **Guard Settings Protection**: Prevents agents from reading TDD Guard configuration
- **File Bypass Blocking**: Blocks shell commands that circumvent TDD validation

## 🧪 Testing the System

### Running the Test Suite

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=tools --cov-report=html

# Test specific functionality
python -m pytest tests/test_generate.py::test_module_info_loads_metadata_correctly -v
```

### Test Coverage
The project includes 10 comprehensive tests covering:
- Module metadata parsing and discovery
- Configuration persistence and loading
- Claude IDE integration functions
- File generation and validation
- User input handling

### Manual Testing Examples

Test the wizard's TDD Guard integration:

```python
# This should be allowed (real business logic)
def calculate_discount(customer_type, amount):
    discount_rates = {"PREMIUM": 0.15, "STANDARD": 0.05}
    return amount * (1 - discount_rates.get(customer_type, 0))

# This should be blocked (hardcoded fake implementation)
def calculate_discount(customer_type, amount):
    return 850.0  # Hardcoded return value
```

## 📁 Generated Files

The wizard creates several output files based on your configuration:

### Core Output Files
```
generated/
├── instructions.md          # Combined TDD Guard rules
├── tests.md                # Test scenarios (optional)
└── .last-config.json      # Configuration persistence
```

### Claude IDE Integration Files
```
.claude/
├── settings.local.json           # Model + hooks configuration
└── tdd-guard/
    └── data/
        ├── instructions.md       # IDE custom instructions
        └── config.json          # Ignore patterns configuration
```

## 🚀 Advanced Configuration

### Configuration Persistence
The wizard automatically saves your complete configuration to `generated/.last-config.json`:

```json
{
  "selected_modules": ["core", "pytest", "test-duplication"],
  "generate_tests": true,
  "model_id": "claude-3-5-sonnet-20241022",
  "enable_hooks": true,
  "copy_instructions": true,
  "configure_ignore_patterns": true,
  "protect_guard_settings": true,
  "block_file_bypass": false
}
```

### Module Development
Each module follows a consistent structure:

```
modules/module-name/
├── metadata.yaml           # Module configuration
├── instructions.md         # TDD rules and patterns
└── test-scenarios.md      # Test examples (optional)
```

**metadata.yaml example:**
```yaml
name: "Test Duplication Prevention"
description: "Prevents creation of duplicate test files"
priority: 1
default: yes
remove_from_ignore:
  - "test_*.py"
```

## 📊 Project Structure

```
tdd-guard-test/
├── install.py                         # Main wizard implementation
├── modules/                           # 9 TDD enforcement modules
│   ├── core/                         # Red-Green-Refactor enforcement
│   ├── test-duplication/             # Duplicate test prevention
│   ├── fake-implementation/          # Hardcoded detection
│   ├── comment-violations/           # Implementation-aware comments
│   ├── quality-control/              # Documentation spam prevention
│   ├── backend-frameworks/           # Framework pattern allowlist
│   ├── pytest/                       # pytest-specific patterns
│   ├── advanced-evasion/             # Sophisticated fake detection
│   ├── meta/                         # Error templates and decision flow
│   └── models.yaml                   # Claude model configurations
├── tests/
│   └── test_generate.py              # Comprehensive test suite (10 tests)
├── generated/                        # Wizard output directory
├── docs/
│   └── CHANGELOG.md                  # Project evolution history
├── .claude/                          # Claude IDE integration
│   ├── settings.local.json           # Local IDE configuration
│   └── tdd-guard/data/              # TDD Guard IDE files
├── requirements.txt                   # Project dependencies
└── README.md                         # This documentation
```

## 🤝 Contributing

We welcome contributions to improve the TDD Guard Configuration Wizard! Here's how to get started:

### Development Setup

1. **Fork and clone the repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run tests**: `python -m pytest tests/ -v`
4. **Test the wizard**: `python install.py`

### Contributing Guidelines

- **Follow TDD practices** - Write tests first, implement minimal code to pass
- **Use pytest** - All tests should use pytest flat functions, not unittest classes
- **Maintain module structure** - Each module should have metadata.yaml and instructions.md
- **Update documentation** - Keep README and CHANGELOG current
- **Test across models** - Validate with different Claude models when possible

### Adding New Modules

To create a new TDD enforcement module:

1. **Create module directory**: `modules/your-module-name/`
2. **Add metadata.yaml**:
   ```yaml
   name: "Your Module Name"
   description: "Brief description of what this module enforces"
   priority: 5
   default: no
   ```
3. **Create instructions.md** with TDD rules and patterns
4. **Test the module** using the wizard
5. **Submit a pull request** with tests

### Testing Changes

Always test your changes thoroughly:
```bash
# Run the full test suite
python -m pytest tests/ -v --cov=tools

# Test wizard functionality
python install.py --list
python install.py your-new-module

# Validate module structure
python install.py --all
```

## 📚 References

- **[TDD Guard](https://github.com/nizos/tdd-guard)** - Main TDD Guard repository and documentation
- **[Claude Code](https://claude.ai/code)** - Claude IDE for AI-assisted development
- **[Test-Driven Development](https://martinfowler.com/bliki/TestDrivenDevelopment.html)** - TDD methodology by Martin Fowler
- **[pytest Documentation](https://docs.pytest.org/)** - Python testing framework
- **[TDD Guard Enforcement](https://github.com/nizos/tdd-guard/blob/main/docs/enforcement.md)** - Advanced enforcement features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

If you encounter issues or have questions:

1. **Check the documentation** in this README
2. **Review the CHANGELOG** for recent changes
3. **Run the test suite** to verify your setup
4. **Open an issue** on GitHub with detailed information

---

**Built with ❤️ for Test-Driven Development**

The TDD Guard Configuration Wizard makes TDD enforcement accessible, configurable, and maintainable. Happy testing!