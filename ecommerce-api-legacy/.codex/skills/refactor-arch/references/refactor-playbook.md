# Playbook de Refatoração

## Sumário

1. [SQL concatenado](#sql-concatenado)
2. [Config hardcoded](#config-hardcoded)
3. [Controller gordo](#controller-gordo)
4. [Senha fraca ou exposta](#senha-fraca-ou-exposta)
5. [Validação duplicada](#validacao-duplicada)
6. [N+1 queries](#n1-queries)
7. [Estado global mutável](#estado-global-mutavel)
8. [Endpoint destrutivo sem proteção](#endpoint-destrutivo-sem-protecao)
9. [API depreciada](#api-depreciada)

## SQL concatenado

Antes:

```py
cursor.execute("SELECT * FROM users WHERE email = '" + email + "'")
```

Depois:

```py
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
```

## Config hardcoded

Antes:

```js
const port = 3000;
const secret = "hardcoded";
```

Depois:

```js
const port = Number(process.env.PORT ?? 3000);
const secret = process.env.SECRET_KEY;
```

## Controller gordo

Antes:

```py
@bp.post("/tasks")
def create():
    data = request.get_json()
    # validação, regra, persistência, resposta
```

Depois:

```py
@bp.post("/tasks")
def create():
    task = task_controller.create(request.get_json())
    return jsonify(task), 201
```

## Senha fraca ou exposta

Antes:

```py
user.password = password
return user.to_dict()
```

Depois:

```py
user.password = generate_password_hash(password)
data = user.to_dict()
data.pop("password", None)
return data
```

## Validação duplicada

Antes:

```py
if not title or len(title) < 3:
    return error("Título inválido")
if not description:
    description = ""
```

Depois:

```py
payload, error = validate_task_payload(request.get_json())
if error:
    return jsonify({"error": error}), 400
```

## N+1 queries

Antes:

```py
for task in tasks:
    user = User.query.get(task.user_id)
```

Depois:

```py
tasks = Task.query.options(joinedload(Task.user)).all()
```

## Estado global mutável

Antes:

```js
let cache = {};
cache[key] = value;
```

Depois:

```js
const cacheStore = new CacheStore();
cacheStore.set(key, value);
```

## Endpoint destrutivo sem proteção

Antes:

```py
@app.delete("/users/<int:id>")
def delete_user(id):
    ...
```

Depois:

```py
@admin_required
@app.delete("/users/<int:id>")
def delete_user(id):
    ...
```

## API depreciada

Antes:

```py
user = User.query.get(user_id)
```

Depois:

```py
user = db.session.get(User, user_id)
```

## Como aplicar o playbook

- Corrigir a causa raiz, não só o sintoma.
- Preservar contratos públicos.
- Refatorar em pequenos passos verificáveis.
- Validar cada mudança com boot e endpoints principais.

