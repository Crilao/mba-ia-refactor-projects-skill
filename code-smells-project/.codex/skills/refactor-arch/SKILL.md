---
name: refactor-arch
description: Audite e refatore codebases legadas para MVC em três fases. Use quando precisar detectar stack, arquitetura, anti-patterns, linhas exatas de problemas, gerar relatório de auditoria ou reestruturar backends em Python/Flask, Node/Express ou stacks semelhantes.
---

# Refactor Arch

## Visão geral

Use esta skill para inspecionar uma codebase legada, produzir uma auditoria reproduzível e depois refatorar o projeto para um MVC mais limpo sem quebrar o comportamento existente.

## Fases

### Fase 1 - Análise

1. Identifique linguagem, framework, banco, ponto de entrada e domínio da aplicação.
2. Mapeie a arquitetura atual: rotas, controllers, models, serviços, utilitários e acoplamentos.
3. Registre o resumo antes de editar qualquer arquivo.
4. Consulte [project-analysis.md](references/project-analysis.md) para heurísticas e sinais.

### Fase 2 - Auditoria

1. Cruze o código com [anti-pattern-catalog.md](references/anti-pattern-catalog.md).
2. Classifique cada finding com severidade, arquivo e linhas exatas.
3. Gere o relatório seguindo [audit-report-template.md](references/audit-report-template.md).
4. Pare e peça confirmação explícita antes de alterar qualquer arquivo.

### Fase 3 - Refatoração

1. Use [mvc-guidelines.md](references/mvc-guidelines.md) como alvo estrutural.
2. Aplique as transformações do [refactor-playbook.md](references/refactor-playbook.md).
3. Preserve endpoints e comportamento observável sempre que possível.
4. Valide boot da aplicação e os endpoints principais após as mudanças.

## Regras de decisão

- Priorize findings que afetem segurança, integridade, autenticação, dados sensíveis ou execução arbitrária.
- Se houver dúvida entre duas severidades, escolha a mais alta quando houver risco de vazamento, corrupção de dados ou compromisso de acesso.
- Não refatore sem evidência concreta. Se o problema parecer possível, confirme no código antes de registrar no relatório.
- Não misture relatório e refatoração. A Fase 2 deve terminar antes de qualquer edição.

## Quando ler os recursos

- Leia `references/project-analysis.md` no início de qualquer projeto novo.
- Leia `references/anti-pattern-catalog.md` para classificar severidade e sinais de detecção.
- Leia `references/audit-report-template.md` para padronizar a saída da Fase 2.
- Leia `references/mvc-guidelines.md` antes de mover código entre camadas.
- Leia `references/refactor-playbook.md` quando precisar transformar um smell específico em código MVC.

