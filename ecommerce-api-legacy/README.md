# ecommerce-api-legacy

LMS API (com fluxo de checkout) em Node.js/Express usada como entrada do desafio `refactor-arch`.

## Como rodar

```bash
npm install
SEED_USER_PASSWORD="uma-senha-forte" npm run seed
ADMIN_TOKEN="admin-token-seguro" npm start
```

A aplicação sobe em `http://localhost:3000`. Por padrão, o banco SQLite é persistido em `data/ecommerce.sqlite`; altere o caminho com `DATABASE_PATH`. O seed é uma operação explícita e requer `SEED_USER_PASSWORD` para não gravar uma senha padrão no código.

Os endpoints administrativos exigem `Authorization: Bearer <ADMIN_TOKEN>`.

Exemplos de requisições estão em `api.http`.

