# Pytest Standards Enforcement

## Priority Level: 5 (Fifth Priority)

## 🧪 PYTEST STANDARDS ENFORCEMENT

### Test Framework Requirements
❌ **BLOCK:** unittest framework (`class TestSomething`, `self.assert*`)
✅ **REQUIRE:** pytest flat functions (`def test_function()`, `assert condition`)

### Mock Pattern Enforcement
❌ **BLOCK:** `with patch('module.func') as mock:` (context managers)
✅ **REQUIRE:** `@patch('module.func')` decorators above function

### Mock Organization Standards
❌ **BLOCK:** Shared mocks in individual test files
✅ **REQUIRE:** Cross-file mocks in `conftest.py`, file-specific mocks at top

### Test Structure Requirements
❌ **BLOCK:** Multiple similar tests (`test_discount_gold`, `test_discount_silver`)
✅ **REQUIRE:** `@pytest.mark.parametrize` for similar scenarios

### Exception Testing Standards
❌ **BLOCK:** `self.assertRaises(ValueError)`
✅ **REQUIRE:** `with pytest.raises(ValueError):`