# TDD Workflow Architecture for Flask Task Tracker

A comprehensive Test-Driven Development (TDD) implementation with automated workflows, ruthless testing, and complete CI/CD integration.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up git hooks for TDD workflow
python scripts/setup_git_hooks.py

# Run all tests
python scripts/test_runner.py

# Start TDD cycle for new feature
python scripts/red_green_refactor.py --start-feature "user_auth" "tests/unit/test_auth.py"
```

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Test Structure](#test-structure)
3. [TDD Workflow](#tdd-workflow)
4. [Example Implementation](#example-implementation)
5. [Scripts and Automation](#scripts-and-automation)
6. [CI/CD Pipeline](#cicd-pipeline)
7. [Quality Gates](#quality-gates)
8. [Usage Examples](#usage-examples)

## 🏗️ Architecture Overview

This project implements a complete TDD architecture with three test layers and automated workflow management:

```
TDD Architecture
├── 🔴 RED Phase: Write failing tests
├── 🟢 GREEN Phase: Make tests pass
├── 🔵 REFACTOR Phase: Improve code quality
└── 🔄 Automated cycle management
```

### Test Layers

```
tests/
├── unit/           # Fast, isolated tests with mocks
├── integration/    # Component interaction tests
├── e2e/           # End-to-end workflow tests
└── conftest.py    # Shared test configuration
```

## 🧪 Test Structure

### Unit Tests (`tests/unit/`)
- **Purpose**: Test individual components in complete isolation
- **Speed**: < 0.1 seconds per test
- **Dependencies**: All external dependencies mocked
- **Coverage**: 90%+ required

**Example**: `tests/unit/test_task_model.py`
```python
@patch('app.models.task.datetime')
def test_create_task_sets_current_timestamp(mock_datetime):
    mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
    task = Task.create(title='Test')
    assert task['created_at'] == datetime(2024, 1, 1, 12, 0, 0)
```

### Integration Tests (`tests/integration/`)
- **Purpose**: Test component interactions with real dependencies
- **Speed**: < 5 seconds per test
- **Dependencies**: Real database (mongomock), mocked external services
- **Focus**: Data flow and component integration

### End-to-End Tests (`tests/e2e/`)
- **Purpose**: Test complete user workflows
- **Speed**: 5-30 seconds per test
- **Dependencies**: Full system testing
- **Focus**: User scenarios and API contracts

## 🔄 TDD Workflow

### Red-Green-Refactor Cycle

#### 🔴 RED Phase
1. Write a failing test that defines desired behavior
2. Test should be minimal and specific
3. Run test to confirm it fails for the right reason

```bash
python scripts/red_green_refactor.py --start-feature "task_tags" "tests/unit/test_task_tags.py"
```

#### 🟢 GREEN Phase
1. Write minimal code to make the test pass
2. Don't worry about perfect design yet
3. Focus on functionality over form

```bash
python scripts/red_green_refactor.py --green
```

#### 🔵 REFACTOR Phase
1. Improve code quality without changing behavior
2. Extract methods, eliminate duplication
3. Keep all tests passing throughout

```bash
python scripts/red_green_refactor.py --refactor
```

### Automated Cycle Management

The TDD cycle manager tracks your progress and provides guidance:

```bash
# Check current phase
python scripts/red_green_refactor.py --status

# Check if ready for next phase
python scripts/red_green_refactor.py --check

# Complete cycle with git commit
python scripts/red_green_refactor.py --complete
```

## 🏷️ Example Implementation: Task Tags Feature

This project includes a complete TDD implementation of a task tagging feature:

### RED Phase: Failing Tests
```python
def test_add_tag_to_task_with_no_existing_tags(self):
    """Test adding a tag to a task that has no tags."""
    task_data = {'title': 'Test Task', 'tags': []}

    # This will fail because TaskTags doesn't exist yet
    from app.models.task_tags import TaskTags
    result = TaskTags.add_tag(task_data, 'urgent')

    assert 'urgent' in result['tags']
    assert len(result['tags']) == 1
```

### GREEN Phase: Minimal Implementation
```python
class TaskTags:
    @classmethod
    def add_tag(cls, task_data, tag):
        """Add a tag to a task."""
        result = task_data.copy()
        if 'tags' not in result:
            result['tags'] = []

        if tag not in result['tags']:
            result['tags'].append(tag)

        return result
```

### REFACTOR Phase: Enhanced Implementation
```python
class TaskTags:
    @classmethod
    def add_tag(cls, task_data: Dict[str, Any], tag: str) -> Dict[str, Any]:
        """Add a validated and normalized tag to a task."""
        cls.validate_tag(tag)
        normalized_tag = cls.normalize_tag(tag)

        result = task_data.copy()
        if 'tags' not in result:
            result['tags'] = []

        if normalized_tag not in result['tags']:
            result['tags'].append(normalized_tag)

        return result
```

## 🔧 Scripts and Automation

### Test Runner (`scripts/test_runner.py`)
Comprehensive test execution with multiple options:

```bash
# Run all tests with coverage
python scripts/test_runner.py

# Run specific test layers
python scripts/test_runner.py --unit
python scripts/test_runner.py --integration
python scripts/test_runner.py --e2e

# Run fast tests for quick feedback
python scripts/test_runner.py --fast

# Run tests in parallel
python scripts/test_runner.py --parallel

# Watch for changes and auto-run tests
python scripts/test_runner.py --watch
```

### TDD Cycle Manager (`scripts/red_green_refactor.py`)
Automated workflow management:

```bash
# Start new feature
python scripts/red_green_refactor.py --start-feature "feature_name" "test_file.py"

