# Changelog

All notable changes to the TDD Guard Multi-Project Installer project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.4.0] - 2025-10-09

### Added
- **Exclusive Core Modules**: Users can now choose TDD strictness level during installation
  - **Core TDD (Strict)**: One test at a time, maximum discipline (default, STRONGLY RECOMMENDED)
  - **Core TDD (Flexible)**: 2-3 similar tests allowed for efficiency
  - Mutually exclusive selection via new `exclusive_group` metadata field
  - Radio selection UI in wizard for exclusive groups ("SELECT ONE" interface)

### Changed
- **Module Selection UX**: Enhanced wizard interface
  - Exclusive groups display as radio buttons (select ONE from group)
  - Standalone modules continue as checkboxes (select multiple)
  - Groups sorted and displayed before standalone modules

### Technical Details
- Added `exclusive_group` property to `ModuleInfo` class (install.py:448)
- Updated `run_wizard()` with exclusive group selection logic (install.py:928-998)
- Created `modules/core-strict/` (renamed from `modules/core/`)
- Created `modules/core-flexible/` (new module with flexible TDD rules)
- All 20 tests passing - no breaking changes to existing functionality

### Files Modified/Created
- Created: `modules/core-flexible/instructions.md` (24 lines)
- Created: `modules/core-flexible/metadata.yaml`
- Created: `modules/core-flexible/test-scenarios.md`
- Renamed: `modules/core/` → `modules/core-strict/`
- Modified: `modules/core-strict/metadata.yaml` (added exclusive_group field)
- Modified: `install.py` (ModuleInfo property + wizard logic)

## [3.3.1] - 2025-10-08

### Fixed
- **Pytest Auto-Approval Availability**: Removed Flask-only restriction for pytest auto-approval
  - Feature now available for **all Python projects** with pytest module selected
  - Previously only prompted for Flask projects, now works for Flask, FastAPI, Django, and general Python projects
  - Updated condition from `project_type == "Python - Flask" and "pytest" in selected_modules` to `"pytest" in selected_modules`
  - Addresses issue where pytest auto-approval was not offered during installation for non-Flask projects

### Technical Details
- Modified file: `install.py` (line 966)
- Tests remain valid as they test the functionality, not the Flask-specific condition
- No breaking changes - expands feature availability

## [3.3.0] - 2025-10-08

### Changed
- **Default Model**: Changed from Claude 3.5 Haiku to Claude Sonnet 4.0
  - Sonnet 4 provides better performance and reliability for TDD validation
  - Haiku remains available as an option but is no longer the default
  - Updated `modules/models.yaml` default flag
  - Updated fallback defaults in `install.py` (3 locations)
  - Updated test expectations in `tests/test_install.py`
  - Updated documentation example in `README.md`

### Technical Details
- Modified files: `modules/models.yaml`, `install.py`, `tests/test_install.py`, `README.md`
- Backward compatibility maintained: existing installations and saved configurations unaffected
- All model options remain available for selection during installation

## [3.2.0] - 2025-10-08

### Added
- **Automatic Pytest Command Approval**: Flask projects with pytest module now support automatic test command approval
  - Adds pytest patterns to `permissions.allow` in `.claude/settings.local.json`
  - Auto-approves: `FLASK_ENV=TESTING poetry run pytest`, `poetry run pytest`, and `pytest` commands
  - Only prompts when project type is Flask and pytest module is selected
  - Persists setting in `.last-config.json` for configuration restoration
  - Displays approval status in installation results

### Enhanced
- **Wizard Flow**: Added conditional "Test Automation" step for Flask/pytest projects
- **Project Type Detection**: Enhanced to pass project type through wizard workflow
- **Configuration Management**: Extended IDE config structure with `auto_approve_pytest` field
- **Installation Results**: Added pytest auto-approval status to summary output

### Technical Improvements
- Added `configure_auto_approve_pytest()` function following existing IDE integration pattern
- Updated `run_wizard()` to accept optional `project_type` parameter
- Enhanced `save_config()` and config loading to persist pytest approval preference
- Comprehensive test coverage with 2 new tests for auto-approval feature

### Files Enhanced
- `install.py` - Auto-approve pytest configuration (Lines 759-802, 917-922, 1037, 1138, 1201-1204)
- `tests/test_install.py` - Test coverage for pytest auto-approval (Lines 292-328)
- `.claude/settings.local.json` (in target projects) - Pytest command permissions

### Tests
- Fixed 3 pre-existing test failures to match current codebase
- All 20 tests passing (18 original + 2 new pytest auto-approval tests)

## [3.1.0] - 2025-10-01

### Added
- **Strict JSON Response Format Module**: Fixes JSON parsing errors in large file validation
  - Reduces JSON parsing errors from 67% to 0%

### Removed
- **Haiku JSON Fix Module**: Replaced by strict-json-responses module

