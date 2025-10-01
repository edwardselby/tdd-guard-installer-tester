# Strict JSON Response Format Test Scenarios

## Overview
This test scenario is designed to **consistently reproduce** the "Bad control character in string literal in JSON" error that occurs when Claude CLI validator returns responses for large, complex files.

## Root Cause (Confirmed)

**Error Location**: `tdd-guard's validator.js:25` - JSON parsing failure

**Trigger Mechanism**:
1. User creates a **very large test file** (200+ lines)
2. TDD Guard sends file content to Claude CLI validator
3. Claude CLI generates a **large validation response** that includes reasoning about the file
4. The response JSON contains **unescaped newlines and special characters**
5. JSON parser fails: "Bad control character in string literal in JSON"

**Key Discovery**: The error is triggered by **file length and complexity**, not specific content patterns.

- ✅ **Large files** (200+ lines): 100% failure rate
- ✅ **Small files** (<50 lines): 0% failure rate
- ✅ **Threshold**: ~150-200 lines total (docstring + code)

---

## Test Execution Instructions

1. **Delete the test file** if it exists: `rm mock_application/tests/test_complex_user_workflow.py`
2. **Attempt to CREATE** the file using Claude Code's Write tool
3. **Observe** whether TDD Guard blocks with JSON parsing error
4. **Record**: Success/Failure, error message, error position
5. **Repeat 5 times** to verify consistency (delete and recreate each time)

---

## Expected Behavior

### BEFORE Fix (Without strict-json-responses module)
- **Expected**: ~67% JSON parsing errors + ~33% TDD violations = 100% total failure rate
- **JSON Errors**: "Bad control character in string literal" or "Unterminated string in JSON"
- **Error Position**: Varies (257, 297, 307, 984, etc.) - depends on Claude's response structure
- **TDD Violations**: ~33% of attempts - Claude detects pattern violations before JSON parsing
- **Note**: Same file content produces different errors due to non-deterministic validation

### AFTER Fix (With strict-json-responses module)
- **Expected**: JSON errors reduced from ~67% to <5%
- **Realistic Success Rate**: ~60-65% (JSON errors fixed, but TDD violations still occur legitimately)
- **TDD Violations**: ~33% will still occur (this is correct TDD enforcement, not a bug)
- **Target**: 4-5 successes out of 6 attempts (vs 0/6 without fix)

---

## 🎯 TEST SCENARIO: Massive Integration Test Function

**File**: `mock_application/tests/test_complex_user_workflow.py`
**Risk Level**: CRITICAL ⚠️⚠️⚠️
**Expected Without Fix**: ~67% JSON parsing errors + ~33% TDD violations = 100% total failure rate
**File Size**: 200+ lines
**Complexity**: Maximum

### Description
A single comprehensive test function with:
- **50+ line docstring** with detailed flow explanations, database schemas, API response examples
- **150+ lines of code** with multiple database operations, validations, and assertions
- **5-7 SQL queries** (registration, verification, authentication, profile management, role assignment)
- **2-3 regex patterns** (email validation, password complexity)
- **Multiple data structures** (dictionaries, lists, JSON examples in docstring)

### File Content

