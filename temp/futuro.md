# Plano Detalhado das Fases Futuras do Projeto

Este documento detalha as fases futuras do projeto de coleta, processamento e análise de dados de FIDCs, complementado com dados macroeconômicos.

## Fase 1: Otimização do Sistema Atual (1-2 meses)

Esta fase foca em aprimorar a base do sistema existente, garantindo robustez, eficiência e preparando o terreno para as fases seguintes.

### 1. Revisão e Otimização do Processo de Web Scraping

**Objetivo**: Melhorar a eficiência, confiabilidade e resiliência do processo de coleta de dados da CVM.

**Passo a Passo**:

1.  **Análise de Desempenho**:
    *   Utilizar ferramentas de profiling (como `cProfile` e `line_profiler` em Python) para identificar gargalos no código atual do `CvmScraper`.
    *   Medir tempos de execução de cada etapa (download, extração, parsing).
    *   Analisar o uso de memória durante o processo.

2.  **Implementação de Mecanismos de Cache**:
    *   **Cache de Requisições**:
        *   Utilizar a biblioteca `requests_cache` para armazenar respostas de requisições HTTP.
        *   Configurar o cache para expirar em intervalos adequados (ex: 1 dia para dados diários, 1 semana para dados mensais).
        *   Implementar lógica para invalidar o cache quando novos dados forem disponibilizados pela CVM (verificação de data de modificação do arquivo, por exemplo).
    *   **Cache de Dados Processados**:
        *   Armazenar resultados intermediários do processamento (DataFrames do Pandas) em formato pickle ou Parquet.
        *   Utilizar um esquema de versionamento para garantir que dados cacheados sejam compatíveis com a versão atual do código.

3.  **Tratamento Robusto de Erros e Retentativas**:
    *   **Erros de Rede**:
        *   Implementar retentativas com backoff exponencial (aumentando o tempo de espera entre tentativas) usando a biblioteca `tenacity`.
        *   Definir um número máximo de tentativas e um tempo limite total.
        *   Capturar exceções específicas de rede (`requests.exceptions.RequestException`, etc.) e tratá-las adequadamente.
    *   **Erros de Dados**:
        *   Adicionar verificações de integridade dos arquivos baixados (verificar tamanho, formato, conteúdo).
        *   Implementar lógica para lidar com arquivos corrompidos ou incompletos (ex: baixar novamente, registrar erro).
        *   Utilizar expressões regulares mais robustas para validar o formato dos dados.
    *   **Logging Detalhado**:
        *   Registrar cada tentativa, erro e sucesso em logs detalhados, incluindo timestamps, URLs, mensagens de erro e stack traces.

4.  **Otimização do Uso de Memória**:
    *   **Processamento em Chunks**:
        *   Utilizar o parâmetro `chunksize` do `pd.read_csv` para processar arquivos CSV grandes em partes menores.
        *   Processar cada chunk individualmente e salvar os resultados parciais no banco de dados.
    *   **Liberação de Memória**:
        *   Utilizar `del` para remover variáveis e DataFrames da memória após o uso.
        *   Utilizar o coletor de lixo do Python (`gc.collect()`) para forçar a liberação de memória.
    *   **Tipos de Dados Eficientes**:
        *   Converter colunas para tipos de dados mais eficientes (ex: `category` para strings com baixa cardinalidade, `Int32` em vez de `Int64` se os valores permitirem).

### 2. Melhoria da Estrutura do Banco de Dados

**Objetivo**: Otimizar o schema do banco de dados para consultas de séries temporais, melhorar performance e adicionar campos calculados.

**Passo a Passo**:

1.  **Análise do Schema Atual**:
    *   Identificar tabelas e colunas mais acessadas em consultas.
    *   Analisar os tipos de dados utilizados e verificar se são os mais adequados.
    *   Verificar a existência de índices e sua eficácia.

2.  **Reorganização para Séries Temporais**:
    *   **Coluna de Data Central**:
        *   Garantir que cada tabela tenha uma coluna de data (`data_referencia`) como chave primária ou parte de uma chave primária composta.
        *   Utilizar o tipo de dado `DATE` ou `DATETIME` apropriado para o banco de dados.
    *   **Tabelas de Fatos e Dimensões**:
        *   Considerar a criação de tabelas de dimensões para informações que se repetem (ex: dados cadastrais do FIDC).
        *   Criar tabelas de fatos para os dados que variam no tempo (ex: patrimônio líquido, número de cotistas).
    *   **Particionamento (se aplicável)**:
        *   Para bancos de dados que suportam particionamento (ex: PostgreSQL, MySQL), considerar particionar tabelas grandes por data.

