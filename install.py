#!/usr/bin/env python3
"""
TDD Guard Configuration Wizard

Interactive wizard for generating custom TDD Guard instructions with full Claude IDE integration.

Features:
    • Module Selection: Choose from 10 TDD modules with smart defaults
    • Model Configuration: Select Claude AI model (Haiku, Sonnet, Opus)
    • Auto-Module Inclusion: Haiku model automatically includes JSON formatting fixes
    • Claude IDE Integration: Automatic hooks, instructions, and ignore patterns setup
    • Enforcement Configuration: Guard settings protection and file bypass blocking
    • Configuration Persistence: Save/restore all settings with one click

Usage:
    python install.py                               # Interactive wizard (default)
    python install.py --all                         # Include all modules (CLI mode)
    python install.py core pytest                   # Specific modules only (CLI mode)
    python install.py --list                        # List available modules

Interactive Wizard Flow:
    1. Load Previous Configuration? [Y/n]           # Restore all saved settings
    2. Module Selection (ordered by priority)       # Choose TDD rules to include
    3. Model Selection (3 Claude models)            # Pick AI model for TDD Guard
    4. Claude IDE Integration (3 options)           # Setup hooks, instructions, patterns
    5. Enforcement Configuration (2 security modes) # Configure access protection
    6. Generate Test Scenarios? [Y/n]              # Include test examples

Generated Files:
    • generated/instructions.md                     # TDD Guard rules for Claude
    • generated/tests.md                           # Test scenarios (optional)
    • .claude/settings.local.json                 # Claude IDE configuration
    • .claude/tdd-guard/data/instructions.md      # IDE custom instructions
    • .claude/tdd-guard/data/config.json          # IDE ignore patterns
    • generated/.last-config.json                 # Configuration persistence

The wizard provides comprehensive TDD Guard setup with Claude IDE integration,
security enforcement, and complete configuration management.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional

def simple_yaml_load(content: str) -> Dict:
    """Simple YAML parser for basic key: value pairs"""
    result = {}
    for line in content.strip().split('\n'):
        line = line.strip()
        if line and ':' in line and not line.startswith('#'):
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            # Convert boolean strings
            if value.lower() in ['yes', 'true']:
                value = True
            elif value.lower() in ['no', 'false']:
                value = False
            # Convert numbers
            elif value.isdigit():
                value = int(value)
            result[key] = value
    return result

class ModuleInfo:
    def __init__(self, name: str, path: Path, silent: bool = False):
        self.name = name
        self.path = path
        self.metadata = {}
        self.line_count = 0
        self.valid = False
        self.silent = silent
        self.load_metadata()
        self.calculate_lines()

    def load_metadata(self):
        """Load metadata.yaml for this module"""
        metadata_path = self.path / 'metadata.yaml'
        if metadata_path.exists():
            try:
                with open(metadata_path, 'r') as f:
                    self.metadata = simple_yaml_load(f.read())
                self.valid = True
            except Exception as e:
                if not self.silent:
                    print(f"Warning: Failed to load metadata for {self.name}: {e}")
        else:
            if not self.silent:
                print(f"Warning: Skipping {self.name} - missing metadata.yaml")

    def calculate_lines(self):
        """Calculate estimated line count for this module"""
        instructions_path = self.path / 'instructions.md'
        if instructions_path.exists():
            try:
                with open(instructions_path, 'r') as f:
                    # Skip title and priority level lines, count actual content
                    lines = f.readlines()
                    content_lines = [l for l in lines if not (l.startswith('#') and 'Priority Level:' in l)]
                    self.line_count = len([l for l in content_lines if l.strip()])
            except Exception:
                self.line_count = 0

    @property
    def display_name(self):
        return self.metadata.get('name', self.name.title())

    @property
    def description(self):
        return self.metadata.get('description', 'No description available')

    @property
    def default_enabled(self):
        default_val = self.metadata.get('default', 'no')
        if isinstance(default_val, bool):
            return default_val
        return str(default_val).lower() in ['yes', 'y', 'true']

    @property
    def priority(self):
        return self.metadata.get('priority', 999)

    @property
    def remove_from_ignore(self):
        return self.metadata.get('remove_from_ignore', [])

    @property
    def auto_include_with_model(self):
        return self.metadata.get('auto_include_with_model', None)

    @property
    def mandatory_for_model(self):
        return self.metadata.get('mandatory_for_model', False)

def discover_modules(silent: bool = False) -> List[ModuleInfo]:
    """Auto-discover all modules in the modules directory"""
    modules_dir = Path(__file__).parent / 'modules'
    if not modules_dir.exists():
        if not silent:
            print("Error: modules directory not found")
        sys.exit(1)

    modules = []
    for module_dir in modules_dir.iterdir():
        if module_dir.is_dir():
            module = ModuleInfo(module_dir.name, module_dir, silent=silent)
            if module.valid:
                modules.append(module)

    # Sort by priority (lower numbers first)
    modules.sort(key=lambda m: m.priority)
    return modules

def load_models() -> List[Dict]:
    """Load available models from modules/models.yaml"""
    models_path = Path(__file__).parent / 'modules' / 'models.yaml'
    if not models_path.exists():
        print("Warning: models.yaml not found. Using default model.")
        return [{"id": "claude-3-5-haiku-20241022", "name": "Claude 3.5 Haiku", "description": "Default model", "default": True}]

    try:
        with open(models_path, 'r') as f:
            content = f.read()

        # Simple YAML parsing for models
        models = []
        current_model = {}

        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('- id:'):
                if current_model:
                    models.append(current_model)
                current_model = {'id': line.split(':', 1)[1].strip().strip('"')}
            elif line.startswith('name:') and current_model:
                current_model['name'] = line.split(':', 1)[1].strip().strip('"')
            elif line.startswith('description:') and current_model:
                current_model['description'] = line.split(':', 1)[1].strip().strip('"')
            elif line.startswith('default:') and current_model:
                default_val = line.split(':', 1)[1].strip().lower()
                current_model['default'] = default_val in ['true', 'yes']

        if current_model:
            models.append(current_model)

        return models if models else [{"id": "claude-3-5-haiku-20241022", "name": "Claude 3.5 Haiku", "description": "Default model", "default": True}]

    except Exception as e:
        print(f"Warning: Failed to load models.yaml: {e}")
        return [{"id": "claude-3-5-haiku-20241022", "name": "Claude 3.5 Haiku", "description": "Default model", "default": True}]

def load_last_config() -> Optional[Dict]:
    """Load the last configuration from generated/.last-config.json"""
    config_path = Path(__file__).parent.parent / 'generated' / '.last-config.json'
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return None

def save_config(selected_modules: List[str], generate_tests: bool, ide_config: Dict):
    """Save configuration to generated/.last-config.json"""
    config_path = Path(__file__).parent.parent / 'generated' / '.last-config.json'
    config_path.parent.mkdir(exist_ok=True)

    config = {
        'selected_modules': selected_modules,
        'generate_tests': generate_tests,
        'model_id': ide_config.get('model_id'),
        'enable_hooks': ide_config.get('enable_hooks', False),
        'copy_instructions': ide_config.get('copy_instructions', False),
        'configure_ignore_patterns': ide_config.get('configure_ignore_patterns', False),
        'protect_guard_settings': ide_config.get('protect_guard_settings', True),
        'block_file_bypass': ide_config.get('block_file_bypass', False)
    }

    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception:
        pass  # Silent fail for config saving

def ask_yes_no(prompt: str, default: bool = True) -> bool:
    """Ask a yes/no question with a default"""
    if default:
        suffix = "[*] Yes  [ ] No"
    else:
        suffix = "[ ] Yes  [*] No"
    while True:
        response = input(f"{prompt} {suffix} (y/n): ").strip().lower()
        if not response:
            return default
        if response in ['y', 'yes']:
            return True
        if response in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'")

def update_model_setting(model_id: str) -> bool:
    """Update the TDD_GUARD_MODEL_VERSION in .claude/settings.local.json"""
    settings_path = Path(__file__).parent.parent / '.claude' / 'settings.local.json'

    try:
        # Create .claude directory if it doesn't exist
        settings_path.parent.mkdir(exist_ok=True)

        # Load existing settings or create default structure
        if settings_path.exists():
            with open(settings_path, 'r') as f:
                settings = json.load(f)
        else:
            settings = {"permissions": {"allow": [], "deny": [], "ask": []}, "env": {}}

        # Ensure env section exists
        if 'env' not in settings:
            settings['env'] = {}

        # Update model version
        settings['env']['TDD_GUARD_MODEL_VERSION'] = model_id

        # Write back to file
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=2)

        return True

    except Exception as e:
        print(f"Warning: Failed to update model setting: {e}")
        return False

def create_hooks(enabled: bool) -> bool:
    """Add TDD Guard hooks to .claude/settings.local.json"""
    if not enabled:
        return True

    settings_path = Path(__file__).parent.parent / '.claude' / 'settings.local.json'

    try:
        # Create .claude directory if it doesn't exist
        settings_path.parent.mkdir(exist_ok=True)

        # Load existing settings or create default structure
        if settings_path.exists():
            with open(settings_path, 'r') as f:
                settings = json.load(f)
        else:
            settings = {"permissions": {"allow": [], "deny": [], "ask": []}, "env": {}}

        # Add hooks section
        hooks_config = {
            "PreToolUse": [
                {
                    "matcher": "Write|Edit|MultiEdit|TodoWrite",
                    "hooks": [{"type": "command", "command": "tdd-guard"}]
                }
            ],
            "UserPromptSubmit": [
                {
                    "hooks": [{"type": "command", "command": "tdd-guard"}]
                }
            ],
            "SessionStart": [
                {
                    "matcher": "startup|resume|clear",
                    "hooks": [{"type": "command", "command": "tdd-guard"}]
                }
            ]
        }

        settings['hooks'] = hooks_config

        # Write back to file
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=2)

        return True

    except Exception as e:
        print(f"Warning: Failed to create hooks: {e}")
        return False

def copy_instructions_to_ide(enabled: bool, instructions_content: str) -> bool:
    """Copy generated instructions to .claude/tdd-guard/data/instructions.md"""
    if not enabled:
        return True

    instructions_path = Path(__file__).parent.parent / '.claude' / 'tdd-guard' / 'data' / 'instructions.md'

    try:
        # Create directory structure
        instructions_path.parent.mkdir(parents=True, exist_ok=True)

        # Write instructions file
        with open(instructions_path, 'w') as f:
            f.write(instructions_content)

        return True

    except Exception as e:
        print(f"Warning: Failed to copy instructions to IDE: {e}")
        return False

def configure_ignore_patterns(enabled: bool, selected_modules: List[ModuleInfo]) -> bool:
    """Configure ignore patterns in .claude/tdd-guard/data/config.json"""
    if not enabled:
        return True

    config_path = Path(__file__).parent.parent / '.claude' / 'tdd-guard' / 'data' / 'config.json'

    try:
        # Create directory structure
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing config or use defaults
        default_ignore_patterns = [
            "*.log", "**/*.json", "**/*.yml", "**/*.yaml",
            "**/*.xml", "**/*.html", "**/*.css", "**/*.rst",
            "*.md", "*.txt"
        ]

        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
                current_ignore_patterns = config.get('ignorePatterns', default_ignore_patterns)
        else:
            config = {"guardEnabled": False}
            current_ignore_patterns = default_ignore_patterns.copy()

        # Remove patterns from selected modules that want to validate those file types
        patterns_to_remove = set()
        for module in selected_modules:
            patterns_to_remove.update(module.remove_from_ignore)

        # Filter out patterns that modules want to remove
        updated_patterns = [p for p in current_ignore_patterns if p not in patterns_to_remove]

        # Update config
        config['guardEnabled'] = True
        config['ignorePatterns'] = updated_patterns

        # Write back to file
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        return True

    except Exception as e:
        print(f"Warning: Failed to configure ignore patterns: {e}")
        return False

def configure_enforcement(protect_settings: bool, block_bypass: bool) -> bool:
    """Configure TDD Guard enforcement in .claude/settings.local.json"""
    if not protect_settings and not block_bypass:
        return True

    settings_path = Path(__file__).parent.parent / '.claude' / 'settings.local.json'

    try:
        # Create .claude directory if it doesn't exist
        settings_path.parent.mkdir(exist_ok=True)

        # Load existing settings or create default structure
        if settings_path.exists():
            with open(settings_path, 'r') as f:
                settings = json.load(f)
        else:
            settings = {"permissions": {"allow": [], "deny": [], "ask": []}, "env": {}}

        # Ensure permissions structure exists
        if 'permissions' not in settings:
            settings['permissions'] = {"allow": [], "deny": [], "ask": []}
        if 'deny' not in settings['permissions']:
            settings['permissions']['deny'] = []

        deny_patterns = []

        if protect_settings:
            deny_patterns.append("Read(.claude/tdd-guard/**)")

        if block_bypass:
            deny_patterns.extend([
                "Bash(echo:*)",
                "Bash(printf:*)",
                "Bash(sed:*)",
                "Bash(awk:*)",
                "Bash(perl:*)"
            ])

        # Merge with existing deny patterns (avoid duplicates)
        existing_deny = set(settings['permissions']['deny'])
        all_deny = list(existing_deny.union(set(deny_patterns)))
        settings['permissions']['deny'] = all_deny

        # Write back to file
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=2)

        return True

    except Exception as e:
        print(f"Warning: Failed to configure enforcement: {e}")
        return False

def validate_generated_file(file_path: Path, estimated_lines: int, file_type: str = "instructions") -> bool:
    """Validate that generated file matches estimated line count"""
    if not file_path.exists():
        print(f"VALIDATION FAILED: {file_type} file not found at {file_path}")
        return False

    try:
        with open(file_path, 'r') as f:
            actual_lines = len([line for line in f if line.strip()])  # Count non-empty lines

        # Allow for some variance (±15% is reasonable)
        tolerance = max(10, int(estimated_lines * 0.15))  # At least 10 lines tolerance
        lower_bound = estimated_lines - tolerance
        upper_bound = estimated_lines + tolerance

        if lower_bound <= actual_lines <= upper_bound:
            print(f"VALIDATION PASSED: {file_type} file ({actual_lines} lines, estimated {estimated_lines})")
            return True
        else:
            variance = abs(actual_lines - estimated_lines)
            percentage = (variance / estimated_lines) * 100 if estimated_lines > 0 else 0
            print(f"VALIDATION WARNING: {file_type} file line count mismatch")
            print(f"   Expected: ~{estimated_lines} lines (±{tolerance})")
            print(f"   Actual: {actual_lines} lines")
            print(f"   Variance: {variance} lines ({percentage:.1f}%)")

            if percentage > 50:  # Major variance
                print(f"   This is a significant variance - please check module line calculations")
                return False
            else:
                print(f"   This variance is within acceptable range for content generation")
                return True

    except Exception as e:
        print(f"VALIDATION ERROR: Could not validate {file_type} file: {e}")
        return False

def run_wizard(modules: List[ModuleInfo]) -> Tuple[List[str], bool, int, Dict]:
    """Run the interactive module selection wizard with Claude IDE integration"""
    print("TDD Guard Configuration Wizard")
    print("=" * 50)
    print()

    selected_modules = []
    total_lines = 0
    ide_config = {
        'model_id': None,
        'enable_hooks': False,
        'copy_instructions': False,
        'configure_ignore_patterns': False,
        'protect_guard_settings': True,
        'block_file_bypass': False
    }

    # Ask about loading previous config
    last_config = load_last_config()
    if last_config:
        if ask_yes_no("Load previous configuration?", True):
            # Load ALL settings from config
            selected_module_names = last_config['selected_modules']
            generate_tests = last_config.get('generate_tests', True)
            loaded_ide_config = {
                'model_id': last_config.get('model_id'),
                'enable_hooks': last_config.get('enable_hooks', False),
                'copy_instructions': last_config.get('copy_instructions', False),
                'configure_ignore_patterns': last_config.get('configure_ignore_patterns', False),
                'protect_guard_settings': last_config.get('protect_guard_settings', True),
                'block_file_bypass': last_config.get('block_file_bypass', False)
            }
            # Skip all wizard questions, return loaded config
            estimated_lines = sum(m.line_count for m in modules if m.name in selected_module_names)
            return selected_module_names, generate_tests, estimated_lines, loaded_ide_config

    print("Module Selection (ordered by priority):")
    print("-" * 40)

    for module in modules:
        # Display module info
        status_char = "*" if module.default_enabled else " "
        print(f"[{status_char}] {module.display_name} (+{module.line_count} lines)")
        print(f"    {module.description}")

        # Ask for selection
        if ask_yes_no("Include this module?", module.default_enabled):
            selected_modules.append(module.name)
            total_lines += module.line_count
            print(f"    Selected (Running total: {total_lines}/300 lines)")

            # Warn if approaching limit
            if total_lines > 300:
                print(f"    WARNING: Exceeds 300-line limit! Current: {total_lines} lines")
        else:
            print(f"    Skipped (Running total: {total_lines}/300 lines)")
        print()

    # Model Selection
    print("Model Selection:")
    print("-" * 40)
    models = load_models()
    for i, model in enumerate(models, 1):
        default_marker = " [*]" if model.get('default', False) else " [ ]"
        print(f"  {i}.{default_marker} {model['name']} ({model['description']})")

    default_model = next((m for m in models if m.get('default')), models[0])
    while True:
        try:
            choice = input(f"Select model [1-{len(models)}] (press Enter for default): ").strip()
            if not choice:
                # Use default model
                selected_model = default_model
                break
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(models):
                selected_model = models[choice_idx]
                break
            print(f"Please enter a number between 1 and {len(models)}")
        except ValueError:
            print(f"Please enter a number between 1 and {len(models)}")

    ide_config['model_id'] = selected_model['id']
    print(f"Selected: {selected_model['name']}")

    # Auto-include model-specific modules
    for module in modules:
        if (module.auto_include_with_model == selected_model['id'] and
            module.name not in selected_modules):
            selected_modules.append(module.name)
            total_lines += module.line_count
            if module.mandatory_for_model:
                print(f"✓ Auto-included mandatory module: {module.display_name} (+{module.line_count} lines)")
            else:
                print(f"✓ Auto-included recommended module: {module.display_name} (+{module.line_count} lines)")
    print()

    # Claude IDE Integration
    print("Claude IDE Integration:")
    print("-" * 40)
    ide_config['enable_hooks'] = ask_yes_no("Enable TDD Guard hooks in Claude IDE?", True)
    ide_config['copy_instructions'] = ask_yes_no("Copy instructions to Claude IDE custom instructions?", True)
    ide_config['configure_ignore_patterns'] = ask_yes_no("Configure ignore patterns for Claude IDE?", True)
    print()

    # Enforcement Configuration
    print("Enforcement Configuration:")
    print("-" * 40)
    ide_config['protect_guard_settings'] = ask_yes_no("Enable Guard Settings Protection? (Prevents agents from reading TDD Guard config)", True)
    ide_config['block_file_bypass'] = ask_yes_no("Block File Operation Bypass? (Prevents shell commands that bypass TDD validation)", False)
    print()

    # Ask about test generation
    generate_tests = ask_yes_no("Generate test scenarios?", True)

    return selected_modules, generate_tests, total_lines, ide_config

def load_module_content(module_name: str) -> Tuple[str, str]:
    """Load instruction and test content for a module."""
    modules_dir = Path(__file__).parent / 'modules'
    module_dir = modules_dir / module_name

    instructions_path = module_dir / 'instructions.md'
    tests_path = module_dir / 'test-scenarios.md'

    instructions = ""
    tests = ""

    if instructions_path.exists():
        instructions = instructions_path.read_text()

    if tests_path.exists():
        tests = tests_path.read_text()

    return instructions, tests

def generate_combined_instructions(modules: List[str]) -> Tuple[str, str]:
    """Generate combined instructions from selected modules."""

    # Get module info for sorting (silent to avoid duplicate warnings)
    all_modules = {m.name: m for m in discover_modules(silent=True)}

    # Sort selected modules by priority
    sorted_modules = sorted(modules, key=lambda m: all_modules.get(m, ModuleInfo(m, Path(), silent=True)).priority)

    instructions_parts = []
    test_parts = []

    # Clean header for LLM consumption
    instructions_parts.append("# TDD Guard Rules")
    instructions_parts.append("")

    test_parts.append("# TDD Guard Test Scenarios")
    test_parts.append("")

    # Load and combine module content
    for module in sorted_modules:
        instructions, tests = load_module_content(module)

        if instructions:
            # Skip the module title line and priority level - just get the content
            content_lines = instructions.split('\n')

            # Find where actual content starts (skip title and priority level)
            content_start = 0
            for i, line in enumerate(content_lines):
                if line.startswith('## ') and not line.startswith('## Priority Level:'):
                    content_start = i
                    break

            # Add the actual instruction content without module headers
            if content_start > 0:
                instructions_parts.extend(content_lines[content_start:])
                instructions_parts.append("")

        if tests:
            # Skip the module title line - just get the content
            content_lines = tests.split('\n')

            # Find where actual content starts (skip title)
            content_start = 0
            for i, line in enumerate(content_lines):
                if line.startswith('## Phase') or line.startswith('### Test'):
                    content_start = i
                    break

            # Add the actual test content without module headers
            if content_start > 0:
                test_parts.extend(content_lines[content_start:])
                test_parts.append("")

    return '\n'.join(instructions_parts), '\n'.join(test_parts)

def main():
    parser = argparse.ArgumentParser(
        description='TDD Guard Configuration Wizard - Interactive setup for TDD Guard with Claude IDE integration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        'modules',
        nargs='*',
        help='Module names to include (e.g., core pytest flask). If none provided, runs wizard.'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List available modules'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Include all available modules'
    )

    args = parser.parse_args()

    # Discover available modules
    available_modules = discover_modules()

    if not available_modules:
        print("Error: No valid modules found. Check modules/ directory and metadata files.")
        sys.exit(1)

    if args.list:
        print("Available modules:")
        for module in available_modules:
            status = "default: yes" if module.default_enabled else "default: no"
            print(f"  {module.name:<20} (priority: {module.priority}, {status})")
            print(f"    {module.description}")
        return

    # Determine module selection method
    estimated_lines = 0
    ide_config = {
        'model_id': None,
        'enable_hooks': False,
        'copy_instructions': False,
        'configure_ignore_patterns': False,
        'protect_guard_settings': True,
        'block_file_bypass': False
    }

    if args.all:
        selected_modules = [m.name for m in available_modules]
        generate_tests = True
        estimated_lines = sum(m.line_count for m in available_modules)
    elif args.modules:
        selected_modules = args.modules
        generate_tests = True
        # Validate module names
        available_names = [m.name for m in available_modules]
        invalid_modules = [m for m in selected_modules if m not in available_names]
        if invalid_modules:
            print(f"Error: Unknown modules: {', '.join(invalid_modules)}")
            print(f"Available modules: {', '.join(available_names)}")
            sys.exit(1)
        # Calculate estimated lines for CLI selection
        estimated_lines = sum(m.line_count for m in available_modules if m.name in selected_modules)
    else:
        # Run wizard (default behavior)
        selected_modules, generate_tests, estimated_lines, ide_config = run_wizard(available_modules)

    # Generate combined content
    instructions, tests = generate_combined_instructions(selected_modules)

    # Check line count and warn if over 300 lines
    instruction_lines = instructions.count('\n') + 1
    if instruction_lines > 300:
        print()
        print(f"WARNING: Generated instructions are {instruction_lines} lines (exceeds 300-line limit)")
        print("         Quality may degrade with instructions over 300 lines.")
        print()

    # Write output files
    output_dir = Path(__file__).parent.parent

    # Ensure generated directory exists
    generated_dir = output_dir / 'generated'
    generated_dir.mkdir(exist_ok=True)

    # Write instructions
    instructions_file = generated_dir / 'instructions.md'
    with open(instructions_file, 'w') as f:
        f.write(instructions)

    # Write tests if requested
    if generate_tests:
        tests_file = generated_dir / 'tests.md'
        with open(tests_file, 'w') as f:
            f.write(tests)

    # Save configuration for next time
    save_config(selected_modules, generate_tests, ide_config)

    # Claude IDE Integration
    ide_results = {}
    if ide_config['model_id']:
        ide_results['model'] = update_model_setting(ide_config['model_id'])

    ide_results['hooks'] = create_hooks(ide_config['enable_hooks'])
    ide_results['instructions'] = copy_instructions_to_ide(ide_config['copy_instructions'], instructions)

    # Get selected module objects for ignore patterns
    selected_module_objects = [m for m in available_modules if m.name in selected_modules]
    ide_results['ignore_patterns'] = configure_ignore_patterns(ide_config['configure_ignore_patterns'], selected_module_objects)

    # Enforcement Configuration
    ide_results['enforcement'] = configure_enforcement(ide_config['protect_guard_settings'], ide_config['block_file_bypass'])

    # Validate generated files and report results
    print()
    print("Generation Complete:")
    print("-" * 20)

    # Validate instructions file
    instructions_valid = validate_generated_file(
        instructions_file,
        estimated_lines,
        "instructions"
    )

    # Validate tests file if generated
    tests_valid = True
    if generate_tests:
        # For tests, we don't have a good estimate, so we do a basic existence check
        tests_file = generated_dir / 'tests.md'
        test_lines = tests.count('\n') + 1
        if tests_file.exists():
            print(f"VALIDATION PASSED: tests file ({test_lines} lines)")
        else:
            print(f"VALIDATION FAILED: tests file not found")
            tests_valid = False

    print()
    print(f"Instructions: {instructions_file} ({instruction_lines} lines)")
    if generate_tests:
        test_lines = tests.count('\n') + 1
        print(f"Tests: {generated_dir / 'tests.md'} ({test_lines} lines)")

    # Claude IDE Integration Results
    if ide_config['model_id']:
        model_status = "Updated in Claude IDE" if ide_results.get('model') else "Failed to update"
        print(f"Model: {ide_config['model_id']} → {model_status}")

    if ide_config['enable_hooks']:
        hooks_status = "Enabled in Claude IDE settings" if ide_results.get('hooks') else "Failed to enable"
        print(f"Hooks: {hooks_status}")

    if ide_config['copy_instructions']:
        instructions_status = "Copied to Claude IDE custom instructions" if ide_results.get('instructions') else "Failed to copy"
        print(f"Instructions: {instructions_status}")

    if ide_config['configure_ignore_patterns']:
        patterns_status = "Configured in Claude IDE" if ide_results.get('ignore_patterns') else "Failed to configure"
        # Count removed patterns
        removed_patterns = set()
        for module in selected_module_objects:
            removed_patterns.update(module.remove_from_ignore)
        if removed_patterns:
            removed_list = ', '.join(sorted(removed_patterns))
            print(f"Ignore patterns: Removed {removed_list} (TDD Guard will now validate these files)")
        else:
            print(f"Ignore patterns: {patterns_status}")

    # Enforcement Configuration Results
    if ide_config['protect_guard_settings'] or ide_config['block_file_bypass']:
        enforcement_status = "Configured in Claude IDE" if ide_results.get('enforcement') else "Failed to configure"
        enforcement_details = []
        if ide_config['protect_guard_settings']:
            enforcement_details.append("Guard settings protected")
        if ide_config['block_file_bypass']:
            enforcement_details.append("File bypass blocked")
        if not ide_config['block_file_bypass'] and ide_config['protect_guard_settings']:
            enforcement_details.append("File bypass not blocked")

        enforcement_summary = ', '.join(enforcement_details)
        print(f"Enforcement: {enforcement_summary}")

    print(f"Modules included: {', '.join(selected_modules)}")
    print(f"Total modules: {len(selected_modules)}")

    # Final validation summary
    if instructions_valid and tests_valid:
        print(f"All validations passed!")
    else:
        print(f"Some validations failed - please review the generated files")

if __name__ == '__main__':
    main()