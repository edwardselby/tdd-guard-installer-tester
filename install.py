#!/usr/bin/env python3
"""
TDD Guard Configuration Wizard - Multi-Project Installation

Interactive wizard for installing TDD Guard into any Python project with full Claude IDE integration.

Features:
    • Multi-Project Support: Auto-discover and select target projects in parent directory
    • Package Installation: Automatically installs tdd-guard-pytest in target project
    • Module Selection: Choose from 10 TDD modules with smart defaults
    • Model Configuration: Select Claude AI model (Haiku, Sonnet, Opus)
    • Auto-Module Inclusion: Haiku model automatically includes JSON formatting fixes
    • Claude IDE Integration: Automatic hooks, instructions, and ignore patterns setup
    • Enforcement Configuration: Guard settings protection and file bypass blocking
    • Configuration Persistence: Save/restore all settings with one click

Multi-Project Installation:
    1. Clone TDD-guard-test into your projects directory
    2. Run the wizard: python install.py
    3. Select target project from auto-discovered list
    4. Wizard installs TDD Guard configuration to selected project

Directory Structure Example:
    projects/
    ├── feed_orchestrator_v2/    ← Target project (will be configured)
    ├── api_gateway/             ← Another project
    └── TDD-guard-test/          ← Installer location (run from here)

Usage:
    python install.py                               # Interactive wizard with project selection
    python install.py --all                         # Include all modules (CLI mode, no project selection)
    python install.py core pytest                   # Specific modules (CLI mode, no project selection)
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
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from rich.console import Console
from rich.prompt import Confirm

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

# ============================================================================
# Rich Console Infrastructure
# ============================================================================

_console = None

def get_console() -> Console:
    """Get or create Rich console instance"""
    global _console
    if _console is None:
        _console = Console()
    return _console

def print_step_header(title: str, step: int, total: int):
    """Print a Rich Panel showing step progress"""
    from rich.panel import Panel
    console = get_console()
    header_text = f"Step {step}/{total}: {title}"
    panel = Panel(header_text, style="bold cyan")
    console.print(panel)

def print_modules_table(modules: List):
    """Print a Rich Table displaying modules"""
    from rich.table import Table
    console = get_console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Module", style="cyan")
    table.add_column("Lines", justify="right", style="green")
    table.add_column("Description")

    for i, module in enumerate(modules, 1):
        table.add_row(
            str(i),
            module.display_name,
            str(module.line_count),
            module.description
        )

    console.print(table)

def parse_module_selection(selection: str, max_count: int) -> List[int]:
    """Parse user module selection string into list of indices"""
    indices = []
    parts = selection.split()

    for part in parts:
        part_lower = part.lower()

        # Handle shortcuts
        if part_lower == 'all':
            return list(range(max_count))
        elif part_lower in ['rec', 'recommended']:
            # Will be handled by caller with module default_enabled flags
            continue
        elif part_lower == 'none':
            return []
        elif '-' in part:
            # Handle ranges like "1-5"
            try:
                start, end = part.split('-')
                start_num = int(start)
                end_num = int(end)
                for num in range(start_num, end_num + 1):
                    if 1 <= num <= max_count and (num - 1) not in indices:
                        indices.append(num - 1)
            except ValueError:
                pass
        else:
            # Handle simple numbers
            try:
                num = int(part)
                if 1 <= num <= max_count and (num - 1) not in indices:
                    indices.append(num - 1)
            except ValueError:
                pass

    return indices

def select_wizard_mode() -> str:
    """Prompt user to select wizard mode"""
    from rich.prompt import Prompt
    from rich.panel import Panel

    console = get_console()

    modes_text = """[cyan]1.[/cyan] Express   - Quick setup with recommended defaults (~90 seconds faster)