3.  **Implementação de Índices**:
    *   **Índices Compostos**:
        *   Criar índices compostos em colunas frequentemente usadas em conjunto em cláusulas `WHERE` (ex: `(data_referencia, id_fidc)`).
    *   **Índices Parciais (se aplicável)**:
        *   Para bancos de dados que suportam (ex: PostgreSQL), criar índices parciais para condições específicas (ex: índice apenas para FIDCs ativos).

4.  **Desenvolvimento de Campos Calculados**:
    *   **Campos Calculados no Banco de Dados**:
        *   Utilizar views ou colunas calculadas (generated columns) para criar campos como:
            *   Variação percentual do patrimônio líquido em relação ao mês anterior.
            *   Rentabilidade acumulada no ano.
            *   Indicadores de inadimplência (ex: atraso acima de 90 dias / total da carteira).
        *   Garantir que os cálculos sejam eficientes e não sobrecarreguem o banco de dados.
    *   **Campos Calculados na Aplicação**:
        *   Para cálculos mais complexos ou que dependam de dados de várias tabelas, realizar os cálculos na aplicação (Python) e armazenar os resultados em novas colunas no banco de dados.

### 3. Tratamento Avançado de Dados

**Objetivo**: Implementar detecção e correção de anomalias, melhorar o tratamento de valores ausentes e adicionar validações de integridade.

**Passo a Passo**:

1.  **Detecção e Correção de Anomalias**:
    *   **Outliers**:
        *   Utilizar métodos estatísticos (ex: desvio padrão, IQR) para identificar outliers em séries temporais.
        *   Implementar regras para tratar outliers (ex: substituir por valores interpolados, remover registros, marcar para análise manual).
    *   **Valores Inconsistentes**:
        *   Definir regras de validação para cada campo (ex: patrimônio líquido não pode ser negativo, número de cotistas deve ser inteiro).
        *   Implementar verificações de consistência entre campos (ex: soma das cotas de diferentes classes deve ser igual ao total de cotas).

2.  **Tratamento de Valores Ausentes**:
    *   **Análise da Causa**:
        *   Investigar a razão dos valores ausentes (ex: erro na coleta, dado não informado, FIDC inativo).
        *   Registrar a causa em logs.
    *   **Imputação**:
        *   Utilizar técnicas de imputação apropriadas para séries temporais:
            *   **Interpolação**: Preencher valores ausentes com base em valores vizinhos.
            *   **Última Observação Válida (LOCF)**: Preencher com o último valor válido.
            *   **Média Móvel**: Preencher com a média dos valores em uma janela móvel.
            *   **Modelos de Machine Learning**: Em casos mais complexos, utilizar modelos de previsão para estimar valores ausentes.
    *   **Marcação**:
        *   Criar uma coluna adicional (`flag_valor_ausente`) para indicar se o valor original era ausente e foi imputado.

3.  **Validações de Integridade**:
    *   **Chaves Primárias e Estrangeiras**:
        *   Garantir que as chaves primárias sejam únicas e não nulas.
        *   Definir chaves estrangeiras para garantir a integridade referencial entre tabelas.
    *   **Restrições de Check**:
        *   Adicionar restrições de check para validar regras de negócio (ex: `patrimonio_liquido >= 0`).
    *   **Triggers (se necessário)**:
        *   Em casos mais complexos, utilizar triggers para realizar validações ou ações antes ou depois de inserções, atualizações ou exclusões.

## Fase 2: Integração com Dados Macroeconômicos (1 mês)

Esta fase visa enriquecer a base de dados com variáveis macroeconômicas relevantes, permitindo análises mais abrangentes.

### 1. Identificação de Fontes de Dados Macroeconômicos

**Objetivo**: Selecionar variáveis macroeconômicas relevantes e identificar fontes de dados confiáveis.

**Passo a Passo**:

