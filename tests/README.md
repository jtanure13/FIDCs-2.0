# Testes do Sistema de Coleta e Processamento de FIDCs

Este diretório contém os testes automatizados do sistema, organizados para facilitar a manutenção, permitir a adição de novos testes e garantir a qualidade do código.

## Conceitos de Testes

### Testes Unitários

Os testes unitários são focados em validar o comportamento de componentes individuais do código (funções, métodos, classes) de forma isolada. Estes testes garantem que cada parte do sistema funcione corretamente quando testada separadamente.

**Características principais:**
- Execução rápida
- Isolamento de dependências externas através de mocks
- Cobertura específica de um componente por vez
- Facilidade para detectar regressões

### Testes de Integração

Os testes de integração verificam se componentes diferentes do sistema funcionam corretamente quando combinados. Estes testes são importantes para garantir que a comunicação entre diferentes partes do código ocorra como esperado.

**Características principais:**
- Validação da interação entre componentes
- Identificação de problemas de comunicação entre módulos
- Detecção de erros que não aparecem em testes unitários isolados

### Mocks e Fixtures

- **Mocks**: São objetos simulados que substituem componentes reais durante os testes, permitindo controlar seu comportamento e isolar o código sendo testado.
- **Fixtures**: São recursos ou dados compartilhados que podem ser reutilizados entre diferentes testes, melhorando a eficiência e reduzindo a duplicação de código.

### TDD (Test-Driven Development)

TDD é uma metodologia de desenvolvimento onde os testes são escritos antes do código de implementação. Segue o ciclo:
1. Escrever um teste que falha
2. Implementar o código mínimo para passar no teste
3. Refatorar o código mantendo os testes passando

## Estrutura dos Testes

A estrutura de testes é organizada da seguinte forma:

```
tests/
├── __init__.py                 # Inicialização do pacote de testes
├── README.md                   # Este arquivo de documentação
├── conftest.py                 # Fixtures compartilhadas por todos os testes
├── run_tests.py                # Script para executar todos os testes
├── fixtures/                   # Dados e objetos reutilizáveis para testes
│   ├── __init__.py             # Inicialização do pacote de fixtures
│   ├── sample_data.py          # Dados de exemplo para testes
│   └── mock_responses.py       # Respostas simuladas para APIs
├── integration/                # Testes de integração
│   ├── __init__.py             # Inicialização do pacote de testes de integração
│   └── test_integration.py     # Testes de integração entre componentes
├── test_logger.py              # Testes unitários para o Logger
├── test_scraper.py             # Testes unitários para o CvmScraper
├── test_collector.py           # Testes unitários para o CvmDataCollector
├── test_processor.py           # Testes unitários para o DataProcessor
├── test_database.py            # Testes unitários para o DatabaseHandler
└── test_pipeline.py            # Testes unitários para o Pipeline
```

## Testes Implementados

### Logger (test_logger.py)
- Inicialização correta
- Criação de arquivos de log
- Formatos de mensagens
- Níveis de log
- Tratamento de exceções

### Scraper (test_scraper.py)
- Download e extração de arquivos CSV
- Manipulação de erros de conexão
- Importação de dados para múltiplos meses
- Tratamento de casos específicos (sem dados, erros parciais)

### Collector (test_collector.py)
- Inicialização com configurações
- Coleta de dados de diferentes tabelas
- Tratamento de erros de download
- Processamento de intervalos de datas
- Logs adequados em diferentes cenários

### Processor (test_processor.py)
- Remoção de registros duplicados
- Conversão de datas em diferentes formatos
- Conversão de tipos numéricos (inteiros e decimais)
- Processamento completo com tratamento de erros

### Database (test_database.py)
- Criação e atualização de tabelas
- Detecção automática de tipos de colunas
- Manipulação de dados (inserção e deleção)
- Transações seguras

### Pipeline (test_pipeline.py)
- Integração entre componentes
- Sequência de processamento
- Tratamento de erros em diferentes estágios
- Exportação de dados em diferentes formatos

### Integração (integration/test_integration.py)
- Fluxo completo do sistema
- Interação entre componentes reais
- Validação de resultados persistidos

## Como Executar os Testes

### Requisitos
- Python 3.6+
- pytest
- pytest-cov (para relatórios de cobertura)

### Instalação das Dependências
```
pip install pytest pytest-cov
```

### Executando Todos os Testes
Para executar todos os testes com geração de relatório de cobertura:

```
python -m tests.run_tests
```

Ou diretamente com pytest:

```
pytest tests/ -v --cov=src
```

### Executando Testes Específicos
Para executar apenas testes unitários:

```
pytest tests/test_*.py -v
```

Para executar apenas testes de integração:

```
pytest tests/integration/ -v
```

Para executar um arquivo de teste específico:

```
pytest tests/test_scraper.py -v
```

## Relatórios de Cobertura

Os relatórios de cobertura mostram quais partes do código foram executadas durante os testes. Isto ajuda a identificar áreas que precisam de mais testes.

Ao executar `python -m tests.run_tests`, os seguintes relatórios são gerados:
- Relatório no terminal (texto)
- Relatório HTML detalhado em `tests/coverage_html/`

## Diretrizes para Escrever Novos Testes

1. **Nomeação clara**: Use nomes descritivos para testes (`test_funcionalidade_cenario`)
2. **Um assert por teste**: Quando possível, mantenha um único assert por teste
3. **Docstrings**: Adicione descrições úteis para cada método de teste
4. **Isolamento**: Use mocks para isolar o código sendo testado
5. **Organização**: Mantenha a estrutura de testes consistente
6. **Cobertura**: Procure cobrir casos de sucesso e falha
7. **Setups/Teardowns**: Use `setUp` e `tearDown` para preparar e limpar recursos

## Contribuindo com Testes

Ao desenvolver novas funcionalidades:
1. Crie testes unitários para cada novo componente
2. Atualize ou crie testes de integração se necessário
3. Verifique se a cobertura de código é mantida ou melhorada
4. Execute todos os testes para garantir que não há regressões