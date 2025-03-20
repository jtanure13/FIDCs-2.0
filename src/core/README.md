# Módulos Core

Esta pasta contém os componentes principais do sistema de coleta e processamento de FIDCs.

## Componentes

- **collector.py**: Implementa a classe `CvmDataCollector` responsável pela coleta de dados da CVM.
  
- **database.py**: Contém a classe `DatabaseHandler` que gerencia todas as operações de banco de dados, como criação de tabelas e inserção/atualização de dados.
  
- **logger.py**: Implementa a classe `Logger` que configura o sistema de logging com três tipos de logs (execução, erros e dados).
  
- **pipeline.py**: Contém a classe `FidcPipeline`, o componente principal que orquestra todo o fluxo de processamento.
  
- **processor.py**: Implementa a classe `DataProcessor` responsável pelo processamento, limpeza e tratamento de duplicatas nos dados.
  
- **scraper.py**: Contém a classe `CvmScraper` que realiza o web scraping e download dos dados da CVM.

## Fluxo de Dados

1. O `FidcPipeline` inicia o processo de coleta para cada tabela configurada
2. O `CvmDataCollector` utiliza o `CvmScraper` para baixar os dados
3. Os dados coletados são enviados para o `DataProcessor` para limpeza
4. O `DatabaseHandler` armazena os dados processados no banco de dados
5. Todo o processo é registrado pelo `Logger` 