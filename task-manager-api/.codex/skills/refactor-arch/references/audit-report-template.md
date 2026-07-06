# Template de Relatório de Auditoria

## Cabeçalho

```md
# Architecture Audit Report

Project: <nome-do-projeto>
Stack: <linguagem + framework>
Files analyzed: <n>
Lines analyzed: <aprox.>
Domain: <domínio inferido>
```

## Resumo executivo

```md
## Summary
CRITICAL: <n> | HIGH: <n> | MEDIUM: <n> | LOW: <n>
```

## Findings

Use uma tabela ou lista por finding. Ordem obrigatória: CRITICAL -> HIGH -> MEDIUM -> LOW.

```md
### [CRITICAL] <título curto>
File: path/file.ext:10-24
Description: <o que acontece>
Impact: <consequência prática>
Recommendation: <como corrigir>
```

## Seção obrigatória para APIs depreciadas

```md
### [MEDIUM] Deprecated API Usage
File: path/file.ext:12
Description: <API antiga encontrada>
Modern equivalent: <substituição recomendada>
```

## Encerramento

```md
Total findings: <n>
Proceed with refactoring? [y/n]
```

## Regras

- Nunca omitir arquivo e linha.
- Nunca agrupar findings com causas diferentes em um único item.
- Nunca misturar recomendações de refatoração com o relatório da Fase 2.
- Se não houver evidência suficiente, não registrar o finding.

