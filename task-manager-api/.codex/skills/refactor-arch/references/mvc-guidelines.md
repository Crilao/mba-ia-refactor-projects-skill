# Guidelines de Arquitetura MVC

## Estrutura alvo

```text
src/
  config/
  models/
  controllers/
  views/ or routes/
  middlewares/
  services/        # opcional, apenas para lógica de apoio
  app.py or app.js # composition root
```

## Responsabilidades

### Models

- Acessar dados.
- Encapsular queries, persistência e regras de domínio simples.
- Não conhecer HTTP.

### Controllers

- Orquestrar o fluxo.
- Validar entrada superficialmente.
- Chamar models/services.
- Não montar SQL bruto nem conter bootstrap do app.

### Views / Routes

- Expor HTTP.
- Traduzir request/response.
- Não conter regra de negócio pesada.

### Config

- Centralizar ambiente, portas, chaves, DB, flags e defaults.
- Ler de `.env` ou variáveis de ambiente.

### Middlewares

- Autenticação, autorização, erro global, logging e cross-cutting concerns.

## Regras práticas

- Manter os handlers finos.
- Extrair regras repetidas para helpers ou services.
- Remover segredos do código.
- Não deixar o bootstrap acumular regras de negócio.
- Preservar contratos de endpoint sempre que possível.

