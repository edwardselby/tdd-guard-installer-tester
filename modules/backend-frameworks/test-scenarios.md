# Backend Framework Test Scenarios

## Phase 6: Backend Framework Intelligence

### Test 6.1: Flask Route Definitions ✅
```python
@app.route('/api/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'POST':
        return create_user(request.json)
    return get_users()
```
**Expected**: Should ALLOW - legitimate Flask pattern

### Test 6.2: FastAPI Patterns ✅
```python
@router.get("/items/{item_id}")
async def read_item(item_id: int):
    return await get_item_from_database(item_id)
```
**Expected**: Should ALLOW - legitimate FastAPI pattern

### Test 6.3: Database Operations ✅
```python
def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()
```
**Expected**: Should ALLOW - real database query

### Test 6.4: Fake Backend Response ❌
```python
@app.route('/api/users')
def get_users():
    return {"users": [{"id": 1, "name": "Test User"}]}  # Hardcoded response
```
**Expected**: Block with fake implementation in backend context

### Test 6.5: Legitimate Backend Framework Patterns ✅
```python
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200
```
**Expected**: Should ALLOW - proper health check endpoint

### Test 6.6: Django Model Operations ✅
```python
def find_active_users_by_role(role, limit=50):
    return User.objects.filter(
        role=role,
        is_active=True,
        last_login__gte=timezone.now() - timedelta(days=30)
    ).order_by('-last_login')[:limit]
```
**Expected**: Should ALLOW - realistic database operation

## Success Criteria
- ✅ Allow legitimate Flask/FastAPI/Django patterns (6 scenarios)
- ✅ Allow proper database operations and framework-specific code
- ❌ Still block fake backend responses with hardcoded data (1 scenario)
- **Framework Aware**: Distinguishes between real framework usage and fake implementations