1.  **Seleção de Variáveis**:
    *   **Indicadores de Inflação**: IPCA, IGP-M, INPC.
    *   **Taxas de Juros**: SELIC, CDI, Taxa de Juros de Longo Prazo (TJLP).
    *   **Indicadores de Atividade Econômica**: PIB, Produção Industrial, Vendas no Varejo, Taxa de Desemprego.
    *   **Indicadores de Crédito**: Concessões de Crédito, Inadimplência do Crédito.
    *   **Câmbio**: Taxa de Câmbio (dólar, euro).

2.  **Identificação de Fontes**:
    *   **Banco Central do Brasil (BCB)**: API do Sistema Gerenciador de Séries Temporais (SGS).
    *   **Instituto Brasileiro de Geografia e Estatística (IBGE)**: APIs de agregados macroeconômicos.
    *   **Fundação Getúlio Vargas (FGV)**: Índices de preços e confiança.
    *   **Outras Fontes**: IPEA, B3 (para dados de mercado).

### 2. Implementação de Coletores para Dados Macroeconômicos

**Objetivo**: Desenvolver módulos específicos para cada fonte de dados macroeconômicos e integrar ao pipeline existente.

**Passo a Passo**:

1.  **Desenvolvimento de Módulos**:
    *   Criar classes Python separadas para cada fonte de dados (ex: `BCBCollector`, `IBGECollector`).
    *   Utilizar bibliotecas como `requests` para acessar APIs e `pandas` para manipular os dados.
    *   Implementar tratamento de erros, retentativas e cache, similar ao `CvmScraper`.
    *   Padronizar a saída dos coletores para um formato comum (DataFrame do Pandas com colunas `data` e `valor`).

2.  **Integração ao Pipeline**:
    *   Modificar o `FidcPipeline` para incluir a coleta de dados macroeconômicos.
    *   Definir a frequência de coleta para cada variável (diária, mensal, etc.).
    *   Orquestrar a execução dos coletores de forma a minimizar o número de requisições e evitar sobrecarga das fontes de dados.

### 3. Normalização e Integração de Dados

**Objetivo**: Alinhar períodos e frequência dos dados e criar tabelas de relacionamento entre FIDCs e dados macro.

**Passo a Passo**:

1.  **Alinhamento de Períodos**:
    *   Definir a granularidade temporal comum (ex: dados mensais).
    *   Para variáveis com frequência diferente (ex: SELIC diária), agregar os dados para a granularidade desejada (ex: média mensal da SELIC).
    *   Utilizar funções do Pandas como `resample` para realizar a agregação.

2.  **Criação de Tabelas de Relacionamento**:
    *   Criar uma tabela `fidc_dados_macro` com as colunas:
        *   `data_referencia` (chave primária, DATE).
        *   `id_fidc` (chave estrangeira para a tabela de FIDCs).
        *   Colunas para cada variável macroeconômica (ex: `ipca`, `selic`, `pib`).
    *   Popular a tabela com os dados coletados e processados.

## Fase 3: Reestruturação para Análise Temporal (1 mês)

Esta fase visa otimizar a estrutura de dados para consultas e análises de séries temporais, incluindo a criação de métricas derivadas.

### 1. Modelagem de Dados para Análise de Séries Temporais

**Objetivo**: Implementar uma estrutura otimizada para consultas temporais e criar agregações por diferentes períodos.

**Passo a Passo**:

1.  **Estrutura Otimizada**:
    *   **Tabela Principal de Séries Temporais**:
        *   Criar uma tabela `fidc_serie_temporal` com as colunas:
            *   `data_referencia` (chave primária, DATE).
            *   `id_fidc` (chave estrangeira para a tabela de FIDCs).
            *   Colunas para cada variável do FIDC (ex: `patrimonio_liquido`, `num_cotistas`, `inadimplencia`).
    *   **Índices**:
        *   Criar índices compostos em `(data_referencia, id_fidc)` e em outras colunas frequentemente usadas em filtros.

2.  **Agregações por Período**:
    *   **Materialized Views (se suportado pelo banco de dados)**:
        *   Criar materialized views para agregações mensais, trimestrais e anuais dos dados.
        *   Atualizar as materialized views periodicamente (ex: diariamente).
    *   **Tabelas de Agregação**:
        *   Se materialized views não forem suportadas, criar tabelas separadas para cada agregação (ex: `fidc_serie_temporal_mensal`, `fidc_serie_temporal_trimestral`).
        *   Popular as tabelas com jobs agendados.