```python
def test_complete_user_registration_and_authentication_workflow():
    """
    Test the complete user registration, authentication, and profile management workflow.

    This comprehensive integration test validates the entire user lifecycle from initial
    registration through authentication, profile updates, role management, and session
    handling. The test ensures all components work together correctly across multiple
    database operations, API calls, validation logic, and business rules.

    Test Flow:
    1. User Registration
       - Validate email format using regex: r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
       - Validate password complexity: uppercase, lowercase, number, special character
       - Check for duplicate email addresses in the database
       - Hash the password using bcrypt with salt rounds = 12
       - Insert user record into users table with status = 'pending'
       - Send verification email with token

    2. Email Verification
       - Validate verification token from email link
       - Update user status from 'pending' to 'active'
       - Create initial user profile with default settings

    3. User Authentication
       - Validate credentials against hashed password
       - Generate JWT token with 24-hour expiration
       - Create session record in sessions table
       - Return authentication response with user data

    4. Profile Management
       - Fetch user profile with JOIN to roles and permissions
       - Update profile information (name, bio, avatar)
       - Validate updated data against business rules

    5. Role Assignment
       - Assign roles to user (admin, editor, viewer)
       - Validate role permissions and access levels
       - Update user_roles junction table

    Expected Database Schema:
    - users: id, email, password_hash, status, created_at, updated_at
    - profiles: user_id, name, bio, avatar_url, settings (JSONB)
    - roles: id, name, permissions (ARRAY)
    - user_roles: user_id, role_id, assigned_at
    - sessions: id, user_id, token, expires_at, created_at

    Expected API Responses:
    Registration: {"status": "success", "user": {...}, "message": "Verification email sent"}
    Verification: {"status": "verified", "user": {...}}
    Login: {"status": "authenticated", "token": "jwt_token", "user": {...}}
    Profile Update: {"status": "updated", "profile": {...}}
    Role Assignment: {"status": "success", "roles": ["admin", "editor"]}
    """

    # Step 1: User Registration
    email = "newuser@example.com"
    password = "SecurePass123!@#"

    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    assert validate_email(email, email_pattern) == True, "Email format validation failed"

    # Validate password complexity
    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$'
    assert validate_password(password, password_pattern) == True, "Password complexity validation failed"

    # Check for duplicate email
    duplicate_check_query = """
        SELECT COUNT(*) as count
        FROM users
        WHERE email = %(email)s
    """
    duplicate_result = db.execute(duplicate_check_query, {"email": email})
    assert duplicate_result[0]["count"] == 0, "Email already exists"

    # Insert user with hashed password
    registration_query = """
        INSERT INTO users (email, password_hash, status, created_at, updated_at)
        VALUES (%(email)s, %(password_hash)s, 'pending', NOW(), NOW())
        RETURNING id, email, status, created_at
    """
    password_hash = hash_password_bcrypt(password, salt_rounds=12)
    user = db.execute(registration_query, {
        "email": email,
        "password_hash": password_hash
    })

    assert user[0]["id"] is not None, "User registration failed"
    assert user[0]["status"] == "pending", "User status should be pending"
    user_id = user[0]["id"]

    # Step 2: Email Verification
    verification_token = generate_verification_token(user_id)
    verify_query = """
        UPDATE users
        SET status = 'active', updated_at = NOW()
        WHERE id = %(user_id)s
        RETURNING id, email, status
    """
    verified_user = db.execute(verify_query, {"user_id": user_id})
    assert verified_user[0]["status"] == "active", "User verification failed"

    # Create initial profile
    profile_query = """
        INSERT INTO profiles (user_id, name, bio, avatar_url, settings)
        VALUES (%(user_id)s, %(name)s, %(bio)s, %(avatar)s, %(settings)s)
        RETURNING user_id, name, bio, settings
    """
    default_settings = '{"theme": "light", "notifications": true, "language": "en"}'
    profile = db.execute(profile_query, {
        "user_id": user_id,
        "name": "New User",
        "bio": "Default bio",
        "avatar": "https://example.com/default-avatar.png",
        "settings": default_settings
    })

    assert profile[0]["user_id"] == user_id, "Profile creation failed"

    # Step 3: User Authentication
    login_credentials = {"email": email, "password": password}

    # Fetch user with password hash for verification
    auth_query = """
        SELECT id, email, password_hash, status
        FROM users
        WHERE email = %(email)s AND status = 'active'
    """
    auth_user = db.execute(auth_query, {"email": email})
    assert len(auth_user) > 0, "User not found or not active"

    # Verify password
    assert verify_password(password, auth_user[0]["password_hash"]) == True, "Invalid password"

    # Generate JWT token
    jwt_token = generate_jwt_token(user_id, expiration_hours=24)

    # Create session
    session_query = """
        INSERT INTO sessions (user_id, token, expires_at, created_at)
        VALUES (%(user_id)s, %(token)s, NOW() + INTERVAL '24 hours', NOW())
        RETURNING id, user_id, token, expires_at
    """
    session = db.execute(session_query, {
        "user_id": user_id,
        "token": jwt_token
    })

    assert session[0]["token"] == jwt_token, "Session creation failed"

    # Step 4: Profile Management
    # Fetch complete user profile with roles
    profile_fetch_query = """
        SELECT
            u.id,
            u.email,
            u.status,
            p.name,
            p.bio,
            p.avatar_url,
            p.settings,
            COALESCE(json_agg(
                json_build_object(
                    'role_id', r.id,
                    'role_name', r.name,
                    'permissions', r.permissions
                )
            ) FILTER (WHERE r.id IS NOT NULL), '[]'::json) as roles
        FROM users u
        LEFT JOIN profiles p ON u.id = p.user_id
        LEFT JOIN user_roles ur ON u.id = ur.user_id
        LEFT JOIN roles r ON ur.role_id = r.id
        WHERE u.id = %(user_id)s
        GROUP BY u.id, u.email, u.status, p.name, p.bio, p.avatar_url, p.settings
    """
    complete_profile = db.execute(profile_fetch_query, {"user_id": user_id})
    assert len(complete_profile) > 0, "Profile fetch failed"

    # Update profile
    profile_update_query = """
        UPDATE profiles
        SET name = %(name)s, bio = %(bio)s, avatar_url = %(avatar)s, settings = %(settings)s
        WHERE user_id = %(user_id)s
        RETURNING user_id, name, bio, avatar_url, settings
    """
    updated_profile = db.execute(profile_update_query, {
        "user_id": user_id,
        "name": "Updated User Name",
        "bio": "Updated biography with details about the user's interests and background",
        "avatar": "https://example.com/custom-avatar.png",
        "settings": '{"theme": "dark", "notifications": false, "language": "en"}'
    })

    assert updated_profile[0]["name"] == "Updated User Name", "Profile update failed"

    # Step 5: Role Assignment
    # Fetch available roles
    roles_query = """
        SELECT id, name, permissions
        FROM roles
        WHERE name IN ('admin', 'editor', 'viewer')
    """
    available_roles = db.execute(roles_query)
    assert len(available_roles) > 0, "No roles available"

    # Assign multiple roles to user
    role_assignment_query = """
        INSERT INTO user_roles (user_id, role_id, assigned_at)
        VALUES (%(user_id)s, %(role_id)s, NOW())
        ON CONFLICT (user_id, role_id) DO NOTHING
        RETURNING user_id, role_id
    """

    for role in available_roles:
        role_assignment = db.execute(role_assignment_query, {
            "user_id": user_id,
            "role_id": role["id"]
        })

    # Verify role assignments
    verify_roles_query = """
        SELECT r.name
        FROM user_roles ur
        JOIN roles r ON ur.role_id = r.id
        WHERE ur.user_id = %(user_id)s
    """
    assigned_roles = db.execute(verify_roles_query, {"user_id": user_id})
    role_names = [role["name"] for role in assigned_roles]

    assert "admin" in role_names, "Admin role not assigned"
    assert "editor" in role_names, "Editor role not assigned"
    assert "viewer" in role_names, "Viewer role not assigned"

    # Final verification: Complete workflow success
    assert len(role_names) >= 3, "Not all roles assigned"
    print(f"✓ Complete user workflow test passed for user ID: {user_id}")
```

