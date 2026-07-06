# Catálogo de Anti-patterns

## Regra

Cada finding deve ter:

- severidade
- arquivo
- linhas exatas
- evidência concreta
- impacto
- recomendação

## Catálogo mínimo

| Anti-pattern | Severidade | Sinais de detecção | Modernização/Recomendação |
|---|---|---|---|
| SQL Injection por concatenação | CRITICAL | `"... " + value`, `f"...{value}..."` em SQL | Usar queries parametrizadas / ORM seguro |
| Segredo ou credencial hardcoded | CRITICAL | `SECRET_KEY`, `password`, `api_key`, `dbPass` no código | Ler de variáveis de ambiente ou secret manager |
| Execução arbitrária de SQL/command | CRITICAL | endpoints que aceitam SQL, `eval`, `exec`, shell dinâmico | Remover a superfície e expor operações fechadas |
| Senha em texto puro ou hash fraco | HIGH | `md5`, `sha1`, retorno de senha na API | `bcrypt`, `argon2`, `generate_password_hash` |
| Controller gordo / God Class | HIGH | classe/arquivo concentra bootstrap, regra, persistência e HTTP | Separar controller, model, service e config |
| Sem autenticação/autorização em ações destrutivas | HIGH | `DELETE`, `PUT`, admin endpoints sem middleware | Adicionar auth middleware e checagem de papel |
| Estado global mutável | HIGH | variáveis globais para cache, sessão, configuração viva | Injeção de dependência / armazenamento por request |
| N+1 queries | MEDIUM | consultas dentro de loops sobre entidades | `JOIN`, eager loading, batch fetch |
| Validação duplicada ou espalhada | MEDIUM | `if` repetidos em vários handlers | Centralizar validação em helpers/schemas |
| API depreciada/legada | MEDIUM | uso de métodos marcados como legacy/deprecated | Trocar pela API moderna documentada |
| Logging por `print` em produção | LOW | `print()` para rastreamento operacional | Usar logger estruturado com níveis |
| Imports mortos / código não usado | LOW | imports sem uso, variáveis exportadas sem consumo | Remover ou consolidar |

## APIs depreciadas: exemplos a procurar

- `Query.get()` no SQLAlchemy: preferir `Session.get(Model, id)`.
- `datetime.utcnow()` quando o projeto já usa timestamps com fuso: preferir `datetime.now(timezone.utc)`.
- `new Buffer()` no Node: preferir `Buffer.from()`.
- APIs de framework marcadas como legacy no release atual: trocá-las pela alternativa documentada mais nova.

## Regra prática

Se a API é antiga, mas ainda funciona, marque como **MEDIUM**. Se a API antiga também expõe dados, fragiliza segurança ou quebra compatibilidade, eleve para **HIGH**.

