# Architecture Audit Report

Project: task-manager-api
Stack: Python + Flask
Files analyzed: 10
Domain: Task management API with users, tasks, categories and reports

## Summary

CRITICAL: 0 | HIGH: 4 | MEDIUM: 3 | LOW: 2

## Findings

### [HIGH] Passwords use weak hashing and are exposed in API responses
File: `task-manager-api/models/user.py:16-32`, `task-manager-api/routes/user_routes.py:33-38`, `207-210`
Description: O modelo de usuário devolve o campo `password` em `to_dict` e usa MD5 para hash de senha.
Impact: Credenciais podem vazar pela API e o armazenamento de senha fica fácil de quebrar.
Recommendation: Usar hash seguro com salt e nunca serializar a senha nas respostas.

### [HIGH] No authentication or authorization on destructive endpoints
File: `task-manager-api/routes/user_routes.py:134-151`, `task-manager-api/routes/task_routes.py:225-238`, `task-manager-api/routes/report_routes.py:190-223`
Description: Endpoints de exclusão e alteração administrativa não têm proteção de acesso.
Impact: Qualquer cliente consegue apagar usuários, tasks e categorias.
Recommendation: Proteger ações destrutivas com autenticação e autorização.

### [HIGH] Hardcoded secret key and debug mode
File: `task-manager-api/app.py:11-13`, `33-34`
Description: A aplicação define `SECRET_KEY` fixa no código e sobe com `debug=True`.
Impact: A configuração fragiliza o ambiente e expõe detalhes de execução.
Recommendation: Ler configuração de variáveis de ambiente e desligar debug fora de desenvolvimento.

### [HIGH] Hardcoded SMTP credentials in notification service
File: `task-manager-api/services/notification_service.py:4-18`
Description: O serviço de notificação embute host, usuário e senha de email diretamente no código.
Impact: Segredos de envio de email ficam expostos e difíceis de trocar por ambiente.
Recommendation: Externalizar credenciais e usar configuração por ambiente.

### [MEDIUM] Overdue logic duplicated across multiple layers
File: `task-manager-api/models/task.py:50-60`, `task-manager-api/routes/user_routes.py:171-180`, `task-manager-api/routes/task_routes.py:30-39`, `71-80`, `task-manager-api/routes/report_routes.py:33-43`, `132-136`
Description: A mesma regra de task atrasada aparece repetida em model, routes e relatórios.
Impact: A manutenção fica cara e a regra pode divergir com o tempo.
Recommendation: Centralizar a lógica de overdue em helper ou método único.

### [MEDIUM] N+1 query patterns in listings and reports
File: `task-manager-api/routes/task_routes.py:14-58`, `task-manager-api/routes/report_routes.py:53-68`, `157-164`
Description: Listagens e relatórios fazem consultas extras dentro de loops.
Impact: A performance degrada conforme os dados crescem.
Recommendation: Reduzir consultas repetidas com eager loading ou agregações.

### [MEDIUM] Boot-time schema creation without migrations
File: `task-manager-api/app.py:30-31`
Description: O schema é criado automaticamente no boot com `db.create_all()`.
Impact: Evolução de banco fica sem controle explícito.
Recommendation: Adotar migrações ou, no mínimo, separar inicialização de esquema do boot normal.

### [LOW] Excess imports and unused utilities
File: `task-manager-api/app.py:7`, `models/task.py:1-3`, `routes/task_routes.py:7`, `utils/helpers.py:3-7`
Description: Há imports e utilitários não utilizados no código atual.
Impact: Polui o projeto e aumenta ruído de manutenção.
Recommendation: Remover imports mortos e consolidar utilitários.

### [LOW] Service has state and dead code
File: `task-manager-api/services/notification_service.py:5-6`, `43-48`
Description: O serviço mantém estado em memória e a lista de notificações não é persistida.
Impact: O comportamento fica limitado ao processo atual e difícil de testar.
Recommendation: Externalizar o estado ou deixar claro que é apenas cache temporário.

## Deprecated APIs

### [MEDIUM] SQLAlchemy legacy query helpers
File: `task-manager-api/routes/user_routes.py:29`, `94`, `136`, `155`; `task-manager-api/routes/task_routes.py:67`, `117`, `158`, `188`, `227`; `task-manager-api/routes/report_routes.py:105`, `159`, `192`, `213`
Description: O código usa `Model.query.get(...)`, que é uma forma legada no SQLAlchemy atual.
Modern equivalent: `db.session.get(Model, id)`

## Total findings

9

Proceed with refactoring? [y/n]