---

## Testing Protocol

### Phase 1: Baseline Testing (WITHOUT Module)

**Objective**: Confirm 100% failure rate

**Steps**:
1. Ensure `strict-json-responses` module is **NOT enabled** in configuration
2. Attempt to create the test file **5 times**
3. **Delete the file** between each attempt: `rm mock_application/tests/test_complex_user_workflow.py`
4. Record for each attempt:
   - ✅ Success or ❌ Failure
   - Exact error message
   - Error position (line/column from error message)
   - Any variations in error

**Expected Result**: 5/5 failures (100% failure rate)

**Documentation Template**:
```
Attempt 1/5
-----------
Module Enabled: No
Result: ❌ Failure
Error: Bad control character in string literal in JSON
Position: line 3 column 232
Notes: [observations]

Attempt 2/5
-----------
[repeat...]
```

---

### Phase 2: Validation Testing (WITH Module)

**Objective**: Verify module reduces errors to <5%

**Steps**:
1. **Enable** the `strict-json-responses` module
2. Attempt to create the **same test file** 5 times
3. Delete the file between each attempt
4. Record same data as Phase 1
5. Calculate improvement: `((5 - failures) / 5) * 100%`

**Expected Result**: 0-1 failures (0-20% failure rate, <5% target)

**Success Criteria**:
- ✅ File creates successfully in ≥4/5 attempts
- ✅ >80% reduction in failures
- ✅ Consistent behavior (not randomly passing/failing)

---

## Success Metrics

### Quantitative Target
- **Baseline (Without Module)**: 100% failure rate (5/5 failures)
- **With Module**: <5% failure rate (0/5 failures ideal, 1/5 acceptable)
- **Required Improvement**: >95% reduction in errors

### Qualitative Indicators

✅ **Module is working if:**
- Large file (200+ lines) creates successfully
- No "Bad control character in string literal" errors
- Consistent success across all retry attempts
- Error position no longer appears in messages

❌ **Module needs improvement if:**
- Still getting JSON parsing errors
- Intermittent failures (passes sometimes, fails others)
- Failure rate >20%
- Error messages unchanged from baseline

---

## Additional Validation

### Control Test: Small File (Should Always Pass)

After testing the large file, verify with a simple control:

**File**: `mock_application/tests/test_simple_control.py`
```python
def test_user_email_update():
    """Test updating user email."""
    query = "UPDATE users SET email = %(email)s WHERE id = %(id)s"
    result = db.execute(query, {"email": "test@example.com", "id": "123"})
    assert result[0]["email"] == "test@example.com"
```

**Expected Result**:
- WITHOUT module: ✅ 0/5 failures (always passes)
- WITH module: ✅ 0/5 failures (always passes)

This confirms the module doesn't break normal operation.

---

## Notes

- **Why single scenario?** This one file has proven 100% failure rate across multiple tests
- **Why 5 attempts?** Establishes consistency and statistical significance
- **Why delete between attempts?** Ensures clean test (no caching effects)
- **Error position varies**: Normal behavior - response structure changes slightly each time

---

## Next Steps After Baseline Testing

1. Document exact failure rate (should be 5/5 = 100%)
2. Enable `strict-json-responses` module
3. Re-test with same protocol
4. Calculate improvement percentage
5. If failures persist, analyze error messages for new patterns
6. If successful (<5% failure), module is validated
