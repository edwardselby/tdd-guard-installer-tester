#!/usr/bin/env python3
"""
TDD Guard Module Validator

Validates that all modules have proper instruction-test coverage and consistency.

Usage:
    python validate.py                    # Validate all modules
    python validate.py core pytest       # Validate specific modules
    python validate.py --check-coverage  # Check test coverage completeness
    python validate.py --fix-format      # Fix formatting issues automatically
"""

import os
import sys
import argparse
import re
from pathlib import Path
from collections import defaultdict

def get_module_paths():
    """Get all module directories."""
    modules_dir = Path(__file__).parent.parent / 'modules'
    if not modules_dir.exists():
        return []

    return [d for d in modules_dir.iterdir() if d.is_dir()]

def validate_module_structure(module_dir):
    """Validate that module has required files."""
    issues = []
    module_name = module_dir.name

    instructions_file = module_dir / 'instructions.md'
    test_file = module_dir / 'test-scenarios.md'

    if not instructions_file.exists():
        issues.append(f"{module_name}: Missing instructions.md")

    if not test_file.exists():
        issues.append(f"{module_name}: Missing test-scenarios.md")

    return issues

def analyze_instructions(instructions_content, module_name):
    """Analyze instruction content for required elements."""
    issues = []

    # Check for required sections
    required_sections = [
        r'# .+',  # Title
        r'## Priority Level:',  # Priority
        r'❌.*BLOCK.*',  # At least one block rule
        r'## Error Templates',  # Error templates
        r'## Integration Notes'  # Integration notes
    ]

    for pattern in required_sections:
        if not re.search(pattern, instructions_content, re.MULTILINE | re.IGNORECASE):
            issues.append(f"{module_name}: Missing required section matching '{pattern}'")

    # Check for proper error template format
    error_templates = re.findall(r'- `❌ .+ → .+`', instructions_content)
    if not error_templates:
        issues.append(f"{module_name}: No properly formatted error templates found")

    return issues

def analyze_test_scenarios(test_content, module_name):
    """Analyze test scenario content."""
    issues = []

    # Count test scenarios
    test_patterns = [
        r'### Test \d+\.\d+:',  # Numbered tests
        r'#### Test \d+\.\d+:',  # Sub-numbered tests
    ]

    total_tests = 0
    for pattern in test_patterns:
        matches = re.findall(pattern, test_content)
        total_tests += len(matches)

    if total_tests == 0:
        issues.append(f"{module_name}: No test scenarios found")

    # Check for expected outcomes
    expected_patterns = [
        r'\\*\\*Expected\\*\\*:',
        r'Expected:',
    ]

    expected_count = 0
    for pattern in expected_patterns:
        matches = re.findall(pattern, test_content, re.IGNORECASE)
        expected_count += len(matches)

    if expected_count < total_tests:
        issues.append(f"{module_name}: {total_tests} tests but only {expected_count} expected outcomes")

    return issues, total_tests

def check_coverage_completeness():
    """Check that modular system covers all original functionality."""
    # This would compare against original INSTRUCTIONS_V1.md
    # For now, just verify all expected modules exist
    expected_modules = {
        'core', 'test-duplication', 'fake-implementation',
        'comment-violations', 'quality-control', 'pytest',
        'backend-frameworks', 'advanced-evasion', 'meta'
    }

    modules_dir = Path(__file__).parent.parent / 'modules'
    actual_modules = {d.name for d in modules_dir.iterdir() if d.is_dir()}

    missing = expected_modules - actual_modules
    extra = actual_modules - expected_modules

    issues = []
    if missing:
        issues.append(f"Missing expected modules: {', '.join(missing)}")
    if extra:
        issues.append(f"Unexpected modules found: {', '.join(extra)}")

    return issues

def validate_modules(module_names=None):
    """Validate specified modules or all modules."""
    module_dirs = get_module_paths()

    if module_names:
        module_dirs = [d for d in module_dirs if d.name in module_names]
        if len(module_dirs) != len(module_names):
            found_names = {d.name for d in module_dirs}
            missing = set(module_names) - found_names
            print(f"Warning: Could not find modules: {', '.join(missing)}")

    all_issues = []
    module_stats = {}

    for module_dir in module_dirs:
        module_name = module_dir.name
        print(f"Validating module: {module_name}")

        # Check file structure
        structure_issues = validate_module_structure(module_dir)
        all_issues.extend(structure_issues)

        if structure_issues:
            continue  # Skip content validation if files missing

        # Validate instructions
        instructions_file = module_dir / 'instructions.md'
        instructions_content = instructions_file.read_text()
        instruction_issues = analyze_instructions(instructions_content, module_name)
        all_issues.extend(instruction_issues)

        # Validate test scenarios
        test_file = module_dir / 'test-scenarios.md'
        test_content = test_file.read_text()
        test_issues, test_count = analyze_test_scenarios(test_content, module_name)
        all_issues.extend(test_issues)

        module_stats[module_name] = {
            'test_count': test_count,
            'instruction_lines': len(instructions_content.split('\\n')),
            'test_lines': len(test_content.split('\\n')),
            'issues': len([i for i in all_issues if i.startswith(module_name)])
        }

    return all_issues, module_stats

def print_validation_report(issues, module_stats, check_coverage=False):
    """Print validation report."""
    print("\\n" + "="*60)
    print("TDD GUARD MODULE VALIDATION REPORT")
    print("="*60)

    if check_coverage:
        coverage_issues = check_coverage_completeness()
        issues.extend(coverage_issues)

    if issues:
        print("\\n❌ ISSUES FOUND:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("\\n✅ ALL MODULES VALID")

    print("\\n📊 MODULE STATISTICS:")
    print(f"{'Module':<20} {'Tests':<8} {'Issues':<8} {'Inst Lines':<12} {'Test Lines'}")
    print("-" * 60)

    total_tests = 0
    total_issues = 0
    for module, stats in sorted(module_stats.items()):
        total_tests += stats['test_count']
        total_issues += stats['issues']
        print(f"{module:<20} {stats['test_count']:<8} {stats['issues']:<8} {stats['instruction_lines']:<12} {stats['test_lines']}")

    print("-" * 60)
    print(f"{'TOTAL':<20} {total_tests:<8} {total_issues:<8}")
    print(f"\\nModules: {len(module_stats)}, Tests: {total_tests}, Issues: {total_issues}")

    if total_issues == 0:
        print("\\n🎉 Perfect! All modules are properly structured and documented.")
    else:
        print(f"\\n⚠️  Found {total_issues} issues across {len(module_stats)} modules.")

def main():
    parser = argparse.ArgumentParser(
        description='Validate TDD Guard modular components',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        'modules',
        nargs='*',
        help='Module names to validate (default: all modules)'
    )

    parser.add_argument(
        '--check-coverage',
        action='store_true',
        help='Check that modules cover all original functionality'
    )

    args = parser.parse_args()

    print("TDD Guard Module Validator")
    print("-" * 40)

    issues, module_stats = validate_modules(args.modules)
    print_validation_report(issues, module_stats, args.check_coverage)

    # Exit with error code if issues found
    sys.exit(1 if issues else 0)

if __name__ == '__main__':
    main()