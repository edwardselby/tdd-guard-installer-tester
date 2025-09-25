#!/usr/bin/env python3
"""
TDD Guard Instruction Generator

Combines modular instruction files into complete TDD Guard instructions.

Usage:
    python generate.py core pytest flask                    # Custom combination
    python generate.py --list                               # List available modules
    python generate.py --all                                # Include all modules
    python generate.py core test-duplication --output custom.md  # Custom output file

Examples:
    python generate.py core test-duplication fake-implementation pytest
    python generate.py core quality-control  # Minimal setup
    python generate.py --all                 # Full feature set
"""

import os
import sys
import argparse
from pathlib import Path

# Module priority order (lower numbers = higher priority, checked first)
MODULE_PRIORITIES = {
    'core': 4,                    # Core TDD workflow
    'test-duplication': 1,        # Critical - check first
    'fake-implementation': 2,     # Second priority
    'comment-violations': 1,      # Critical - check first
    'quality-control': 1,         # Critical - check first
    'pytest': 5,                  # Framework enforcement
    'backend-frameworks': 3,      # Third priority
    'advanced-evasion': 6,        # Advanced patterns
    'meta': 7,                    # Meta-rules (decision matrix, templates)
}

def get_available_modules():
    """Get list of available modules from the modules directory."""
    modules_dir = Path(__file__).parent.parent / 'modules'
    if not modules_dir.exists():
        return []

    modules = []
    for module_dir in modules_dir.iterdir():
        if module_dir.is_dir() and (module_dir / 'instructions.md').exists():
            modules.append(module_dir.name)

    return sorted(modules)

def load_module_content(module_name):
    """Load instruction and test content for a module."""
    modules_dir = Path(__file__).parent.parent / 'modules'
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

def generate_combined_instructions(modules):
    """Generate combined instructions from selected modules."""

    # Sort modules by priority (lower number = higher priority)
    sorted_modules = sorted(modules, key=lambda m: MODULE_PRIORITIES.get(m, 999))

    # Always include core and meta if not specified
    if 'core' not in sorted_modules:
        sorted_modules.insert(0, 'core')
    if 'meta' not in sorted_modules:
        sorted_modules.append('meta')

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
        description='Generate TDD Guard instructions from modular components',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        'modules',
        nargs='*',
        help='Module names to include (e.g., core pytest flask)'
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

    parser.add_argument(
        '--output',
        default='generated/INSTRUCTIONS_GENERATED.md',
        help='Output filename for instructions (default: generated/INSTRUCTIONS_GENERATED.md)'
    )

    parser.add_argument(
        '--test-output',
        default='generated/TESTING_GENERATED.md',
        help='Output filename for tests (default: generated/TESTING_GENERATED.md)'
    )

    args = parser.parse_args()

    available_modules = get_available_modules()

    if not available_modules:
        print("Error: No modules found. Make sure modules/ directory exists with instruction files.")
        sys.exit(1)

    if args.list:
        print("Available modules:")
        for module in available_modules:
            priority = MODULE_PRIORITIES.get(module, 999)
            print(f"  {module:<20} (Priority: {priority})")
        print("\\nPriority levels: 1=Critical, 2-3=Core, 4-5=Framework, 6-7=Advanced")
        return

    if args.all:
        selected_modules = available_modules
    elif args.modules:
        selected_modules = args.modules
        # Validate module names
        invalid_modules = [m for m in selected_modules if m not in available_modules]
        if invalid_modules:
            print(f"Error: Unknown modules: {', '.join(invalid_modules)}")
            print(f"Available modules: {', '.join(available_modules)}")
            sys.exit(1)
    else:
        print("Error: No modules specified. Use --list to see available modules or --help for usage.")
        sys.exit(1)

    # Generate combined content
    instructions, tests = generate_combined_instructions(selected_modules)

    # Check line count and warn if over 300 lines
    instruction_lines = instructions.count('\n') + 1
    if instruction_lines > 300:
        print(f"⚠️  WARNING: Generated instructions are {instruction_lines} lines (exceeds 300-line limit)")
        print("   Quality may degrade with instructions over 300 lines. Consider reducing module bloat.")
        print()

    # Write output files
    output_dir = Path(__file__).parent.parent

    # Ensure generated directory exists
    generated_dir = output_dir / 'generated'
    generated_dir.mkdir(exist_ok=True)

    instructions_file = output_dir / args.output
    with open(instructions_file, 'w') as f:
        f.write(instructions)

    tests_file = output_dir / args.test_output
    with open(tests_file, 'w') as f:
        f.write(tests)

    print(f"Generated instructions: {instructions_file}")
    print(f"Generated tests: {tests_file}")
    print(f"Modules included: {', '.join(selected_modules)}")
    print(f"Total modules: {len(selected_modules)}")

if __name__ == '__main__':
    main()