### 2. Criação de Métricas Derivadas

**Objetivo**: Desenvolver indicadores baseados em múltiplas variáveis e implementar cálculos de variação e tendências.

**Passo a Passo**:

1.  **Indicadores Baseados em Múltiplas Variáveis**:
    *   **Rentabilidade Ajustada ao Risco**:
        *   Calcular a rentabilidade do FIDC e ajustar por um indicador de risco (ex: volatilidade, perda esperada).
    *   **Índice de Sharpe**:
        *   Calcular o Índice de Sharpe do FIDC, comparando a rentabilidade com a taxa livre de risco (SELIC).
    *   **Outros Indicadores**:
        *   Desenvolver outros indicadores relevantes para análise de FIDCs, como duration, convexidade, etc.

2.  **Cálculos de Variação e Tendências**:
    *   **Variação Percentual**:
        *   Calcular a variação percentual de cada variável em relação ao período anterior (mês, trimestre, ano).
        *   Utilizar funções do Pandas como `pct_change`.
    *   **Médias Móveis**:
        *   Calcular médias móveis de diferentes períodos (ex: 3 meses, 6 meses, 12 meses) para suavizar flutuações e identificar tendências.
        *   Utilizar funções do Pandas como `rolling`.
    *   **Tendências**:
        *   Implementar algoritmos para identificar tendências de alta, baixa ou estabilidade em cada variável.

### 3. Testes de Desempenho Analítico

**Objetivo**: Verificar o tempo de resposta para consultas complexas e otimizar estruturas para os casos de uso mais comuns.

**Passo a Passo**:

1.  **Criação de Consultas de Teste**:
    *   Desenvolver um conjunto de consultas SQL que representem os casos de uso mais comuns de análise de dados.
    *   Incluir consultas com filtros, agregações, ordenações e junções de tabelas.

2.  **Medição de Tempo de Resposta**:
    *   Utilizar ferramentas do banco de dados para medir o tempo de execução de cada consulta.
    *   Executar as consultas em diferentes horários e com diferentes volumes de dados.

3.  **Otimização**:
    *   **Índices**:
        *   Analisar os planos de execução das consultas e verificar se os índices estão sendo utilizados corretamente.
        *   Adicionar ou modificar índices se necessário.
    *   **Reescrita de Consultas**:
        *   Se necessário, reescrever as consultas para torná-las mais eficientes.
        *   Utilizar dicas de otimização do banco de dados (ex: hints no Oracle).
    *   **Materialized Views/Tabelas de Agregação**:
        *   Verificar se as materialized views ou tabelas de agregação estão sendo utilizadas e se estão atualizadas.

## Fase 4: Desenvolvimento do Dashboard (1-2 meses)

Esta fase visa criar um dashboard interativo para visualização e análise dos dados de FIDCs e variáveis macroeconômicas.

### 1. Definição de Requisitos de Visualização

**Objetivo**: Identificar os principais indicadores e visualizações, e definir o fluxo de navegação e interação.

**Passo a Passo**:

1.  **Indicadores Principais**:
    *   **Evolução Temporal**:
        *   Patrimônio Líquido, Número de Cotistas, Rentabilidade, Inadimplência, Carteira de Ativos.
    *   **Comparação entre FIDCs**:
        *   Ranking por Patrimônio Líquido, Rentabilidade, Risco.
    *   **Correlação com Variáveis Macroeconômicas**:
        *   Gráficos mostrando a relação entre indicadores de FIDCs e variáveis como SELIC, IPCA, PIB.

2.  **Visualizações**:
    *   **Gráficos de Linha**: Para séries temporais.
    *   **Gráficos de Barra**: Para comparações entre FIDCs.
    *   **Gráficos de Dispersão**: Para correlações.
    *   **Tabelas**: Para dados detalhados.
    *   **Mapas de Calor**: Para visualizar a performance de diferentes FIDCs ao longo do tempo.