## [3.0.0] - 2024-09-26

### Major: Multi-Project Installation Support
- **🎯 Multi-Project Discovery**: Auto-discover and select from compatible Python projects in workspace
- **📦 Automatic Package Installation**: Install `tdd-guard-pytest` directly in target project's virtual environment
- **🔍 Project Type Detection**: Automatically identify Flask, FastAPI, Django, and general Python projects
- **🌐 Cross-Project Configuration**: Deploy TDD Guard configuration to any target project
- **📋 Enhanced Project Selection**: Interactive project browser with virtual environment detection
- **⚙️ Haiku JSON Fix Module**: Auto-include JSON formatting fixes for Claude 3.5 Haiku model
- **🏗️ Installation Workflow**: Complete end-to-end installation from discovery to deployment

### Enhanced Multi-Project Features
- **Project Validation**: Comprehensive project compatibility checking
- **Virtual Environment Detection**: Support for .venv, venv, env, virtualenv structures
- **Target Path Persistence**: Save and restore target project selections
- **Installation Summary**: Detailed post-installation status and next steps
- **Cross-Project Isolation**: Each project maintains independent TDD Guard configuration

### Updated Documentation
- **README.md**: Complete rewrite for multi-project installer workflow
- **Usage Examples**: Project selection interface and installation flow
- **Troubleshooting Guide**: Multi-project installation issues and solutions
- **Project Compatibility**: Supported project types and requirements matrix
- **Directory Structure**: Installer vs target project file organization

### Files Enhanced for Multi-Project Support
- `install.py` - Complete multi-project installation workflow (Lines 84-376)
- `generated/.last-config.json` - Target project path persistence
- Target project `.claude/` - Cross-project Claude IDE integration
- `README.md` - Multi-project installer documentation

## [2.0.0] - 2024-01-XX

### Added
- **Claude IDE Integration**: Complete integration with Claude IDE's .claude directory system
- **Model Selection**: Support for Claude AI model selection (Haiku, Sonnet, Opus) with metadata-driven configuration
- **Hooks Configuration**: Automatic TDD Guard hooks setup in Claude IDE settings.local.json
- **Instructions Integration**: Copy generated instructions to Claude IDE custom instructions
- **Ignore Patterns Management**: Smart ignore pattern configuration with module-based removals
- **Enforcement Configuration**: Guard settings protection and file bypass blocking features
- **Configuration Persistence**: Enhanced .last-config.json with complete settings restoration
- **Consistent UI**: Standardized default option display using [*] and [ ] bracket notation throughout wizard
- **Comprehensive Test Suite**: 10 pytest tests covering all core functionality with proper mocking
- **Enhanced Help Documentation**: Complete --help option reflecting all new features

### Enhanced
- **Wizard Flow**: Streamlined 6-step interactive process with intelligent defaults
- **Module System**: Metadata-driven module loading with priority-based ordering
- **Error Handling**: Robust error handling with graceful fallbacks for all IDE operations
- **File Validation**: Enhanced validation with tolerance-based line count checking
- **CLI Interface**: Improved argument parsing with comprehensive help text

### Technical Improvements
- **Architecture**: Modular design with separated concerns for IDE integration
- **Dependencies**: Minimal requirements.txt focused on testing framework
- **Code Quality**: Full compliance with TDD Guard rules and best practices
- **Documentation**: Comprehensive inline documentation and examples

### Files Added
- `requirements.txt` - Project dependencies specification
- `tests/test_generate.py` - Comprehensive test suite (10 tests)
- `modules/models.yaml` - Claude model configurations
- `docs/CHANGELOG.md` - Project change documentation

### Files Enhanced
- `install.py` - Complete rewrite with Claude IDE integration
- `generated/.last-config.json` - Extended configuration persistence
- `.claude/settings.local.json` - TDD Guard hooks and enforcement
- `README.md` - Updated with comprehensive usage documentation

## [1.0.0] - 2024-01-XX

### Added
- **Initial Release**: Basic TDD Guard Configuration Wizard
- **Module Discovery**: Auto-discovery of TDD modules with metadata parsing
- **Interactive Wizard**: Command-line interface for module selection
- **File Generation**: Combined instructions.md and tests.md generation
- **CLI Support**: Command-line arguments for non-interactive usage
- **Basic Validation**: Line count estimation and validation

### Core Features
- Module selection with priority ordering
- Instruction and test scenario generation
- Basic configuration saving
- CLI modes: wizard, --all, specific modules, --list

### Initial Architecture
- `tools/generate.py` - Core wizard implementation
- `modules/` - TDD module definitions with metadata.yaml
- `generated/` - Output directory for generated files

---

**Legend:**
- **Added**: New features and capabilities
- **Enhanced**: Improvements to existing functionality
- **Technical Improvements**: Code quality and architecture changes
- **Files Added/Enhanced**: Specific file-level changes