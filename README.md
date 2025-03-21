# Sistema de Coleta e Processamento de Dados de FIDCs

## Índice
1. [Introdução](#introdução)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Componentes Principais](#componentes-principais)
   - [Logger](#logger)
   - [Scraper](#scraper)
   - [Collector](#collector)
   - [Processor](#processor)
   - [Database](#database)
   - [Pipeline](#pipeline)
5. [Fluxo de Processamento](#fluxo-de-processamento)
6. [Configuração](#configuração)
7. [Logs](#logs)
8. [Testes](#testes)
9. [Implantação](#implantação)
10. [Uso](#uso)
11. [Contribuição](#contribuição)

## Introdução

Este projeto implementa um sistema completo para coleta, processamento e armazenamento de dados de Fundos de Investimento em Direitos Creditórios (FIDCs) da CVM (Comissão de Valores Mobiliários). O sistema realiza web scraping nos dados públicos da CVM, processa as informações coletadas e as armazena em um banco de dados estruturado para posterior análise.

### Objetivo

O principal objetivo é criar uma base de dados estruturada contendo informações históricas e atualizadas sobre FIDCs, permitindo análises detalhadas do mercado brasileiro de securitização de recebíveis. Os dados coletados incluem informações sobre patrimônio líquido, cotistas, inadimplência, carteira de ativos, rentabilidade, entre outros.

### Características Principais

- **Automatização Completa**: Download, extração, processamento e armazenamento automatizados
- **Processamento Robusto**: Tratamento de dados inconsistentes, duplicatas e formatos variados
- **Modularidade**: Componentes independentes e facilmente extensíveis
- **Escalabilidade**: Capacidade de lidar com grandes volumes de dados
- **Resiliência**: Tratamento robusto de erros, retentativas e rollbacks em caso de falha
- **Rastreabilidade**: Sistema completo de logging para auditoria e diagnóstico

## Arquitetura do Sistema

O sistema segue uma arquitetura modular de camadas, onde cada componente tem responsabilidades específicas e bem definidas:

```
┌─────────────────────────────────────────────────────────────┐
│                      FidcPipeline                           │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                      CvmDataCollector                       │
└───────────────┬─────────────────────────────┬───────────────┘
                │                             │
                ▼                             ▼
┌───────────────────────────┐   ┌───────────────────────────┐
│        CvmScraper         │   │      DataProcessor        │
└───────────────────────────┘   └─────────────┬─────────────┘
                                              │
                                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      DatabaseHandler                        │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                     Banco de Dados                          │
└─────────────────────────────────────────────────────────────┘
```

**Fluxo de Dados:**
1. O `FidcPipeline` controla todo o processo e inicia a coleta de dados
2. O `CvmDataCollector` utiliza o `CvmScraper` para baixar os dados da CVM
3. Os dados são enviados para o `DataProcessor` para limpeza e transformação
4. O `DatabaseHandler` armazena os dados processados no banco de dados
5. O sistema de `Logger` registra todas as operações durante o processo

## Estrutura do Projeto

```
FIDCs/
├── config/                     # Configurações do sistema
│   ├── __init__.py
│   └── tables.py               # Definição das tabelas e campos a coletar
├── data/                       # Diretório para armazenamento temporário
│   └── meta_txt/               # Metadados e descrição dos campos
│       ├── carteira_ativos.txt
│       ├── cedentes_tomadores.txt
│       ├── inadimplencia.txt
│       └── ...
├── logs/                       # Logs do sistema
│   ├── error/                  # Logs de erros
│   ├── data/                   # Logs de dados
│   └── exec/                   # Logs de execução
├── src/                        # Código-fonte
│   ├── __init__.py
│   └── core/                   # Módulos principais
│       ├── __init__.py
│       ├── collector.py        # Implementação do CvmDataCollector
│       ├── database.py         # Implementação do DatabaseHandler
│       ├── logger.py           # Sistema de logging
│       ├── pipeline.py         # Orquestrador principal
│       ├── processor.py        # Processamento de dados
│       ├── scraper.py          # Scraping da web
│       └── README.md           # Documentação dos componentes
├── tests/                      # Testes automatizados
│   ├── __init__.py
│   ├── README.md               # Documentação dos testes
│   ├── conftest.py             # Configurações compartilhadas de testes
│   ├── run_tests.py            # Script para executar testes
│   ├── fixtures/               # Dados para testes
│   │   ├── __init__.py
│   │   ├── sample_data.py      
│   │   └── mock_responses.py   
│   ├── integration/            # Testes de integração
│   │   ├── __init__.py
│   │   └── test_integration.py
│   ├── test_collector.py       # Testes do CvmDataCollector
│   ├── test_database.py        # Testes do DatabaseHandler
│   ├── test_logger.py          # Testes do Logger
│   ├── test_pipeline.py        # Testes do Pipeline
│   ├── test_processor.py       # Testes do DataProcessor
│   └── test_scraper.py         # Testes do CvmScraper
├── backup/                     # Backup de dados processados
├── duplicatas/                 # Registros de duplicatas identificadas
├── __pycache__/                # Arquivos de cache Python
├── main.py                     # Ponto de entrada da aplicação
├── pytest.ini                  # Configuração do pytest
├── requirements.txt            # Dependências de produção
└── requirements-dev.txt        # Dependências de desenvolvimento
```

## Componentes Principais

### Logger

O componente `Logger` implementa um sistema abrangente de logging para rastrear todos os aspectos da operação do sistema.

**Recursos Principais:**
- Três tipos de logs separados: execução, erros e dados
- Rotação automática de logs por tamanho e data
- Formatação personalizada para cada tipo de log
- Níveis configuráveis de verbosidade

**Implementação:**
```python
class Logger:
    def __init__(self, log_dir='logs'):
        self.log_dir = log_dir
        self._setup_log_dirs()
        self._setup_loggers()
        
    def _setup_log_dirs(self):
        # Cria diretórios de log se não existirem
        
    def _setup_loggers(self):
        # Configura loggers para execução, erros e dados
        
    def get_exec_logger(self):
        # Retorna logger para operações de execução
        
    def get_error_logger(self):
        # Retorna logger para erros
        
    def get_data_logger(self):
        # Retorna logger para operações de dados
```

### Scraper

O componente `CvmScraper` é responsável por baixar e extrair os dados da CVM.

**Recursos Principais:**
- Download de arquivos ZIP da CVM
- Extração de arquivos CSV
- Tratamento de erros de rede e arquivos corrompidos
- Suporte a diferentes períodos de coleta

**Implementação:**
```python
class CvmScraper:
    @staticmethod
    def baixar_extrair_csv(url, nome_arquivo_csv):
        # Baixa arquivo ZIP e extrai o CSV desejado
        
    @staticmethod
    def importa_dados(data_inicio, data_fim, tabela_info):
        # Importa dados para um intervalo de datas
        # Retorna um DataFrame pandas com os dados
```

**Parâmetros de Configuração:**
- URLs base para download
- Mapeamento de tabelas para arquivos CSV
- Configurações de timeout e retentativas

### Collector

O `CvmDataCollector` coordena o processo de coleta de dados, utilizando o Scraper para realizar o download e orquestrando o intervalo de datas.

**Recursos Principais:**
- Gerenciamento de períodos de coleta
- Coordenação entre scraping e processamento
- Manipulação de erros durante a coleta
- Logging detalhado do processo

**Implementação:**
```python
class CvmDataCollector:
    def __init__(self, table_info, logger=None):
        self.table_info = table_info
        self.logger = logger or Logger()
        self.exec_logger = self.logger.get_exec_logger()
        self.error_logger = self.logger.get_error_logger()
        
    def collect_data(self, data_inicio, data_fim=None):
        # Coleta dados para o intervalo especificado
        
    def _importa_dados(self, data_inicio, data_fim):
        # Utiliza o CvmScraper para importar os dados
        # Trata erros e retorna o DataFrame resultante
```

### Processor

O `DataProcessor` é responsável por limpar, transformar e padronizar os dados coletados.

**Recursos Principais:**
- Remoção de registros duplicados
- Conversão de tipos de dados (datas, números)
- Tratamento de valores ausentes
- Normalização de formatos
- Validação de integridade dos dados

**Implementação:**
```python
class DataProcessor:
    def __init__(self, logger=None):
        self.logger = logger or Logger()
        self.exec_logger = self.logger.get_exec_logger()
        self.error_logger = self.logger.get_error_logger()
        self.data_logger = self.logger.get_data_logger()
        
    def process_data(self, df, table_info):
        # Processa o DataFrame de acordo com as regras da tabela
        
    def remove_duplicates(self, df, key_columns):
        # Remove registros duplicados com base nas colunas-chave
        
    def convert_dates(self, df, date_columns, date_format=None):
        # Converte colunas de datas para o formato datetime
        
    def convert_numeric(self, df, numeric_columns):
        # Converte colunas numéricas para os tipos adequados
```

### Database

O `DatabaseHandler` gerencia todas as operações relacionadas ao banco de dados, incluindo criação de esquemas, inserção e atualização de dados.

**Recursos Principais:**
- Criação automática de tabelas
- Detecção inteligente de tipos de dados
- Inserção eficiente de grandes volumes de dados
- Transações com rollback automático em caso de erro
- Exportação de dados em diferentes formatos

**Implementação:**
```python
class DatabaseHandler:
    def __init__(self, db_path='data/fidc.db', logger=None):
        self.db_path = db_path
        self.logger = logger or Logger()
        self.exec_logger = self.logger.get_exec_logger()
        self.error_logger = self.logger.get_error_logger()
        self.data_logger = self.logger.get_data_logger()
        self.connection = self._create_connection()
        
    def _create_connection(self):
        # Cria e retorna uma conexão com o banco de dados
        
    def create_table(self, table_name, df, primary_key=None):
        # Cria tabela com base na estrutura do DataFrame
        
    def insert_data(self, table_name, df, if_exists='append'):
        # Insere dados na tabela especificada
        
    def export_data(self, table_name, output_format='csv', output_path=None):
        # Exporta dados da tabela no formato especificado
```

### Pipeline

O `FidcPipeline` é o componente central que orquestra todo o fluxo de coleta, processamento e armazenamento de dados.

**Recursos Principais:**
- Orquestração do fluxo completo
- Gerenciamento de dependências entre tabelas
- Controle de erros e recuperação
- Configuração flexível das tabelas a serem coletadas

**Implementação:**
```python
class FidcPipeline:
    def __init__(self, tables_config, logger=None):
        self.tables_config = tables_config
        self.logger = logger or Logger()
        self.exec_logger = self.logger.get_exec_logger()
        self.error_logger = self.logger.get_error_logger()
        self.collector = CvmDataCollector(None, logger=self.logger)
        self.processor = DataProcessor(logger=self.logger)
        self.db_handler = DatabaseHandler(logger=self.logger)
        
    def run(self, data_inicio, data_fim=None):
        # Executa o pipeline completo para todas as tabelas
        
    def process_table(self, table_name, table_info, data_inicio, data_fim):
        # Processa uma tabela específica (coleta, processa, armazena)
        
    def export_tables(self, output_format='csv', tables=None):
        # Exporta as tabelas especificadas no formato desejado
```

## Fluxo de Processamento

O fluxo completo de processamento segue os seguintes passos:

1. **Inicialização**:
   - Carregamento das configurações das tabelas
   - Inicialização dos componentes (Logger, Collector, Processor, DatabaseHandler)
   - Preparação dos diretórios de trabalho

2. **Para cada tabela configurada**:
   - **Coleta de Dados**:
     - O Collector determina o intervalo de datas a ser coletado
     - O Scraper baixa os arquivos ZIP da CVM
     - Os arquivos CSV são extraídos dos ZIPs
     - Os dados são convertidos em DataFrames pandas

   - **Processamento**:
     - Remoção de registros duplicados
     - Conversão de tipos de dados
     - Tratamento de valores inconsistentes
     - Normalização de formatos
     - Validação dos dados processados

   - **Armazenamento**:
     - Criação da tabela no banco se não existir
     - Inserção dos dados processados
     - Registro de métricas (quantidade de registros, tempo de processamento)

3. **Finalização**:
   - Geração de relatório de execução
   - Backup dos dados (opcional)
   - Limpeza de arquivos temporários

## Configuração

O sistema é configurado principalmente através do arquivo `config/tables.py`, que define as tabelas a serem coletadas e seus parâmetros:

```python
TABLES = {
    'caracteristicas_fundo': {
        'url_pattern': 'http://dados.cvm.gov.br/dados/FI/DOC/ICVM555/DADOS/inf_cadastral_fi_{year}{month}.csv',
        'primary_key': ['CNPJ_FUNDO', 'DT_REG'],
        'date_columns': ['DT_REG', 'DT_CONST', 'DT_CANCEL', 'DT_INI_EXERC', 'DT_FIM_EXERC'],
        'date_format': '%Y-%m-%d',
        'numeric_columns': ['VL_PATRIM_LIQ', 'CONDOM']
    },
    'carteira_ativos': {
        'url_pattern': 'http://dados.cvm.gov.br/dados/FI/DOC/CDA/DADOS/cda_fi_YYYY{year}{month}.zip',
        'csv_name': 'cda_fi_{year}{month}.csv',
        'primary_key': ['CNPJ_FUNDO', 'DT_COMPTC', 'CD_ATIVO'],
        'date_columns': ['DT_COMPTC'],
        'date_format': '%Y-%m-%d',
        'numeric_columns': ['QT_NEGS', 'QT_POS_FINAL', 'VL_MERC_POS_FINAL', 'VL_CUSTO_TOT']
    },
    # Outras tabelas...
}
```

**Parâmetros de Configuração**:
- `url_pattern`: Padrão da URL para download dos dados, com placeholders para ano e mês
- `csv_name`: Nome do arquivo CSV dentro do ZIP (quando aplicável)
- `primary_key`: Colunas que compõem a chave primária
- `date_columns`: Colunas que contêm datas
- `date_format`: Formato das datas
- `numeric_columns`: Colunas numéricas
- `dependencies`: Tabelas que devem ser processadas antes desta

## Logs

O sistema mantém três tipos distintos de logs:

### Logs de Execução
Registram informações sobre o fluxo de execução do sistema:
```
2023-03-15 10:23:45 [INFO] Pipeline iniciado para tabela 'carteira_ativos'
2023-03-15 10:24:12 [INFO] Download concluído: cda_fi_202301.zip (2.3MB)
2023-03-15 10:24:15 [INFO] Extração concluída: 14523 registros processados
```

### Logs de Erro
Registram erros e exceções que ocorrem durante a execução:
```
2023-03-15 10:52:33 [ERROR] Falha ao baixar arquivo: Connection timeout
2023-03-15 10:52:33 [ERROR] Traceback: ...
2023-03-15 10:52:34 [INFO] Tentativa 2 de 3 para URL: http://dados.cvm.gov.br/...
```

### Logs de Dados
Registram informações sobre os dados processados:
```
2023-03-15 11:05:22 [INFO] Tabela 'carteira_ativos': 14523 registros importados
2023-03-15 11:05:22 [INFO] Duplicatas removidas: 28 registros
2023-03-15 11:05:23 [INFO] Valores nulos tratados: 142 células em 98 registros
```

## Testes

O sistema conta com uma suíte abrangente de testes unitários e de integração, implementados com pytest:

### Estrutura de Testes
```
tests/
├── fixtures/               # Dados compartilhados para testes
├── integration/            # Testes de integração
└── test_*.py               # Testes unitários para cada componente
```

### Tipos de Testes

#### Testes Unitários
Testam componentes individuais de forma isolada, utilizando mocks para simular dependências:
```python
def test_scraper_download_success(mock_response):
    # Testa o download bem-sucedido de um arquivo
    response = mock_response(200, b'test data')
    result = CvmScraper.baixar_extrair_csv('http://test.url', 'output.csv')
    assert result.status_code == 200
    assert os.path.exists('output.csv')
```

#### Testes de Integração
Testam a interação entre múltiplos componentes:
```python
def test_collector_processor_integration():
    # Testa a integração entre o Collector e o Processor
    collector = CvmDataCollector(TABLES['carteira_ativos'])
    processor = DataProcessor()
    
    df = collector.collect_data('2023-01-01', '2023-01-31')
    processed_df = processor.process_data(df, TABLES['carteira_ativos'])
    
    assert not processed_df.empty
    assert 'DT_COMPTC' in processed_df.columns
    assert processed_df['DT_COMPTC'].dtype == 'datetime64[ns]'
```

### Execução dos Testes
Os testes podem ser executados através do script `tests/run_tests.py`:
```bash
# Executar todos os testes
python -m tests.run_tests

# Executar testes específicos
pytest tests/test_scraper.py -v
pytest tests/test_processor.py::test_remove_duplicates -v
```

## Implantação

O sistema pode ser implantado em diversos ambientes:

### Ambiente de Desenvolvimento
```
# Instalar dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Executar em modo de desenvolvimento
python main.py --start-date=2023-01-01 --end-date=2023-01-31
```

### Ambiente de Produção
```
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar apenas dependências de produção
pip install -r requirements.txt

# Executar em modo de produção
python main.py --env=prod --start-date=2023-01-01
```

### Agendamento de Execução
O sistema pode ser configurado para execução periódica através de ferramentas como cron (Linux/Mac) ou Agendador de Tarefas (Windows):

**Exemplo de configuração cron (Linux/Mac)**:
```
# Executar diariamente às 3h da manhã
0 3 * * * cd /path/to/project && python main.py --update-mode=incremental
```

**Exemplo para Docker**:
Um Dockerfile está disponível para facilitar a implantação em ambientes containerizados:
```
# Construir a imagem
docker build -t fidc-collector .

# Executar o container
docker run -v ./data:/app/data fidc-collector --start-date=2023-01-01
```

## Uso

### Linha de Comando
A aplicação pode ser executada diretamente através do arquivo `main.py`:

```bash
# Execução básica (coleta dados do último mês)
python main.py

# Especificar intervalo de datas
python main.py --start-date=2022-01-01 --end-date=2022-12-31

# Coletar apenas tabelas específicas
python main.py --tables=carteira_ativos,rentabilidade

# Modo de atualização incremental
python main.py --update-mode=incremental

# Exportar dados coletados
python main.py --export-format=csv --export-dir=./exported_data
```

### Uso Programático
O sistema também pode ser utilizado como biblioteca em outros projetos Python:

```python
from src.core.pipeline import FidcPipeline
from config.tables import TABLES

# Inicializar o pipeline
pipeline = FidcPipeline(TABLES)

# Coletar dados
pipeline.run(data_inicio='2022-01-01', data_fim='2022-12-31')

# Exportar dados
pipeline.export_tables(output_format='csv', 
                      output_dir='./exported_data',
                      tables=['carteira_ativos', 'rentabilidade'])
```

### API (Futura Implementação)
Uma API REST está em desenvolvimento para permitir acesso aos dados coletados:

```
GET /api/v1/tables                      # Lista todas as tabelas disponíveis
GET /api/v1/tables/{table_name}         # Obtém dados de uma tabela
GET /api/v1/funds/{cnpj}                # Obtém dados de um fundo específico
GET /api/v1/statistics                  # Obtém estatísticas de mercado
```

## Contribuição

Contribuições são bem-vindas! Por favor, siga estas etapas:

1. Verifique as issues abertas ou crie uma nova issue para discutir a mudança proposta
2. Fork o repositório
3. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
4. Implemente as mudanças com testes apropriados
5. Execute os testes para garantir que tudo está funcionando (`python -m tests.run_tests`)
6. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
7. Push para a branch (`git push origin feature/nova-funcionalidade`)
8. Abra um Pull Request

### Diretrizes de Contribuição
- Siga o estilo de código existente (PEP 8)
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário
- Mantenha os commits atômicos e mensagens claras
- Verifique se todos os testes estão passando antes de submeter o PR
