# Logs Directory

Este diretório armazena os logs da aplicação, organizados para facilitar o monitoramento, análise e depuração do sistema.

## Estrutura de Logs

- **execution_logs/**: Logs de execução normal do sistema
  - Registra o fluxo de processamento
  - Contém informações sobre início e término de cada etapa
  - Formato: `execution_YYYY-MM-DD.log`

- **error_logs/**: Logs de erros e exceções
  - Registra exceções e falhas do sistema
  - Inclui rastreamento completo de erros (stack traces)
  - Formato: `error_YYYY-MM-DD.log`

- **data_logs/**: Logs de processamento de dados
  - Registra operações de transformação de dados
  - Contém estatísticas de processamento (registros processados, filtrados, etc.)
  - Formato: `data_YYYY-MM-DD.log`

## Níveis de Log

Os logs são categorizados nos seguintes níveis:

- **INFO**: Informações gerais sobre o funcionamento normal
- **WARNING**: Alertas sobre situações potencialmente problemáticas
- **ERROR**: Erros que afetam uma operação específica
- **CRITICAL**: Erros graves que podem comprometer o sistema

## Formato de Log

Cada entrada de log segue o formato:

```
[TIMESTAMP] [LEVEL] [MODULE] - Mensagem
```

Exemplo:
```
[2023-05-15 14:32:45] [INFO] [data_processing] - Processamento da tabela 'caracteristicas_fundo' iniciado
```

## Retenção de Logs

Os arquivos de log são mantidos por 90 dias, após os quais são automaticamente arquivados.