3.  **Fluxo de Navegação**:
    *   **Página Inicial**: Visão geral do mercado de FIDCs, com indicadores agregados.
    *   **Página de Detalhes do FIDC**: Informações detalhadas sobre um FIDC específico, incluindo séries temporais e comparação com outros FIDCs.
    *   **Página de Análise Macroeconômica**: Visualização da relação entre FIDCs e variáveis macroeconômicas.

4.  **Interação**:
    *   **Filtros**:
        *   Período de Tempo, Classe de Cota, Administrador, Gestor.
    *   **Seleção**:
        *   Selecionar um FIDC para ver detalhes.
    *   **Drill-Down**:
        *   Aprofundar em um indicador para ver mais detalhes (ex: clicar em um ponto do gráfico de linha para ver os dados daquele mês).

### 2. Implementação do Backend Analítico

**Objetivo**: Desenvolver APIs para alimentar o dashboard e implementar cache para consultas frequentes.

**Passo a Passo**:

1.  **Desenvolvimento de APIs**:
    *   Utilizar um framework como Flask ou FastAPI (Python) para criar APIs RESTful.
    *   Definir endpoints para cada tipo de consulta (ex: `/fidcs`, `/fidcs/{id}`, `/series_temporais`, `/macro`).
    *   Utilizar bibliotecas como Marshmallow ou Pydantic para validar e serializar os dados.

2.  **Implementação de Cache**:
    *   Utilizar um sistema de cache como Redis ou Memcached para armazenar resultados de consultas frequentes.
    *   Definir políticas de expiração de cache adequadas para cada tipo de dado.
    *   Invalidar o cache quando os dados forem atualizados.

### 3. Desenvolvimento do Frontend

**Objetivo**: Criar visualizações interativas e implementar filtros e controles para exploração de dados.

**Passo a Passo**:

1.  **Escolha de Tecnologias**:
    *   Utilizar um framework JavaScript como React, Vue.js ou Angular.
    *   Utilizar uma biblioteca de gráficos como Chart.js, D3.js ou Plotly.js.

2.  **Implementação das Visualizações**:
    *   Criar componentes reutilizáveis para cada tipo de visualização.
    *   Conectar os componentes às APIs do backend.
    *   Implementar interatividade (ex: zoom, pan, tooltips).

3.  **Implementação de Filtros e Controles**:
    *   Criar componentes para filtros (ex: dropdowns, date pickers).
    *   Implementar lógica para aplicar os filtros aos dados.
    *   Adicionar controles para ordenação e paginação de tabelas.

## Fase 5: Refinamento e Funcionalidades Adicionais (conforme necessário)

Esta fase visa refinar o sistema com base no feedback dos usuários e implementar funcionalidades adicionais.

### 1. Refinamento Baseado em Feedback

**Objetivo**: Ajustar visualizações e análises conforme necessidade e otimizar a performance de consultas frequentes.

**Passo a Passo**:

1.  **Coleta de Feedback**:
    *   Realizar testes com usuários e coletar feedback sobre a usabilidade, visualizações e funcionalidades do dashboard.
    *   Utilizar ferramentas de análise de uso (ex: Google Analytics) para identificar padrões de uso e pontos de melhoria.

2.  **Ajustes**:
    *   Modificar visualizações, fluxos de navegação e interações com base no feedback.
    *   Adicionar novas visualizações ou funcionalidades solicitadas pelos usuários.

3.  **Otimização de Performance**:
    *   Identificar consultas lentas ou gargalos no sistema.
    *   Otimizar consultas, índices ou estruturas de dados conforme necessário.

### 2. Implementação de Funcionalidades Extras

**Objetivo**: Adicionar funcionalidades como sistema de alertas e API pública.

**Passo a Passo**:

1.  **Sistema de Alertas**:
    *   Definir regras para alertas (ex: variação do patrimônio líquido acima de um limite, inadimplência acima de um patamar).
    *   Implementar um sistema para enviar alertas por e-mail ou outros canais.
    *   Permitir que os usuários configurem seus próprios alertas.

2.  **API Pública**:
    *   Definir os endpoints da API pública.
    *   Implementar autenticação e autorização para controlar o acesso aos dados.
    *   Documentar a API utilizando ferramentas como Swagger ou OpenAPI.

Este plano detalhado fornece um roteiro para o desenvolvimento futuro do projeto, cobrindo desde a otimização da base até a criação de um dashboard interativo e funcionalidades adicionais. 