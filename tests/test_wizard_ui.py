"""
Tests for Rich UI wizard components

Following TDD methodology - each test written before implementation
"""
from unittest.mock import patch, MagicMock

def test_console_instance_exists():
    """Test that Rich console is available"""
    from install import get_console

    console = get_console()
    assert console is not None
    assert hasattr(console, 'print')


def test_ask_yes_no_uses_rich_confirm():
    """Test ask_yes_no delegates to Rich Confirm.ask"""
    from install import ask_yes_no

    with patch('rich.prompt.Confirm.ask', return_value=True) as mock_confirm:
        result = ask_yes_no("Test prompt", default=True)

        assert result is True
        mock_confirm.assert_called_once_with("Test prompt", default=True)


def test_print_step_header_displays_panel():
    """Test step header prints a Rich Panel with progress"""
    from install import print_step_header

    mock_console = MagicMock()
    with patch('install.get_console', return_value=mock_console):
        print_step_header("Module Selection", 2, 5)

        mock_console.print.assert_called_once()
        call_args = mock_console.print.call_args[0]
        assert len(call_args) > 0


def test_print_modules_table_displays_table():
    """Test module display creates Rich Table with modules"""
    from install import print_modules_table, ModuleInfo
    from pathlib import Path

    mock_console = MagicMock()
    mock_modules = [
        ModuleInfo("test-module", Path("/fake"), silent=True)
    ]

    with patch('install.get_console', return_value=mock_console):
        print_modules_table(mock_modules)

        mock_console.print.assert_called_once()
        call_args = mock_console.print.call_args[0]
        assert len(call_args) > 0


def test_parse_module_selection_simple_numbers():
    """Test parsing simple space-separated numbers like '1 3 5'"""
    from install import parse_module_selection

    result = parse_module_selection("1 3 5", 10)

    assert result == [0, 2, 4]


def test_parse_module_selection_ranges():
    """Test parsing ranges like '1-5' expands to [0,1,2,3,4]"""
    from install import parse_module_selection

    result = parse_module_selection("1-5", 10)

    assert result == [0, 1, 2, 3, 4]


def test_parse_module_selection_shortcut_all():
    """Test 'all' shortcut selects all modules"""
    from install import parse_module_selection

    result = parse_module_selection("all", 5)

    assert result == [0, 1, 2, 3, 4]


def test_select_wizard_mode_returns_choice():
    """Test wizard mode selection prompts user and returns choice"""
    from install import select_wizard_mode

    with patch('rich.prompt.Prompt.ask', return_value='1') as mock_prompt:
        result = select_wizard_mode()

        assert result == 'express'
        mock_prompt.assert_called_once()


def test_get_express_mode_config_returns_defaults():
    """Test express mode returns configuration with recommended defaults"""
    from install import get_express_mode_config, ModuleInfo
    from pathlib import Path

    mock_modules = [
        ModuleInfo("module1", Path("/fake1"), silent=True),
        ModuleInfo("module2", Path("/fake2"), silent=True)
    ]
    mock_models = [{"id": "model1", "default": True}]

    config = get_express_mode_config(mock_modules, mock_models)

    assert 'selected_modules' in config
    assert 'model_id' in config
    assert 'ide_config' in config
    assert config['ide_config']['enable_hooks'] is True


def test_run_wizard_with_mode_parameter():
    """Test run_wizard accepts and uses mode parameter"""
    from install import run_wizard, ModuleInfo
    from pathlib import Path

    mock_modules = [
        ModuleInfo("module1", Path("/fake1"), silent=True)
    ]

    with patch('install.load_last_config', return_value=None):
        with patch('install.get_express_mode_config') as mock_config:
            mock_config.return_value = {
                'selected_modules': ['module1'],
                'model_id': 'model1',
                'ide_config': {'enable_hooks': True},
                'generate_tests': True
            }
            with patch('install.load_models', return_value=[{"id": "model1"}]):
                result = run_wizard(mock_modules, mode='express')

                assert result is not None
                mock_config.assert_called_once()
