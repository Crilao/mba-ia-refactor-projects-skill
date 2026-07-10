# Refactor Playbook

## Summary

1. SQL concatenation
2. Hardcoded config
3. Sensitive data in logs
4. Weak or exposed password handling
5. Duplicated validation
6. N+1 queries
7. Mutable global state
8. Destructive endpoint without protection
9. Deprecated API usage

## SQL concatenation

Before:

```py
cursor.execute("SELECT * FROM users WHERE email = '" + email + "'")
```

After:

```py
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
```

## Hardcoded config

Before:

```js
const port = 3000;
const secret = "hardcoded";
```

After:

```js
const port = Number(process.env.PORT ?? 3000);
const secret = process.env.SECRET_KEY;
```

## Sensitive data in logs

Before:

```js
console.log(`Processing card ${card} with gateway key ${gatewayKey}`);
```

After:

```js
console.info('Checkout in progress', {
  userId,
  courseId,
});
```

- Never log card numbers, passwords, tokens, gateway keys, or plaintext credentials.
- If context is required, log only non-sensitive metadata and mask values when needed.

## Weak or exposed password handling

Before:

```py
user.password = password
return user.to_dict()
```

After:

```py
user.password = generate_password_hash(password)
data = user.to_dict()
data.pop("password", None)
return data
```

Node.js example:

```js
const bcrypt = require('bcryptjs');
const hash = await bcrypt.hash(password, 12);
```

If the project already uses `argon2`, prefer `argon2.hash(password)` and `argon2.verify(hash, password)`.

- Never keep `badCrypto`, MD5, SHA1, or homegrown password hashing.
- Every password creation or update must use a secure salted hash.

## Duplicated validation

Before:

```py
if not title or len(title) < 3:
    return error("Invalid title")
if not description:
    description = ""
```

After:

```py
payload, error = validate_task_payload(request.get_json())
if error:
    return jsonify({"error": error}), 400
```

## N+1 queries

Before:

```py
for task in tasks:
    user = User.query.get(task.user_id)
```

After:

```py
tasks = Task.query.options(joinedload(Task.user)).all()
```

## Mutable global state

Before:

```js
let cache = {};
cache[key] = value;
```

After:

```js
const cacheStore = new CacheStore();
cacheStore.set(key, value);
```

## Destructive endpoint without protection

Before:

```py
@app.delete("/users/<int:id>")
def delete_user(id):
    ...
```

After:

```py
@admin_required
@app.delete("/users/<int:id>")
def delete_user(id):
    ...
```

## Deprecated API usage

Before:

```py
user = User.query.get(user_id)
```

After:

```py
user = db.session.get(User, user_id)
```

## How to apply the playbook

- Fix the root cause, not just the symptom.
- Preserve public contracts.
- Refactor in small verifiable steps.
- Validate each change with boot and the main endpoints.
- If Phase 2 found a smell, Phase 3 must apply the matching transformation before any cosmetic cleanup.
- Re-run the audit after each change set to confirm critical findings are gone.
