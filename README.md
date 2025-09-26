# TDD Guard Multi-Project Installer

A comprehensive interactive installer for deploying TDD Guard into any Python project with full Claude IDE integration. This tool auto-discovers projects in your workspace and enables developers to install tailored TDD enforcement rules through a modular, intelligent configuration system.

## 🎯 Project Overview

The **TDD Guard Multi-Project Installer** transforms TDD Guard deployment from manual configuration to an intelligent, cross-project installation process. The installer provides:

1. **Multi-Project Installation** - Auto-discover and install TDD Guard into any Python project in your workspace
2. **Interactive Module Selection** - Choose from 10 specialized TDD modules with smart defaults
3. **Automatic Package Installation** - Installs `tdd-guard-pytest` in target project's virtual environment
4. **Claude IDE Integration** - Seamless setup of hooks, model configuration, and ignore patterns
5. **Configuration Persistence** - Save and restore complete installer settings
6. **Enforcement Controls** - Advanced security settings for guard protection

**Key Features:**
- 🎯 **Multi-Project Installation** - Auto-discover and install into any Python project in your workspace
- 📦 **Automatic Package Installation** - Installs `tdd-guard-pytest` in target project's virtual environment
- 🔍 **Intelligent Project Discovery** - Auto-detects Flask, FastAPI, Django, and general Python projects
- 🎛️ **Interactive Installation Wizard** - Step-by-step project selection and configuration with intelligent defaults
- 🧩 **Modular Architecture** - 10 specialized modules covering all TDD violation types
- 🔧 **Claude IDE Integration** - Automatic hooks, instructions, and ignore pattern setup
- 🔐 **Security Enforcement** - Guard settings protection and file bypass blocking
- 💾 **Configuration Management** - Complete settings persistence and restoration
- ✅ **Production Ready** - Comprehensive test suite and validation

## 📋 Multi-Project Setup

The installer is designed to work across multiple projects in your workspace. Here's the recommended setup:

### Directory Structure
```
projects/
├── my-api-project/           ← Target project (Flask/FastAPI)
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   └── .venv/               ← Virtual environment (auto-detected)
├── my-web-app/              ← Another target project
│   ├── src/
│   ├── tests/
│   └── venv/                ← Virtual environment (auto-detected)
└── tdd-guard-installer/     ← This installer (run from here)
    ├── modules/
    ├── install.py
    └── generated/
```