[cyan]2.[/cyan] Custom    - Full control over all settings
[cyan]3.[/cyan] Minimal   - Bare minimum configuration"""

    panel = Panel(modes_text, title="Wizard Mode", style="bold magenta", width=80)
    console.print(panel)

    choice = Prompt.ask("Select mode", choices=["1", "2", "3"], default="1")

    mode_map = {"1": "express", "2": "custom", "3": "minimal"}
    return mode_map[choice]

def get_express_mode_config(modules: List, models: List[Dict]) -> Dict:
    """Get express mode configuration with recommended defaults"""
    selected_modules = [m.name for m in modules if m.default_enabled]
    default_model = next((m for m in models if m.get('default')), models[0] if models else None)
    model_id = default_model['id'] if default_model else None

    ide_config = {
        'model_id': model_id,
        'enable_hooks': True,
        'copy_instructions': True,
        'configure_ignore_patterns': True,
        'protect_guard_settings': True,
        'block_file_bypass': False,
        'auto_approve_pytest': True
    }

    return {
        'selected_modules': selected_modules,
        'model_id': model_id,
        'ide_config': ide_config,
        'generate_tests': True
    }

def select_model(models: List[Dict], step: int = 1, total: int = 5) -> Dict:
    """Select Claude AI model using Rich table"""
    from rich.table import Table
    from rich.prompt import Prompt

    console = get_console()

    print_step_header("Model Selection", step, total)

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Model", style="cyan")
    table.add_column("Description", style="dim")
    table.add_column("Default", justify="center", width=10)

    default_idx = 0
    for i, model in enumerate(models, 1):
        default_marker = "[green]✓[/green]" if model.get('default') else ""
        if model.get('default'):
            default_idx = i

        table.add_row(
            str(i),
            model['name'],
            model['description'],
            default_marker
        )

    console.print(table)
    console.print()

    choice = Prompt.ask(
        f"[cyan]Select model[/cyan]",
        choices=[str(i) for i in range(1, len(models) + 1)],
        default=str(default_idx) if default_idx else "1"
    )

    selected_model = models[int(choice) - 1]
    console.print(f"[green]✓[/green] Selected: [cyan]{selected_model['name']}[/cyan]")
    console.print()

    return selected_model

def select_from_exclusive_group(group_name: str, modules: List['ModuleInfo']) -> 'ModuleInfo':
    """Select one module from an exclusive group using Rich UI"""
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt

    console = get_console()

    # Display group header
    header = f"{group_name.upper()} - SELECT ONE"
    panel = Panel(header, style="bold yellow", width=80)
    console.print(panel)
    console.print()

    # Create table with radio button style
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Module", style="cyan")
    table.add_column("Description", style="dim")
    table.add_column("Lines", justify="right", width=10)
    table.add_column("Default", justify="center", width=10)

    default_idx = 0
    for i, module in enumerate(modules, 1):
        default_marker = "[green]●[/green]" if module.default_enabled else "[dim]○[/dim]"
        if module.default_enabled:
            default_idx = i

        table.add_row(
            str(i),
            module.display_name,
            module.description,
            f"+{module.line_count}",
            default_marker
        )

    console.print(table)
    console.print()

    choice = Prompt.ask(
        f"[cyan]Select option[/cyan]",
        choices=[str(i) for i in range(1, len(modules) + 1)],
        default=str(default_idx) if default_idx else "1"
    )

    selected_module = modules[int(choice) - 1]
    console.print(f"[green]✓[/green] Selected: [cyan]{selected_module.display_name}[/cyan]")
    console.print()

    return selected_module

def select_standalone_modules(modules: List['ModuleInfo']) -> List['ModuleInfo']:
    """Select multiple standalone modules using Rich UI (checkbox style)"""
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Confirm

    console = get_console()

    # Display header
    header = "Additional Modules (ordered by priority)"
    panel = Panel(header, style="bold cyan", width=80)
    console.print(panel)
    console.print()

    # Create table showing all modules
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Module", style="cyan")
    table.add_column("Description", style="dim")
    table.add_column("Lines", justify="right", width=10)
    table.add_column("Default", justify="center", width=10)

    for module in modules:
        default_marker = "[green]✓[/green]" if module.default_enabled else ""
        table.add_row(
            module.display_name,
            module.description,
            f"+{module.line_count}",
            default_marker
        )

    console.print(table)
    console.print()

    # Ask for each module individually (checkbox style)
    selected = []
    for module in modules:
        default_choice = module.default_enabled
        question = f"Include [cyan]{module.display_name}[/cyan]?"

        if Confirm.ask(question, default=default_choice):
            selected.append(module)
            console.print(f"  [green]✓[/green] Added: {module.display_name}")
        else:
            console.print(f"  [dim]○[/dim] Skipped: {module.display_name}")

    console.print()
    return selected

# ============================================================================
# Phase 1: Project Discovery & Detection Functions
# ============================================================================

def detect_project_type(project_path: Path) -> str:
    """Identify project framework type by analyzing dependencies"""
    requirements_path = project_path / 'requirements.txt'
    pyproject_path = project_path / 'pyproject.toml'

    dependencies = []

    if requirements_path.exists():
        try:
            with open(requirements_path, 'r') as f:
                dependencies = f.read().lower()
        except Exception:
            pass

    if pyproject_path.exists():
        try:
            with open(pyproject_path, 'r') as f:
                dependencies += f.read().lower()
        except Exception:
            pass

    if 'flask' in dependencies:
        return "Python - Flask"
    elif 'fastapi' in dependencies:
        return "Python - FastAPI"
    elif 'django' in dependencies:
        return "Python - Django"
    else:
        return "Python - General"

def find_virtual_environment(project_path: Path) -> Optional[Path]:
    """Locate virtual environment in project"""
    common_venv_names = ['.venv', 'venv', 'env', 'virtualenv']

    for venv_name in common_venv_names:
        venv_path = project_path / venv_name
        if venv_path.exists():
            python_path = venv_path / 'bin' / 'python'
            if python_path.exists():
                return python_path
            python_path_win = venv_path / 'Scripts' / 'python.exe'
            if python_path_win.exists():
                return python_path_win

    return None

def validate_project_path(project_path: Path) -> Tuple[bool, str]:
    """Validate that path is a suitable target project"""
    installer_dir = Path(__file__).parent

    if not project_path.exists():
        return False, f"Path does not exist: {project_path}"

    if not project_path.is_dir():
        return False, f"Path is not a directory: {project_path}"

    # Allow installation to this project itself for testing/fixing purposes
    # if project_path.resolve() == installer_dir.resolve():
    #     return False, "Cannot install to TDD-guard-test directory itself"

    project_indicators = [
        project_path / '.git',
        project_path / 'pyproject.toml',
        project_path / 'requirements.txt',
        project_path / 'package.json'
    ]

    if not any(indicator.exists() for indicator in project_indicators):
        return False, "No project indicators found (.git, pyproject.toml, requirements.txt, package.json)"

    try:
        test_file = project_path / '.tdd_guard_write_test'
        test_file.touch()
        test_file.unlink()
    except PermissionError:
        return False, f"No write permission for: {project_path}"
    except Exception as e:
        return False, f"Cannot write to path: {e}"

    return True, "Valid project path"

def discover_projects() -> List[Dict]:
    """Scan parent directory for compatible Python projects"""
    parent_dir = Path(__file__).parent.parent
    installer_dir = Path(__file__).parent

    projects = []

    # Add THIS PROJECT as index 0 for testing/fixing purposes
    try:
        project_type = detect_project_type(installer_dir)
        venv_python = find_virtual_environment(installer_dir)
        has_tdd_guard = (installer_dir / '.claude' / 'tdd-guard').exists()

        projects.append({
            'name': f"{installer_dir.name} (THIS PROJECT)",
            'path': installer_dir,
            'type': project_type,
            'venv': venv_python,
            'has_tdd_guard': has_tdd_guard
        })
    except Exception as e:
        print(f"Warning: Error scanning this project: {e}")

    # Scan parent directory for other projects
    try:
        for item in parent_dir.iterdir():
            if not item.is_dir():
                continue

            # Skip the installer directory (already added above as "THIS PROJECT")
            if item.resolve() == installer_dir.resolve():
                continue

            is_project = (
                (item / '.git').exists() or
                (item / 'pyproject.toml').exists() or
                (item / 'requirements.txt').exists()
            )

            if is_project:
                project_type = detect_project_type(item)
                venv_python = find_virtual_environment(item)

                has_tdd_guard = (item / '.claude' / 'tdd-guard').exists()

                projects.append({
                    'name': item.name,
                    'path': item,
                    'type': project_type,
                    'venv': venv_python,
                    'has_tdd_guard': has_tdd_guard
                })

    except Exception as e:
        print(f"Warning: Error scanning parent directory: {e}")

    # Sort other projects by name, but keep THIS PROJECT at index 0
    this_project = projects[0]  # THIS PROJECT
    other_projects = sorted(projects[1:], key=lambda p: p['name'])

    return [this_project] + other_projects

# ============================================================================
# Phase 2: Interactive Project Selection
# ============================================================================

def select_target_project() -> Optional[Path]:
    """Interactive project selection with auto-discovery using Rich UI"""
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt

    console = get_console()

    # Welcome header
    header_text = """[bold cyan]Target Project Selection[/bold cyan]
