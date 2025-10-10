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


def test_select_model_displays_rich_table():
    """Test model selection uses Rich table instead of print"""
    from install import select_model

    models = [
        {"id": "model1", "name": "Model 1", "description": "Test model", "default": True},
        {"id": "model2", "name": "Model 2", "description": "Another model", "default": False}
    ]

    with patch('install.get_console') as mock_console:
        with patch('rich.prompt.Prompt.ask', return_value='1'):
            result = select_model(models)

            # Should print Rich table
            mock_console.return_value.print.assert_called()
            assert result['id'] == 'model1'


def test_select_from_exclusive_group_uses_rich():
    """Test exclusive group selection uses Rich panel and table"""
    from install import select_from_exclusive_group, ModuleInfo
    from pathlib import Path

    modules = [
        ModuleInfo("mod1", Path("/fake1"), silent=True),
        ModuleInfo("mod2", Path("/fake2"), silent=True)
    ]

    with patch('install.get_console') as mock_console:
        with patch('rich.prompt.Prompt.ask', return_value='1'):
            result = select_from_exclusive_group("core-tdd", modules)

            # Should print Rich components
            mock_console.return_value.print.assert_called()
            assert result.name == "mod1"


def test_select_standalone_modules_uses_rich():
    """Test standalone module selection uses Rich table and Confirm"""
    from install import select_standalone_modules

    # Mock ModuleInfo objects
    mod1 = MagicMock()
    mod1.name = "mod1"
    mod1.display_name = "Module 1"
    mod1.description = "Test module 1"
    mod1.line_count = 100
    mod1.default_enabled = True

    mod2 = MagicMock()
    mod2.name = "mod2"
    mod2.display_name = "Module 2"
    mod2.description = "Test module 2"
    mod2.line_count = 200
    mod2.default_enabled = False

    modules = [mod1, mod2]

    with patch('install.get_console') as mock_console:
        with patch('rich.prompt.Confirm.ask', side_effect=[True, False]):
            selected = select_standalone_modules(modules)

            # Should print Rich components
            mock_console.return_value.print.assert_called()
            assert len(selected) == 1
            assert selected[0].name == "mod1"


def test_show_line_count_warning_uses_rich_panel():
    """Test line count warning displays Rich Panel with yellow styling"""
    from install import show_line_count_warning

    with patch('install.get_console') as mock_console:
        show_line_count_warning(450, threshold=300)

        # Should print Rich Panel with warning
        mock_console.return_value.print.assert_called()
        # Verify it was called (Panel will be in call args)
        assert mock_console.return_value.print.call_count >= 1


def test_show_generation_results_uses_rich_table():
    """Test generation results display uses Rich Table"""
    from install import show_generation_results
    from pathlib import Path

    results = {
        'instructions_file': Path('/fake/instructions.md'),
        'instruction_lines': 500,
        'tests_file': Path('/fake/tests.md'),
        'test_lines': 100,
        'instructions_valid': True,
        'tests_valid': True,
        'selected_modules': ['core', 'pytest'],
        'ide_results': {
            'model': True,
            'hooks': True,
            'instructions': True,
            'ignore_patterns': True,
            'auto_approve_pytest': True,
            'enforcement': True
        },
        'ide_config': {
            'model_id': 'claude-sonnet-4-0',
            'enable_hooks': True,
            'copy_instructions': True,
            'configure_ignore_patterns': True,
            'auto_approve_pytest': True,
            'protect_guard_settings': True,
            'block_file_bypass': False
        }
    }

    with patch('install.get_console') as mock_console:
        show_generation_results(results)

        # Should print Rich Panel and Table
        mock_console.return_value.print.assert_called()
        assert mock_console.return_value.print.call_count >= 2


def test_is_interactive_terminal_returns_true_for_tty():
    """Test TTY detection returns True for interactive terminals"""
    from install import is_interactive_terminal

    with patch('sys.stdin.isatty', return_value=True):
        assert is_interactive_terminal() is True


def test_is_interactive_terminal_returns_false_for_non_tty():
    """Test TTY detection returns False for non-interactive terminals (CI/CD)"""
    from install import is_interactive_terminal

    with patch('sys.stdin.isatty', return_value=False):
        assert is_interactive_terminal() is False


def test_select_model_interactive_calls_inquirer():
    """Test that select_model_interactive uses InquirerPy for arrow-key selection"""
    from install import select_model_interactive

    models = [{"id": "sonnet", "name": "Claude Sonnet 4.0", "description": "Balanced", "default": True}]

    mock_select = MagicMock()
    mock_select.execute.return_value = models[0]

    with patch('InquirerPy.inquirer.select', return_value=mock_select):
        result = select_model_interactive(models)

        assert result == models[0]


def test_select_from_exclusive_group_interactive_calls_inquirer():
    """Test that exclusive group selection uses InquirerPy select for radio buttons"""
    from install import select_from_exclusive_group_interactive, ModuleInfo
    from pathlib import Path

    modules = [ModuleInfo("core-strict", Path("/fake"), silent=True)]

    mock_select = MagicMock()
    mock_select.execute.return_value = modules[0]

    with patch('InquirerPy.inquirer.select', return_value=mock_select):
        result = select_from_exclusive_group_interactive("core-tdd", modules)

        assert result == modules[0]


def test_select_standalone_modules_interactive_calls_checkbox():
    """Test that standalone module selection uses InquirerPy checkbox for multi-select"""
    from install import select_standalone_modules_interactive, ModuleInfo
    from pathlib import Path

    modules = [ModuleInfo("pytest", Path("/fake"), silent=True)]

    mock_checkbox = MagicMock()
    mock_checkbox.execute.return_value = [modules[0]]

    with patch('InquirerPy.inquirer.checkbox', return_value=mock_checkbox):
        result = select_standalone_modules_interactive(modules)

        assert result == [modules[0]]