# Transition between phases
python scripts/red_green_refactor.py --green
python scripts/red_green_refactor.py --refactor

# Complete cycle
python scripts/red_green_refactor.py --complete
```

### CI Pipeline (`scripts/ci_test_pipeline.py`)
Complete CI/CD pipeline:

```bash
# Run full pipeline
python scripts/ci_test_pipeline.py

# Custom coverage threshold
python scripts/ci_test_pipeline.py --coverage-threshold 95
```

### Git Hooks Setup (`scripts/setup_git_hooks.py`)
Automated git workflow integration:

```bash
# Install TDD git hooks
python scripts/setup_git_hooks.py
```

## 🚀 CI/CD Pipeline

### GitHub Actions Workflow (`.github/workflows/tdd-ci.yml`)

**Multi-stage pipeline**:
1. **Code Quality**: Linting, formatting, syntax checks
2. **Unit Tests**: Fast tests with coverage reporting
3. **Integration Tests**: Component interaction testing
4. **Security Tests**: Security-focused test validation
5. **E2E Tests**: Complete workflow validation
6. **Quality Gate**: Coverage and test result validation

**Matrix Testing**: Python 3.9, 3.10, 3.11

**Deployment Flow**:
- `develop` branch → Staging environment
- `main` branch → Production environment

### Quality Gates

**Automated checks**:
- ✅ Minimum 90% test coverage
- ✅ All required tests passing
- ✅ No security vulnerabilities
- ✅ Code quality standards met

## 🛡️ Quality Standards

### Coverage Requirements
- **Minimum**: 90% line coverage
- **Reports**: HTML, XML, terminal output
- **Enforcement**: CI pipeline failure below threshold

### Test Quality Checklist
- [ ] Every function has tests for success and failure scenarios
- [ ] All external dependencies mocked in unit tests
- [ ] Tests use realistic data, not generic "test" strings
- [ ] Error tests verify specific error types and messages
- [ ] Mock interactions verified with exact expected calls
- [ ] Tests would actually fail if implementation was broken

### Security Testing
```python
@pytest.mark.security
def test_task_creation_prevents_xss():
    """Test that task creation sanitizes malicious content."""
    malicious_data = {
        'title': '<script>alert("xss")</script>',
        'description': '<img src="x" onerror="alert(1)">'
    }

    result = create_task(malicious_data)

    assert '<script>' not in result['title']
    assert 'onerror=' not in result['description']
```

## 📊 Testing Approach: Ruthless Validation

### Mindset: Destroy the Code
**Mission**: Find every possible way the code can break

**Test Categories**:
1. **Happy Path**: Normal expected usage
2. **Input Validation**: Empty, None, wrong type, malformed data
3. **Edge Cases**: Boundary values, extreme inputs
4. **Error Handling**: How does it handle failures?
5. **Dependencies**: What happens when external services fail?
6. **State Changes**: Does it modify state correctly?

### Example: Ruthless Testing
```python
def test_create_task_with_invalid_inputs():
    """Test all possible invalid inputs."""
    invalid_inputs = [
        None,                    # None input
        {},                      # Empty dict
        {'title': ''},          # Empty title
        {'title': None},        # None title
        {'title': 123},         # Wrong type
        {'title': 'x' * 10000}, # Extremely long
        {'status': 'invalid'},  # Invalid status
    ]

    for invalid_input in invalid_inputs:
        with pytest.raises((ValueError, ValidationError)):
            create_task(invalid_input)
```

## 🔧 Usage Examples

### Running Tests

```bash
# Quick development feedback
python scripts/test_runner.py --fast

# Full test suite with coverage
python scripts/test_runner.py --coverage

# Run only failing tests
python scripts/test_runner.py --lf

# Run tests matching pattern
pytest -k "test_create" tests/unit/

# Run with specific markers
pytest -m "security" tests/
```

### TDD Development Workflow

```bash
# 1. Start new feature
python scripts/red_green_refactor.py --start-feature "user_auth" "tests/unit/test_auth.py"

# 2. Write failing test (RED)
# Edit test file and run
python scripts/red_green_refactor.py --red

# 3. Write minimal implementation (GREEN)
# Edit implementation and run
python scripts/red_green_refactor.py --green

# 4. Refactor and improve (REFACTOR)
# Clean up code and run
python scripts/red_green_refactor.py --refactor

# 5. Complete cycle
python scripts/red_green_refactor.py --complete
```

### Git Workflow Integration

```bash
# Set up git hooks
python scripts/setup_git_hooks.py

# Commits will automatically:
# - Check syntax
# - Run fast tests
# - Suggest TDD commit formats

# TDD commit formats
git commit -m "RED: Add failing test for user authentication"
git commit -m "GREEN: Implement basic user login"
git commit -m "REFACTOR: Extract validation logic"
git commit -m "TDD: Complete user authentication feature"
```

## 📚 Documentation

- **[TDD Guidelines](docs/TDD_GUIDELINES.md)**: Comprehensive TDD best practices
- **[API Documentation](docs/API.md)**: REST API specifications
- **[Architecture Decision Records](docs/ADRs/)**: Design decisions and rationale

## 🤝 Contributing

1. Follow TDD workflow: RED → GREEN → REFACTOR
2. Maintain 90%+ test coverage
3. Use ruthless testing approach
4. Write tests before implementation
5. Keep tests fast and isolated

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Remember**: Be ruthless in your testing, compassionate in your feedback, and relentless in your pursuit of quality.

*"The goal is not to write tests, but to write better software through testing."*