# Changelog

All notable changes to the TDD Guard Configuration Wizard project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- `tools/generate.py` - Complete rewrite with Claude IDE integration
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