[dim]Select which project to install TDD Guard into[/dim]"""
    console.print(Panel(header_text, style="bold magenta", width=80))
    console.print()

    projects = discover_projects()

    if not projects:
        console.print("[yellow]⚠[/yellow]  No compatible projects found in parent directory.")
        console.print("[dim]Make sure you have cloned TDD-guard-test into your projects directory.[/dim]")
        console.print()

        if ask_yes_no("Would you like to specify a custom path?", False):
            custom_path = Prompt.ask("\n[cyan]Enter project path[/cyan]")
            project_path = Path(custom_path).expanduser().resolve()
            is_valid, message = validate_project_path(project_path)
            if is_valid:
                return project_path
            else:
                console.print(f"\n[red]✗[/red] Invalid path: {message}")
                return None
        return None

    console.print(f"[green]✓[/green] Discovered {len(projects)} compatible project(s)\n")

    # Create Rich table for projects
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Project Name", style="cyan")
    table.add_column("Type", style="yellow")
    table.add_column("Virtual Env", style="green")
    table.add_column("TDD Guard", style="blue")

    for i, project in enumerate(projects, 1):
        venv_status = "✓ Found" if project['venv'] else "✗ Not found"
        if project['venv']:
            venv_name = project['venv'].parent.parent.name
            venv_status += f" ({venv_name})"

        tdd_status = "⚠ Installed" if project['has_tdd_guard'] else "Not installed"

        table.add_row(
            str(i),
            project['name'],
            project['type'],
            venv_status,
            tdd_status
        )

    console.print(table)
    console.print(f"\n  {len(projects) + 1}. [yellow][Custom Path][/yellow] - Specify a different location")
    console.print()

    while True:
        try:
            choice = Prompt.ask(
                f"[cyan]Select target project[/cyan]",
                choices=[str(i) for i in range(1, len(projects) + 2)],
                default="1"
            )

            choice_num = int(choice)

            if choice_num == len(projects) + 1:
                custom_path = Prompt.ask("\n[cyan]Enter project path[/cyan]")
                project_path = Path(custom_path).expanduser().resolve()
                is_valid, message = validate_project_path(project_path)
                if is_valid:
                    return project_path
                else:
                    console.print(f"\n[red]✗[/red] Invalid path: {message}")
                    continue

            if 1 <= choice_num <= len(projects):
                selected = projects[choice_num - 1]
                console.print(f"\n[green]✓[/green] Selected: [cyan]{selected['name']}[/cyan]")
                console.print(f"  Path: {selected['path']}")
                console.print(f"  Type: {selected['type']}")

                if selected['has_tdd_guard']:
                    console.print("\n[yellow]⚠  Warning:[/yellow] This project already has TDD Guard installed.")
                    console.print("  Continuing will overwrite existing configuration.")

                if ask_yes_no("\nContinue with this project?", True):
                    console.print()
                    return selected['path']
                else:
                    console.print("\n[red]✗[/red] Installation cancelled.")
                    return None

        except KeyboardInterrupt:
            console.print("\n\n[red]✗[/red] Installation cancelled.")
            return None

# ============================================================================
# Phase 3: Package Installation
# ============================================================================

def install_tdd_guard_package(project_path: Path) -> bool:
    """Install tdd-guard-pytest in target project's environment"""
    print("\nInstalling TDD Guard package...")
    print("-" * 40)

    venv_python = find_virtual_environment(project_path)

    if not venv_python:
        print("⚠  Warning: No virtual environment detected in target project.")
        print(f"Searched for: .venv/, venv/, env/, virtualenv/")
        print("\nOptions:")
        print("  1. Install system-wide (not recommended)")
        print("  2. Cancel and create virtual environment first")

        choice = input("\nYour choice [1-2]: ").strip()

        if choice != '1':
            print("\n❌ Installation cancelled. Create a virtual environment and try again.")
            return False

        python_executable = sys.executable
    else:
        python_executable = str(venv_python)
        venv_name = venv_python.parent.parent.name
        print(f"✓ Using virtual environment: {venv_name}")

    try:
        print(f"Running: {python_executable} -m pip install tdd-guard-pytest")

        result = subprocess.run(
            [python_executable, '-m', 'pip', 'install', 'tdd-guard-pytest'],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print("✓ Successfully installed tdd-guard-pytest")
            return True
        else:
            print(f"❌ Installation failed:")
            print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("❌ Installation timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False

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

    @property
    def exclusive_group(self):
        return self.metadata.get('exclusive_group', None)

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
        return [{"id": "claude-sonnet-4-0", "name": "Claude Sonnet 4.0", "description": "Default model", "default": True}]

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

        return models if models else [{"id": "claude-sonnet-4-0", "name": "Claude Sonnet 4.0", "description": "Default model", "default": True}]

    except Exception as e:
        print(f"Warning: Failed to load models.yaml: {e}")
        return [{"id": "claude-sonnet-4-0", "name": "Claude Sonnet 4.0", "description": "Default model", "default": True}]

def load_last_config() -> Optional[Dict]:
    """Load the last configuration from generated/.last-config.json"""
    config_path = Path(__file__).parent / 'generated' / '.last-config.json'
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return None

def save_config(selected_modules: List[str], generate_tests: bool, ide_config: Dict, target_path: Optional[Path] = None):
    """Save configuration to generated/.last-config.json"""
    config_path = Path(__file__).parent / 'generated' / '.last-config.json'
    config_path.parent.mkdir(exist_ok=True)

    config = {
        'selected_modules': selected_modules,
        'generate_tests': generate_tests,
        'target_path': str(target_path) if target_path else None,
        'model_id': ide_config.get('model_id'),
        'enable_hooks': ide_config.get('enable_hooks', False),
        'copy_instructions': ide_config.get('copy_instructions', False),
        'configure_ignore_patterns': ide_config.get('configure_ignore_patterns', False),
        'protect_guard_settings': ide_config.get('protect_guard_settings', True),
        'block_file_bypass': ide_config.get('block_file_bypass', False),
        'auto_approve_pytest': ide_config.get('auto_approve_pytest', False)
    }

    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception:
        pass  # Silent fail for config saving

def ask_yes_no(prompt: str, default: bool = True) -> bool:
    """Ask a yes/no question with a default using Rich Confirm"""
    return Confirm.ask(prompt, default=default)

def update_model_setting(model_id: str, target_path: Path) -> bool:
    """Update the TDD_GUARD_MODEL_VERSION in .claude/settings.local.json"""
    settings_path = target_path / '.claude' / 'settings.local.json'

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

def create_hooks(enabled: bool, target_path: Path) -> bool:
    """Add TDD Guard hooks to .claude/settings.local.json"""
    if not enabled:
        return True

    settings_path = target_path / '.claude' / 'settings.local.json'

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

def copy_instructions_to_ide(enabled: bool, instructions_content: str, target_path: Path) -> bool:
    """Copy generated instructions to .claude/tdd-guard/data/instructions.md"""
    if not enabled:
        return True

    instructions_path = target_path / '.claude' / 'tdd-guard' / 'data' / 'instructions.md'

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

def configure_ignore_patterns(enabled: bool, selected_modules: List[ModuleInfo], target_path: Path) -> bool:
    """Configure ignore patterns in .claude/tdd-guard/data/config.json"""
    if not enabled:
        return True

    config_path = target_path / '.claude' / 'tdd-guard' / 'data' / 'config.json'

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

def configure_enforcement(protect_settings: bool, block_bypass: bool, target_path: Path) -> bool:
    """Configure TDD Guard enforcement in .claude/settings.local.json"""
    if not protect_settings and not block_bypass:
        return True

    settings_path = target_path / '.claude' / 'settings.local.json'

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

def configure_auto_approve_pytest(enabled: bool, target_path: Path) -> bool:
    """Add pytest patterns to permissions.allow in .claude/settings.local.json"""
    if not enabled:
        return True

    settings_path = target_path / '.claude' / 'settings.local.json'

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
        if 'allow' not in settings['permissions']:
            settings['permissions']['allow'] = []

        # Add pytest patterns if not already present
        pytest_patterns = [
            "Bash(FLASK_ENV=TESTING poetry run pytest:*)",
            "Bash(poetry run pytest:*)",
            "Bash(pytest:*)"
        ]

        for pattern in pytest_patterns:
            if pattern not in settings['permissions']['allow']:
                settings['permissions']['allow'].append(pattern)

        # Write back to file
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=2)

        return True

    except Exception as e:
        print(f"Warning: Failed to configure auto-approve for pytest: {e}")
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

def run_wizard(modules: List[ModuleInfo], project_type: Optional[str] = None, mode: Optional[str] = None) -> Tuple[List[str], bool, int, Dict]:
    """Run the interactive module selection wizard with Claude IDE integration"""
    from rich.panel import Panel

    console = get_console()

    # Welcome banner
    welcome_text = """[bold cyan]TDD Guard Configuration Wizard[/bold cyan]
[dim]Configure TDD Guard for your project with intelligent defaults[/dim]"""
    console.print(Panel(welcome_text, style="bold magenta", width=80))
    console.print()

    # Ask about loading previous config first
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
                'block_file_bypass': last_config.get('block_file_bypass', False),
                'auto_approve_pytest': last_config.get('auto_approve_pytest', False)
            }
            # Skip all wizard questions, return loaded config
            estimated_lines = sum(m.line_count for m in modules if m.name in selected_module_names)
            console.print("[green]✓ Configuration loaded[/green]")
            console.print()
            return selected_module_names, generate_tests, estimated_lines, loaded_ide_config

    # If mode not specified, prompt user to select
    if mode is None:
        mode = select_wizard_mode()
        console.print()

    # Handle express mode
    if mode == 'express':
        console.print("[cyan]Express mode:[/cyan] Using recommended defaults")
        console.print()
        models = load_models()
        config = get_express_mode_config(modules, models)
        estimated_lines = sum(m.line_count for m in modules if m.name in config['selected_modules'])
        console.print(f"[green]✓[/green] Selected {len(config['selected_modules'])} modules with recommended settings")
        console.print()
        return config['selected_modules'], config['generate_tests'], estimated_lines, config['ide_config']

    # Handle minimal mode
    if mode == 'minimal':
        console.print("[cyan]Minimal mode:[/cyan] Bare minimum configuration")
        console.print()
        # Just core module, default model, no extras
        models = load_models()
        default_model = next((m for m in models if m.get('default')), models[0] if models else None)

        selected_modules = ['core-strict']  # Just the core strict module
        ide_config = {
            'model_id': default_model['id'] if default_model else None,
            'enable_hooks': True,
            'copy_instructions': True,
            'configure_ignore_patterns': False,
            'protect_guard_settings': True,
            'block_file_bypass': False,
            'auto_approve_pytest': False
        }
        estimated_lines = sum(m.line_count for m in modules if m.name in selected_modules)
        console.print(f"[green]✓[/green] Configured with core TDD module only")
        console.print()
        return selected_modules, True, estimated_lines, ide_config

    # Custom mode - full wizard with Rich UI
    console.print("[cyan]Custom mode:[/cyan] Full control over all settings")
    console.print()

    selected_modules = []
    total_lines = 0
    ide_config = {
        'model_id': None,
        'enable_hooks': False,
        'copy_instructions': False,
        'configure_ignore_patterns': False,
        'protect_guard_settings': True,
        'block_file_bypass': False,
        'auto_approve_pytest': False
    }

    # Model Selection using Rich UI
    models = load_models()
    selected_model = select_model(models, step=1, total=5)
    ide_config['model_id'] = selected_model['id']

    # Auto-include model-specific modules BEFORE showing module selection
    model_specific_modules = []
    for module in modules:
        if (module.auto_include_with_model == selected_model['id']):
            model_specific_modules.append(module.name)
            selected_modules.append(module.name)
            total_lines += module.line_count
            if module.mandatory_for_model:
                print(f"✓ Auto-including mandatory module for {selected_model['name']}: {module.display_name}")
            else:
                print(f"✓ Auto-including recommended module for {selected_model['name']}: {module.display_name}")

    if model_specific_modules:
        print()

    # Module Selection (now AFTER model selection)
    # Separate modules into exclusive groups and standalone modules
    exclusive_groups = {}
    standalone_modules = []

    for module in modules:
        # Skip modules that were auto-included for the selected model
        if module.name in model_specific_modules:
            continue

        if module.exclusive_group:
            group_name = module.exclusive_group
            if group_name not in exclusive_groups:
                exclusive_groups[group_name] = []
            exclusive_groups[group_name].append(module)
        else:
            standalone_modules.append(module)

    # Handle exclusive groups first (radio selection with Rich UI)
    for group_name, group_modules in sorted(exclusive_groups.items()):
        selected = select_from_exclusive_group(group_name, group_modules)
        selected_modules.append(selected.name)
        total_lines += selected.line_count

    # Handle standalone modules (checkbox selection with Rich UI)
    if standalone_modules:
        selected_standalone = select_standalone_modules(standalone_modules)
        for module in selected_standalone:
            selected_modules.append(module.name)
            total_lines += module.line_count

    # Claude IDE Integration
    from rich.panel import Panel
    console = get_console()
    console.print(Panel("Claude IDE Integration", style="bold cyan", width=80))
    console.print()
    ide_config['enable_hooks'] = ask_yes_no("Enable TDD Guard hooks in Claude IDE?", True)
    ide_config['copy_instructions'] = ask_yes_no("Copy instructions to Claude IDE custom instructions?", True)
    ide_config['configure_ignore_patterns'] = ask_yes_no("Configure ignore patterns for Claude IDE?", True)
    console.print()

    # Enforcement Configuration
    console.print(Panel("Enforcement Configuration", style="bold cyan", width=80))
    console.print()
    ide_config['protect_guard_settings'] = ask_yes_no("Enable Guard Settings Protection? (Prevents agents from reading TDD Guard config)", True)
    ide_config['block_file_bypass'] = ask_yes_no("Block File Operation Bypass? (Prevents shell commands that bypass TDD validation)", False)
    console.print()

    # Auto-Approve Pytest (for any Python project with pytest module)
    if "pytest" in selected_modules:
        console.print(Panel("Test Automation", style="bold cyan", width=80))
        console.print()
        ide_config['auto_approve_pytest'] = ask_yes_no("Enable automatic approval for pytest commands?", True)
        console.print()

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

    # PHASE 5.1: Project Selection Step
    # Only do project selection for wizard mode (not CLI mode)
    target_path = None
    project_type = None
    if not args.list and not args.all and not args.modules:
        target_path = select_target_project()
        if not target_path:
            print()
            print("Installation cancelled. No target project selected.")
            sys.exit(0)

        # Detect project type for conditional features
        project_type = detect_project_type(target_path)

        # Install TDD Guard package
        package_installed = install_tdd_guard_package(target_path)
        if not package_installed:
            print()
            print("Warning: Failed to install tdd-guard-pytest package.")
            print("You may need to install it manually:")
            print("  cd ", target_path)
            print("  pip install tdd-guard-pytest")
            if not ask_yes_no("Continue anyway?", False):
                sys.exit(1)

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
        selected_modules, generate_tests, estimated_lines, ide_config = run_wizard(available_modules, project_type)

    # Generate combined content
    instructions, tests = generate_combined_instructions(selected_modules)

    # Check line count and warn if over 300 lines
    instruction_lines = instructions.count('\n') + 1
    if instruction_lines > 300:
        print()
        print(f"WARNING: Generated instructions are {instruction_lines} lines (exceeds 300-line limit)")
        print("         Quality may degrade with instructions over 300 lines.")
        print()

    # Write output files (keep local to TDD-guard-test)
    output_dir = Path(__file__).parent

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
    save_config(selected_modules, generate_tests, ide_config, target_path)

    # Claude IDE Integration (only if target_path is set)
    ide_results = {}
    if target_path:
        if ide_config['model_id']:
            ide_results['model'] = update_model_setting(ide_config['model_id'], target_path)

        ide_results['hooks'] = create_hooks(ide_config['enable_hooks'], target_path)
        ide_results['instructions'] = copy_instructions_to_ide(ide_config['copy_instructions'], instructions, target_path)

        # Get selected module objects for ignore patterns
        selected_module_objects = [m for m in available_modules if m.name in selected_modules]
        ide_results['ignore_patterns'] = configure_ignore_patterns(ide_config['configure_ignore_patterns'], selected_module_objects, target_path)

        # Configure pytest auto-approval
        ide_results['auto_approve_pytest'] = configure_auto_approve_pytest(ide_config['auto_approve_pytest'], target_path)
    else:
        # CLI mode without target_path - skip IDE integration
        ide_results = {'model': False, 'hooks': False, 'instructions': False, 'ignore_patterns': False, 'auto_approve_pytest': False}

    # Enforcement Configuration (only if target_path is set)
    if target_path:
        ide_results['enforcement'] = configure_enforcement(ide_config['protect_guard_settings'], ide_config['block_file_bypass'], target_path)
    else:
        ide_results['enforcement'] = False

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

    # Pytest Auto-Approval Results
    if ide_config['auto_approve_pytest']:
        auto_approve_status = "Enabled for pytest commands" if ide_results.get('auto_approve_pytest') else "Failed to enable"
        print(f"Auto-approve pytest: {auto_approve_status}")

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

    # PHASE 5.2: Installation Summary (only for wizard mode with target)
    if target_path:
        print()
        print("=" * 50)
        print("Installation Complete!")
        print("=" * 50)
        print()
        print("Target Project:", target_path.name)
        print("Location:", str(target_path))
        print()
        print("Configuration:")
        print("  Modules:", len(selected_modules), "modules selected")
        print("  Model:", ide_config.get('model_id', 'Not configured'))
        print("  Package: tdd-guard-pytest", "✓ Installed" if package_installed else "✗ Not installed")
        print()
        print("Files created in target project:")
        if ide_results.get('hooks'):
            print("  ✓", target_path / '.claude' / 'settings.local.json')
        if ide_results.get('instructions'):
            print("  ✓", target_path / '.claude' / 'tdd-guard' / 'data' / 'instructions.md')
        if ide_results.get('ignore_patterns'):
            print("  ✓", target_path / '.claude' / 'tdd-guard' / 'data' / 'config.json')
        print()
        print("Next steps:")
        print("  1. cd", str(target_path))
        print("  2. Restart Claude Code to load new hooks")
        print("  3. Start writing tests with TDD Guard protection!")
        print()

if __name__ == '__main__':
    main()