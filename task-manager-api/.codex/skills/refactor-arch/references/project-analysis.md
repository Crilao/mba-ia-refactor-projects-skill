# Análise de Projeto

## Objetivo

Detectar stack, arquitetura atual, banco de dados e domínio com leitura estática do repositório.

## Ordem de inspeção

1. Leia arquivos de manifesto: `package.json`, `requirements.txt`, `pyproject.toml`, `pom.xml`, `go.mod`.
2. Localize o ponto de entrada: `app.py`, `main.py`, `server.js`, `index.js`, `src/app.js`.
3. Identifique o framework por imports e bootstrap: Flask, Express, FastAPI, Nest, etc.
4. Mapeie pastas de responsabilidade: `routes`, `controllers`, `models`, `services`, `utils`, `config`.
5. Identifique o banco e o ORM/driver: SQLite, PostgreSQL, SQLAlchemy, sqlite3, Sequelize, Knex, etc.
6. Leia endpoints e nomes de entidades para inferir o domínio funcional.

## Heurísticas

- Se o app cria o framework e registra rotas no mesmo arquivo, a arquitetura tende a ser monolítica ou mal separada.
- Se consultas SQL aparecem em handlers ou controllers, procure acoplamento entre camadas.
- Se o bootstrap contém credenciais, flags de debug ou configuração de banco, marque como risco de configuração.
- Se os dados são montados por `print`, string concatenation ou `request.body` direto no SQL, procure riscos de segurança.
- Se o projeto já tem camadas, valide se a separação é real ou só nominal.

## Sinais por stack

### Python/Flask

- `from flask import Flask, Blueprint`
- `app.route(...)`, `add_url_rule(...)`, `register_blueprint(...)`
- `flask_sqlalchemy`, `sqlite3`, `psycopg2`, `sqlalchemy`

### Node/Express

- `const express = require('express')`
- `app.use(express.json())`, `app.get/post/put/delete(...)`
- `sqlite3`, `sequelize`, `knex`, `mongoose`

## Saída esperada da Fase 1

- Linguagem e framework detectados.
- Banco e ORM/driver detectados.
- Descrição curta do domínio.
- Mapa de arquitetura atual.
- Lista do que parece violar MVC.