### Prerequisites
- Python 3.8+ installed
- Target projects should have virtual environments (`.venv/`, `venv/`, `env/`, or `virtualenv/`)
- [Claude Code](https://claude.ai/code) (optional, for IDE integration)

### Installation

1. **Clone the installer into your projects directory:**
   ```bash
   cd /path/to/your/projects
   git clone https://github.com/your-org/tdd-guard-installer.git
   cd tdd-guard-installer
   ```

2. **Install installer dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the interactive installer:**
   ```bash
   python install.py
   ```

4. **Select your target project from the auto-discovered list**

The installer will:
- Auto-discover compatible Python projects in the parent directory
- Install `tdd-guard-pytest` in the target project's virtual environment
- Configure TDD Guard with your selected modules
- Set up Claude IDE integration in the target project

### Basic Usage

The installer provides a step-by-step interactive experience with automatic project discovery:

```bash
$ python install.py

==================================================
Target Project Selection
==================================================

Discovered 3 compatible project(s) in parent directory:

  1. my-api-project                  (Python - Flask)
     /Users/dev/projects/my-api-project
     Virtual env: ✓ Found (.venv)
     TDD Guard: Not installed

  2. my-web-app                      (Python - FastAPI)
     /Users/dev/projects/my-web-app
     Virtual env: ✓ Found (venv)
     TDD Guard: ⚠  Already installed

  3. [Custom Path] - Specify a different project location

Select target project [1-3]: 1

Selected: my-api-project
Path: /Users/dev/projects/my-api-project
Type: Python - Flask

Continue with this project? [*] Yes  [ ] No (y/n): y

Installing TDD Guard package...
----------------------------------------
✓ Using virtual environment: .venv
Running: /Users/dev/projects/my-api-project/.venv/bin/python -m pip install tdd-guard-pytest
✓ Successfully installed tdd-guard-pytest

TDD Guard Configuration Wizard
==================================================

Load previous configuration? [*] Yes  [ ] No (y/n):

Model Selection:
----------------------------------------
  1. [*] Claude 3.5 Haiku (Fast, efficient model for quick TDD validation)
  2. [ ] Claude 3.5 Sonnet (Balanced performance and capability)
  3. [ ] Claude Opus (Most capable model for complex scenarios)
Select model [1-3] (press Enter for default):

✓ Auto-including mandatory module for Claude 3.5 Haiku: Haiku JSON Formatting Fix

Module Selection (ordered by priority):
----------------------------------------
[*] Test File Duplication Prevention (+45 lines)
    Prevents creation of duplicate test files and similar test functions
Include this module? [*] Yes  [ ] No (y/n): y

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

==================================================
Installation Complete!
==================================================

Target Project: my-api-project
Location: /Users/dev/projects/my-api-project

Configuration:
  Modules: 6 modules selected
  Model: claude-3-5-haiku-20241022
  Package: tdd-guard-pytest ✓ Installed

Files created in target project:
  ✓ /Users/dev/projects/my-api-project/.claude/settings.local.json
  ✓ /Users/dev/projects/my-api-project/.claude/tdd-guard/data/instructions.md
  ✓ /Users/dev/projects/my-api-project/.claude/tdd-guard/data/config.json

Next steps:
  1. cd /Users/dev/projects/my-api-project
  2. Restart Claude Code to load new hooks
  3. Start writing tests with TDD Guard protection!
```

## 🎛️ Command Line Options

The installer supports multiple usage modes:

### Interactive Mode (Default) - With Project Selection
```bash
python install.py
```
Launches the full interactive installer with:
1. Auto-discovery of compatible projects in parent directory
2. Interactive project selection
3. Automatic package installation in target project
4. Step-by-step configuration with Claude IDE integration

### CLI Mode - Local Configuration Only
```bash
# Include all available modules (no project selection)
python install.py --all

# Select specific modules (no project selection)
python install.py core pytest test-duplication

# List available modules
python install.py --list
```
**Note:** CLI mode generates configuration files locally in the installer directory and does not perform cross-project installation or package installation.

### Help Documentation
```bash
python install.py --help
```
Display comprehensive help including all available options and workflow steps.

## 🧩 Available Modules

The installer includes 10 specialized TDD enforcement modules:

| Module | Priority | Default | Description |
|--------|----------|---------|-------------|
| **haiku-json-fix** | 0 | Auto | JSON formatting fix for Claude 3.5 Haiku (auto-included with Haiku model) |
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

## 🗺️ Project Compatibility

The installer automatically detects and supports various Python project types:

### Supported Project Types
| Project Type | Detection Criteria | Virtual Environment | Package Installation |
|--------------|-------------------|-------------------|---------------------|
| **Flask** | `flask` in requirements.txt/pyproject.toml | Required | ✓ Automatic |
| **FastAPI** | `fastapi` in requirements.txt/pyproject.toml | Required | ✓ Automatic |
| **Django** | `django` in requirements.txt/pyproject.toml | Required | ✓ Automatic |
| **General Python** | .git + (requirements.txt or pyproject.toml) | Required | ✓ Automatic |

### Project Requirements
- **Git Repository**: Project must be a git repository (`.git` directory present)
- **Python Dependencies**: Must have `requirements.txt` or `pyproject.toml`
- **Virtual Environment**: Must have one of: `.venv/`, `venv/`, `env/`, or `virtualenv/`
- **Write Permissions**: Installer must be able to create files in the project directory

### Virtual Environment Detection
The installer automatically detects virtual environments in this priority order:
1. `.venv/` (recommended)
2. `venv/`
3. `env/`
4. `virtualenv/`

For each detected environment, it verifies that the Python executable exists and is accessible.

### Project Discovery Process
1. **Scan Parent Directory**: Looks for sibling directories of the installer
2. **Validate Projects**: Checks for git repository and dependency files
3. **Detect Project Type**: Analyzes dependencies to determine framework
4. **Check Virtual Environment**: Locates and validates virtual environment
5. **Check TDD Guard Status**: Determines if TDD Guard is already installed

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

The installer creates files in two locations:

### Files Created in Installer Directory (for reference)
```
tdd-guard-installer/
└── generated/
    ├── instructions.md          # Combined TDD Guard rules (reference copy)
    ├── tests.md                # Test scenarios (optional)
    └── .last-config.json      # Configuration persistence
```

### Files Created in Target Project (active configuration)
```
target-project/
├── .claude/
│   ├── settings.local.json           # Model + hooks configuration
│   └── tdd-guard/
│       └── data/
│           ├── instructions.md       # IDE custom instructions (active)
│           └── config.json          # Ignore patterns configuration (active)
└── .venv/                            # Package installed here
    └── lib/python3.x/site-packages/
        └── tdd_guard_pytest/         # Installed package
```

**Important:** The active TDD Guard configuration lives in the target project, not the installer directory.

## 🚀 Advanced Configuration

### Configuration Persistence
The installer automatically saves your complete configuration to `generated/.last-config.json` with target project information:

```json
{
  "selected_modules": ["core", "pytest", "test-duplication", "haiku-json-fix"],
  "generate_tests": true,
  "target_path": "/Users/dev/projects/my-api-project",
  "model_id": "claude-3-5-haiku-20241022",
  "enable_hooks": true,
  "copy_instructions": true,
  "configure_ignore_patterns": true,
  "protect_guard_settings": true,
  "block_file_bypass": false
}
```

### Cross-Project Installation Benefits
- **Consistent Configuration**: Use the same installer settings across multiple projects
- **Team Deployment**: Clone installer once, deploy to multiple team projects
- **Environment Isolation**: Each project gets its own virtual environment installation
- **Project-Specific Customization**: Target project types (Flask/FastAPI/Django) can influence module recommendations

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

### Installer Structure
```
tdd-guard-installer/
├── install.py                         # Main installer implementation
├── modules/                           # 10 TDD enforcement modules
│   ├── haiku-json-fix/               # Haiku model JSON formatting fix
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
├── generated/                        # Installer output directory (reference)
├── docs/
│   └── CHANGELOG.md                  # Project evolution history
├── requirements.txt                   # Installer dependencies
└── README.md                         # This documentation
```

### Target Project Structure (after installation)
```
target-project/
├── app/                              # Your application code
├── tests/                            # Your tests
├── .venv/                            # Virtual environment with tdd-guard-pytest
├── .claude/                          # Claude IDE integration (created by installer)
│   ├── settings.local.json           # Model + hooks configuration
│   └── tdd-guard/
│       └── data/
│           ├── instructions.md       # Active TDD Guard rules
│           └── config.json          # Ignore patterns
├── requirements.txt                  # Your project dependencies
└── pyproject.toml                    # Your project configuration
```

## 🚫 Troubleshooting

### Common Installation Issues

#### Project Discovery Problems
**Issue**: "No compatible projects found in parent directory"
- **Solution**: Ensure you've cloned the installer into a directory that contains other Python projects
- **Check**: Parent directory should contain projects with `.git` and `requirements.txt`/`pyproject.toml`

#### Virtual Environment Issues
**Issue**: "No virtual environment detected in target project"
- **Solution**: Create a virtual environment in the target project:
  ```bash
  cd /path/to/target-project
  python -m venv .venv
  ```
- **Supported names**: `.venv`, `venv`, `env`, `virtualenv`

#### Package Installation Failures
**Issue**: "Failed to install tdd-guard-pytest"
- **Check**: Virtual environment has pip and internet access
- **Solution**: Manual installation:
  ```bash
  cd /path/to/target-project
  source .venv/bin/activate  # or Scripts\activate on Windows
  pip install tdd-guard-pytest
  ```

#### Permission Errors
**Issue**: "No write permission for project directory"
- **Solution**: Check file permissions and ownership
- **macOS/Linux**: `chmod 755 /path/to/target-project`
- **Windows**: Run installer as administrator

#### Claude IDE Integration Issues
**Issue**: "Failed to create hooks or copy instructions"
- **Solution**: Check that target project allows `.claude` directory creation
- **Manual setup**: Copy files from installer's `generated/` to target's `.claude/tdd-guard/data/`

## 🤝 Contributing

We welcome contributions to improve the TDD Guard Multi-Project Installer! Here's how to get started:

### Development Setup

1. **Fork and clone the repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run tests**: `python -m pytest tests/ -v`
4. **Test the installer**: `python install.py`

### Contributing Guidelines

- **Follow TDD practices** - Write tests first, implement minimal code to pass
- **Use pytest** - All tests should use pytest flat functions, not unittest classes
- **Maintain module structure** - Each module should have metadata.yaml and instructions.md
- **Update documentation** - Keep README and CHANGELOG current
- **Test across models** - Validate with different Claude models when possible
- **Test multi-project scenarios** - Verify installation across different project types

### Adding New Modules

To create a new TDD enforcement module:

1. **Create module directory**: `modules/your-module-name/`
2. **Add metadata.yaml**:
   ```yaml
   name: "Your Module Name"
   description: "Brief description of what this module enforces"
   priority: 5
   default: no
   auto_include_with_model: "claude-3-5-haiku-20241022"  # optional
   mandatory_for_model: false  # optional
   remove_from_ignore: ["*.py"]  # optional
   ```
3. **Create instructions.md** with TDD rules and patterns
4. **Test the module** using the installer across different project types
5. **Submit a pull request** with tests

### Testing Changes

Always test your changes thoroughly:
```bash
# Run the full test suite
python -m pytest tests/ -v --cov=install

# Test installer functionality
python install.py --list
python install.py your-new-module

# Test multi-project installation
# Set up test projects in parent directory and run:
python install.py  # Test project discovery and selection

# Validate module structure
python install.py --all
```

### Multi-Project Testing

When testing the installer:

1. **Create test projects** in parent directory with different frameworks
2. **Test project discovery** - Verify all projects are found and classified correctly
3. **Test virtual environment detection** - Create various venv structures
4. **Test package installation** - Verify `tdd-guard-pytest` installs correctly
5. **Test cross-project isolation** - Ensure configurations don't interfere

### Testing Across Project Types

Create test projects for each supported type:
```bash
# Flask project
touch requirements.txt
echo "flask==2.3.0" > requirements.txt
python -m venv .venv

# FastAPI project
touch requirements.txt
echo "fastapi==0.104.0" > requirements.txt
python -m venv venv

# Django project
touch requirements.txt
echo "django==4.2.0" > requirements.txt
python -m venv env
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

The TDD Guard Multi-Project Installer makes TDD enforcement accessible, scalable across projects, and maintainable. Deploy once, protect everywhere! Happy testing!