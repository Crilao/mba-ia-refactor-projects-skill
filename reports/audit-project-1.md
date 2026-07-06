# Architecture Audit Report

Project: code-smells-project
Stack: Python + Flask
Files analyzed: 4
Domain: E-commerce API (produtos, usuários e pedidos)

## Summary

CRITICAL: 3 | HIGH: 2 | MEDIUM: 2 | LOW: 1

## Findings

### [CRITICAL] SQL Injection via string concatenation
File: `code-smells-project/models.py:28-29`, `47-50`, `57-61`, `68`, `89-93`, `105-110`, `122-130`, `140-166`, `174`, `188`, `192`, `206`, `220`, `280`, `289-299`
Description: Várias consultas SQL são construídas com concatenação de strings usando valores vindos da entrada da aplicação.
Impact: Um atacante pode alterar a query executada, ler dados indevidos ou corromper o banco.
Recommendation: Substituir concatenação por queries parametrizadas em todos os acessos ao banco.

### [CRITICAL] Arbitrary SQL execution endpoint
File: `code-smells-project/app.py:59-78`
Description: O endpoint `/admin/query` aceita SQL arbitrário no payload e o executa diretamente no banco.
Impact: Qualquer cliente que alcance esse endpoint pode ler, alterar ou destruir dados livremente.
Recommendation: Remover o endpoint ou restringi-lo a operações muito específicas, autenticadas e validadas.

### [CRITICAL] Plaintext password exposure
File: `code-smells-project/models.py:72-85`, `89-119`, `122-130`; `code-smells-project/controllers.py:128-162`
Description: Senhas são armazenadas em texto puro e retornadas em listagens e respostas de API.
Impact: Vazamento de credenciais e comprometimento direto das contas dos usuários.
Recommendation: Hash seguro para senhas e nunca retornar o campo `senha` nas respostas.

### [HIGH] Hardcoded secret key and debug mode
File: `code-smells-project/app.py:7-8`, `80-88`
Description: A `SECRET_KEY` está fixa no código e a aplicação sobe com `DEBUG=True`.
Impact: A configuração enfraquece a segurança e facilita abuso em ambiente exposto.
Recommendation: Mover configuração para variáveis de ambiente e desabilitar debug fora de desenvolvimento.

### [HIGH] Unprotected destructive admin endpoint
File: `code-smells-project/app.py:47-57`
Description: `/admin/reset-db` apaga todas as tabelas sem autenticação nem autorização.
Impact: Qualquer acesso ao endpoint permite perda total de dados.
Recommendation: Proteger com autenticação forte ou remover a operação da API pública.

### [MEDIUM] Order workflow without transaction boundaries
File: `code-smells-project/models.py:133-169`
Description: O fluxo de criação de pedido faz múltiplas escritas sem transação explícita ou rollback.
Impact: Falhas intermediárias podem deixar estoque, itens e pedido inconsistentes.
Recommendation: Envolver o fluxo em transação e aplicar rollback em qualquer erro.

### [MEDIUM] Repeated validation in controllers
File: `code-smells-project/controllers.py:24-58`, `64-93`, `146-183`, `188-250`
Description: As mesmas validações aparecem repetidas em vários handlers.
Impact: Regras podem divergir com o tempo e a manutenção fica mais cara.
Recommendation: Centralizar validações e regras compartilhadas em helpers ou serviços.

### [LOW] Operational logging via print
File: `code-smells-project/controllers.py:8`, `57`, `106`, `161`, `179`, `208-210`, `248-250`
Description: O projeto usa `print` como mecanismo de observabilidade.
Impact: Logs difíceis de filtrar, padronizar e correlacionar em produção.
Recommendation: Substituir por logger estruturado com níveis.

## Deprecated APIs

None detected in this project.

## Total findings

8

Proceed with refactoring? [y/n]
