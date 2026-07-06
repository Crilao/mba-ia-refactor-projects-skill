# Architecture Audit Report

Project: ecommerce-api-legacy
Stack: Node.js + Express
Files analyzed: 3
Domain: LMS API with checkout flow and financial reporting

## Summary

CRITICAL: 2 | HIGH: 3 | MEDIUM: 2 | LOW: 1

## Findings

### [CRITICAL] Hardcoded secrets and credentials
File: `ecommerce-api-legacy/src/utils.js:1-6`
Description: O arquivo expõe credenciais do banco, chave de pagamento e usuário SMTP diretamente no código.
Impact: Qualquer pessoa com acesso ao repositório obtém segredos sensíveis e pode reutilizá-los fora do sistema.
Recommendation: Remover segredos do código e ler tudo de variáveis de ambiente ou secret manager.

### [CRITICAL] Sensitive payment data is logged
File: `ecommerce-api-legacy/src/AppManager.js:45-46`
Description: O fluxo de checkout imprime o cartão e a chave do gateway de pagamento no log.
Impact: Dados de pagamento e segredos podem vazar em logs de aplicação.
Recommendation: Nunca logar dados de cartão ou chaves sensíveis; usar logs mínimos e mascarados.

### [HIGH] Weak custom password hashing
File: `ecommerce-api-legacy/src/AppManager.js:68-71`, `ecommerce-api-legacy/src/utils.js:17-22`
Description: A senha do usuário novo é passada por `badCrypto`, que gera um hash curto e previsível.
Impact: Credenciais ficam muito mais fáceis de quebrar ou reutilizar.
Recommendation: Usar um algoritmo seguro de hash de senha com salt, como bcrypt ou argon2.

### [HIGH] Destructive user deletion without authorization
File: `ecommerce-api-legacy/src/AppManager.js:131-136`
Description: O endpoint de deleção de usuário está exposto sem qualquer controle de autenticação ou autorização.
Impact: Qualquer cliente pode remover usuários da aplicação.
Recommendation: Proteger ações destrutivas com autenticação e autorização adequadas.

### [HIGH] In-memory database resets state on reboot
File: `ecommerce-api-legacy/src/AppManager.js:7`, `10-22`
Description: O banco é criado em memória e os seeds são reaplicados a cada boot.
Impact: O sistema perde estado ao reiniciar e não se comporta como uma aplicação persistente.
Recommendation: Migrar para um banco persistente e separar o seed da inicialização normal.

### [MEDIUM] God object concentrates route, persistence and business logic
File: `ecommerce-api-legacy/src/AppManager.js:4-138`
Description: A classe `AppManager` mistura criação de schema, seed, rotas HTTP e regras de negócio.
Impact: A manutenção e os testes ficam difíceis, e o projeto não segue MVC de forma clara.
Recommendation: Separar controller, service e access layer em módulos menores.

### [MEDIUM] Financial report uses deeply nested callbacks
File: `ecommerce-api-legacy/src/AppManager.js:80-129`
Description: O relatório financeiro é montado com várias camadas de callbacks aninhados e múltiplas consultas por curso e matrícula.
Impact: O código fica difícil de ler e tende a crescer mal em performance.
Recommendation: Extrair o relatório para um serviço com consultas mais diretas e fluxo mais linear.

### [LOW] Global mutable state and dead export
File: `ecommerce-api-legacy/src/utils.js:9-10`, `25`
Description: `globalCache` e `totalRevenue` são globais mutáveis, e `totalRevenue` não é usado.
Impact: Aumenta acoplamento implícito e polui o módulo com código morto.
Recommendation: Encapsular estado em um serviço e remover exports não utilizados.

## Deprecated APIs

None detected in this project.

## Total findings

8

Proceed with refactoring? [y/n]
