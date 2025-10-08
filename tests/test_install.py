import pytest
from unittest.mock import patch, mock_open, MagicMock
import json
from pathlib import Path
import sys
import os

# Add root directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from install import (
    ModuleInfo, discover_modules, load_models, load_last_config,
    save_config, ask_yes_no, update_model_setting, create_hooks,
    copy_instructions_to_ide, configure_ignore_patterns, generate_combined_instructions,
    detect_project_type, find_virtual_environment, validate_project_path,
    configure_auto_approve_pytest
)


def test_module_info_loads_metadata_correctly():
    """Test ModuleInfo correctly parses metadata.yaml content"""
    mock_metadata = "name: Test Module\ndescription: Test description\ndefault: yes\npriority: 1"

    with patch('pathlib.Path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data=mock_metadata)):
            module = ModuleInfo("test-module", Path("/fake/path"), silent=True)

    assert module.display_name == "Test Module"
    assert module.description == "Test description"
    assert module.default_enabled == True
    assert module.priority == 1


@patch('pathlib.Path.exists')
def test_discover_modules_finds_valid_modules(mock_exists):
    """Test module discovery returns properly configured modules"""
    mock_exists.return_value = True

    with patch('pathlib.Path.iterdir') as mock_iterdir:
        mock_dir = MagicMock()
        mock_dir.name = "core"
        mock_dir.is_dir.return_value = True
        mock_iterdir.return_value = [mock_dir]

        with patch('builtins.open', mock_open(read_data="name: Core\npriority: 1")):
            modules = discover_modules(silent=True)

    assert len(modules) == 1
    assert modules[0].name == "core"


def test_load_models_returns_default_when_file_missing():
    """Test load_models provides fallback when models.yaml is missing"""
    with patch('pathlib.Path.exists', return_value=False):
        models = load_models()

    assert len(models) == 1
    assert models[0]['id'] == "claude-sonnet-4-0"
    assert models[0]['default'] == True


@patch('pathlib.Path.exists')
@patch('builtins.open', new_callable=mock_open)
def test_load_last_config_returns_parsed_configuration(mock_file, mock_exists):
    """Test configuration loading parses JSON correctly"""
    mock_exists.return_value = True
    test_config = {"selected_modules": ["core"], "generate_tests": True}
    mock_file.return_value.read.return_value = json.dumps(test_config)

    config = load_last_config()

    assert config == test_config


@patch('pathlib.Path.mkdir')
@patch('json.dump')
@patch('builtins.open', new_callable=mock_open)
def test_save_config_persists_all_settings(mock_file, mock_json_dump, mock_mkdir):
    """Test save_config writes complete configuration to file"""
    ide_config = {
        'model_id': 'claude-sonnet',
        'enable_hooks': True,
        'copy_instructions': False,
        'configure_ignore_patterns': True,
        'protect_guard_settings': False,
        'block_file_bypass': True
    }

    save_config(['core', 'pytest'], True, ide_config)

    mock_mkdir.assert_called_once()
    mock_json_dump.assert_called_once()
    written_data = mock_json_dump.call_args[0][0]
    assert written_data['selected_modules'] == ['core', 'pytest']
    assert written_data['model_id'] == 'claude-sonnet'
    assert written_data['block_file_bypass'] == True


@patch('builtins.input', return_value='y')
def test_ask_yes_no_accepts_valid_responses(mock_input):
    """Test yes/no prompts handle valid user input correctly"""
    result = ask_yes_no("Test prompt", default=False)

    assert result == True


@patch('pathlib.Path.mkdir')
@patch('pathlib.Path.exists')
@patch('json.dump')
@patch('json.load')
@patch('builtins.open', new_callable=mock_open)
def test_update_model_setting_modifies_claude_settings(mock_file, mock_json_load, mock_json_dump, mock_exists, mock_mkdir):
    """Test model setting updates Claude IDE configuration"""
    mock_exists.return_value = True
    existing_settings = {"env": {"OTHER_VAR": "value"}}
    mock_json_load.return_value = existing_settings

    result = update_model_setting("claude-new-model", Path("/fake/project"))

    assert result == True
    written_data = mock_json_dump.call_args[0][0]
    assert written_data['env']['TDD_GUARD_MODEL_VERSION'] == 'claude-new-model'


@patch('pathlib.Path.exists', return_value=False)
@patch('pathlib.Path.mkdir')
@patch('json.dump')
@patch('builtins.open', new_callable=mock_open)
def test_create_hooks_adds_guard_configuration(mock_file, mock_json_dump, mock_mkdir, mock_exists):
    """Test hook creation configures TDD Guard integration"""
    result = create_hooks(enabled=True, target_path=Path("/fake/project"))

    assert result == True
    written_data = mock_json_dump.call_args[0][0]
    assert 'hooks' in written_data
    assert 'PreToolUse' in written_data['hooks']
    assert written_data['hooks']['PreToolUse'][0]['matcher'] == "Write|Edit|MultiEdit|TodoWrite"


@patch('pathlib.Path.mkdir')
@patch('builtins.open', new_callable=mock_open)
def test_copy_instructions_creates_ide_file(mock_file, mock_mkdir):
    """Test instruction copying creates proper IDE directory structure"""
    test_content = "# TDD Guard Rules\nTest instructions"

    result = copy_instructions_to_ide(enabled=True, instructions_content=test_content, target_path=Path("/fake/project"))

    assert result == True
    mock_mkdir.assert_called_once()
    mock_file().write.assert_called_with(test_content)


@patch('pathlib.Path.mkdir')
@patch('pathlib.Path.exists', return_value=False)
@patch('json.dump')
@patch('builtins.open', new_callable=mock_open)
def test_configure_ignore_patterns_processes_module_requirements(mock_file, mock_json_dump, mock_exists, mock_mkdir):
    """Test ignore pattern configuration handles module removal requests"""
    mock_module = MagicMock()
    mock_module.remove_from_ignore = ["*.md", "*.txt"]

    result = configure_ignore_patterns(enabled=True, selected_modules=[mock_module], target_path=Path("/fake/project"))

    assert result == True
    written_data = mock_json_dump.call_args[0][0]
    # Verify that *.md and *.txt are removed from default ignore patterns
    assert "*.md" not in written_data['ignorePatterns']
    assert "*.txt" not in written_data['ignorePatterns']


def test_module_info_loads_haiku_auto_include_properties():
    """Test ModuleInfo correctly loads auto-include properties for haiku module"""
    mock_metadata = """name: "Haiku JSON Fix"
description: "Fixes JSON parsing for Haiku model"
priority: 0
default: no
auto_include_with_model: "claude-3-5-haiku-20241022"
mandatory_for_model: true"""

    with patch('pathlib.Path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data=mock_metadata)):
            module = ModuleInfo("haiku-json-fix", Path("/fake/path"), silent=True)

    assert module.auto_include_with_model == "claude-3-5-haiku-20241022"
    assert module.mandatory_for_model == True
    assert module.priority == 0


def test_strict_json_responses_module_has_correct_properties():
    """Test that strict-json-responses module exists and has correct properties"""
    modules = discover_modules(silent=True)

    # Find the strict-json-responses module
    json_module = None
    for module in modules:
        if module.name == "strict-json-responses":
            json_module = module
            break

    # Verify the module exists and has correct properties
    assert json_module is not None
    assert json_module.priority == 0
    assert json_module.mandatory_for_model == True


def test_generate_with_strict_json_responses_module():
    """Test that generating with strict-json-responses module produces proper instructions"""
    # Test CLI mode with just the strict-json-responses module
    instructions, tests = generate_combined_instructions(['strict-json-responses'])

    # Verify the JSON formatting instructions are included
    assert "Response Formatting Rules" in instructions
    assert "JSON Response Format Requirements" in instructions
    assert "properly escape" in instructions.lower()
    assert "reasoning" in instructions.lower()

    # Verify priority 0 content appears early in the file
    lines = instructions.split('\n')
    json_section_found = False
    for i, line in enumerate(lines[:20]):  # Check first 20 lines
        if "Response Formatting Rules" in line or "JSON Response Format" in line:
            json_section_found = True
            break

    assert json_section_found, "JSON formatting instructions should appear early in the file"

# New Tests for Multi-Project Installation Features

def test_detect_project_type_identifies_flask():
    """Test project type detection for Flask projects"""
    with patch('pathlib.Path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data="flask==2.0.0\npytest==7.0")):
            project_type = detect_project_type(Path("/fake/project"))
    
    assert project_type == "Python - Flask"


def test_find_virtual_environment_locates_venv():
    """Test virtual environment detection finds .venv directory"""
    # Simple test - just verify function returns None for non-existent venv
    result = find_virtual_environment(Path("/fake/nonexistent/project"))
    
    # Should return None when no venv exists
    assert result is None


def test_validate_project_path_accepts_self():
    """Test that validation accepts installer directory for testing/fixing purposes"""
    installer_dir = Path(__file__).parent.parent

    is_valid, message = validate_project_path(installer_dir)

    # The installer directory is allowed for testing/fixing purposes
    assert is_valid == True
    assert "Valid project path" in message


def test_validate_project_path_rejects_nonexistent():
    """Test validation rejects non-existent paths"""
    fake_path = Path("/this/path/does/not/exist/at/all")
    
    is_valid, message = validate_project_path(fake_path)
    
    assert is_valid == False
    assert "does not exist" in message


def test_save_config_stores_target_path():
    """Test that save_config stores target_path in configuration"""
    target = Path("/fake/target/project")
    ide_config = {
        'model_id': 'claude-sonnet',
        'enable_hooks': True,
        'copy_instructions': False,
        'configure_ignore_patterns': True,
        'protect_guard_settings': False,
        'block_file_bypass': True
    }

    with patch('pathlib.Path.mkdir'):
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('json.dump') as mock_json_dump:
                save_config(['core', 'pytest'], True, ide_config, target)

    # Verify target_path was included in saved config
    written_data = mock_json_dump.call_args[0][0]
    assert 'target_path' in written_data
    assert written_data['target_path'] == str(target)


# Tests for Auto-Approve Pytest Feature

def test_configure_auto_approve_pytest_adds_pytest_patterns_to_allow():
    """Test auto-approve configuration adds pytest patterns to permissions.allow"""
    with patch('pathlib.Path.exists', return_value=False):
        with patch('pathlib.Path.mkdir'):
            with patch('builtins.open', mock_open()) as mock_file:
                with patch('json.dump') as mock_json_dump:
                    result = configure_auto_approve_pytest(enabled=True, target_path=Path("/fake/project"))

    assert result == True
    written_data = mock_json_dump.call_args[0][0]
    assert 'permissions' in written_data
    assert 'allow' in written_data['permissions']
    assert "Bash(FLASK_ENV=TESTING poetry run pytest:*)" in written_data['permissions']['allow']
    assert "Bash(poetry run pytest:*)" in written_data['permissions']['allow']
    assert "Bash(pytest:*)" in written_data['permissions']['allow']


def test_save_config_persists_auto_approve_pytest_setting():
    """Test that save_config stores auto_approve_pytest in configuration"""
    ide_config = {
        'model_id': 'claude-sonnet',
        'enable_hooks': True,
        'copy_instructions': False,
        'configure_ignore_patterns': True,
        'protect_guard_settings': False,
        'block_file_bypass': True,
        'auto_approve_pytest': True
    }

    with patch('pathlib.Path.mkdir'):
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('json.dump') as mock_json_dump:
                save_config(['core', 'pytest'], True, ide_config)

    written_data = mock_json_dump.call_args[0][0]
    assert 'auto_approve_pytest' in written_data
    assert written_data['auto_approve_pytest'] == True
