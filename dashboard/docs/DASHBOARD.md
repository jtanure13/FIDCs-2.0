# Dashboard de Análise de FIDCs

## Índice
1. [Introdução](#introdução)
2. [Objetivos do Dashboard](#objetivos-do-dashboard)
3. [Arquitetura e Tecnologias](#arquitetura-e-tecnologias)
4. [Principais Métricas](#principais-métricas)
   - [Métricas de Performance](#métricas-de-performance)
   - [Métricas de Risco](#métricas-de-risco)
   - [Métricas de Composição](#métricas-de-composição)
   - [Métricas Comparativas](#métricas-comparativas)
5. [Interface e Visualizações](#interface-e-visualizações)
   - [Visão Geral do Mercado](#visão-geral-do-mercado)
   - [Análise Individual de FIDCs](#análise-individual-de-fidcs)
   - [Comparação entre FIDCs](#comparação-entre-fidcs)
   - [Análise Setorial](#análise-setorial)
6. [Fluxo de Dados](#fluxo-de-dados)
7. [Implementação](#implementação)
8. [Extensões Futuras](#extensões-futuras)
9. [Referências](#referências)

## Introdução

Este documento descreve o design e as especificações do Dashboard de Análise de FIDCs, uma interface web interativa que permite visualizar e analisar dados de Fundos de Investimento em Direitos Creditórios (FIDCs) coletados pelo sistema de webscraping da CVM.

O dashboard tem como objetivo principal fornecer uma visão clara, intuitiva e efetiva do mercado de FIDCs no Brasil, permitindo tanto uma análise de alto nível do mercado como um todo quanto análises detalhadas de fundos individuais ou comparações entre diferentes fundos.

## Objetivos do Dashboard

1. **Visualização Intuitiva**: Apresentar dados complexos em um formato visual de fácil compreensão
2. **Análise Comparativa**: Permitir a comparação direta entre diferentes FIDCs e setores
3. **Monitoramento de Tendências**: Identificar tendências e padrões no mercado ao longo do tempo
4. **Detecção de Anomalias**: Destacar fundos com comportamento atípico ou potencialmente problemático
5. **Suporte à Decisão**: Fornecer informações relevantes para decisões de investimento ou regulatórias
6. **Personalização**: Permitir que os usuários personalizem as visualizações de acordo com suas necessidades

## Arquitetura e Tecnologias

O dashboard será implementado usando tecnologias modernas para garantir desempenho, interatividade e facilidade de manutenção:

### Backend
- **Python**: Processamento de dados e cálculo de métricas (Pandas, NumPy)
- **FastAPI**: API RESTful para comunicação com frontend
- **SQLite/PostgreSQL**: Armazenamento dos dados processados

### Frontend
- **React.js**: Biblioteca JavaScript para construção da interface
- **Plotly.js/ECharts**: Biblioteca de visualização interativa
- **Material-UI**: Framework de componentes para uma interface moderna
- **Redux**: Gerenciamento de estado da aplicação

### Arquitetura de Alto Nível
```
┌──────────────────┐    ┌───────────────┐    ┌───────────────┐
│                  │    │               │    │               │
│  Webscraper CVM  ├───►│  Banco de     ├───►│  API Backend  │
│                  │    │  Dados        │    │               │
└──────────────────┘    └───────────────┘    └───────┬───────┘
                                                     │
                                                     ▼
                                            ┌───────────────┐
                                            │               │
                                            │  Frontend     │
                                            │  Dashboard    │
                                            │               │
                                            └───────────────┘
```

## Principais Métricas

O dashboard apresentará um conjunto inicial de métricas cuidadosamente selecionadas que oferecem uma visão abrangente do desempenho e das características dos FIDCs, sem sobrecarregar o usuário com informações excessivamente complexas ou redundantes.

### Métricas de Performance

1. **Rentabilidade**
   - **Rentabilidade Anualizada**: Taxa de retorno anualizada do fundo
   - **Rentabilidade Acumulada**: Retorno total durante um período específico
   - **Comparação com Benchmark**: Diferença de performance em relação ao CDI ou outro benchmark
   - **Consistência de Retornos**: Desvio-padrão dos retornos mensais

2. **Valor do Patrimônio Líquido**
   - **PL Atual**: Valor atual do patrimônio líquido
   - **Evolução do PL**: Série histórica do patrimônio líquido
   - **Taxa de Crescimento do PL**: Crescimento percentual em diferentes períodos

3. **Índices de Eficiência**
   - **Índice de Despesas**: Relação entre despesas administrativas e PL
   - **Índice de Captação**: Relação entre novas entradas e PL médio
   - **Relação Custo-Benefício**: Despesas versus retorno gerado

### Métricas de Risco

1. **Inadimplência**
   - **Taxa de Inadimplência Atual**: Percentual de créditos em atraso
   - **Inadimplência por Faixa de Atraso**: Distribuição por tempo de atraso (15-30, 31-60, 61-90, >90 dias)
   - **Tendência de Inadimplência**: Evolução histórica das taxas de inadimplência
   - **Comparação Setorial**: Posição relativa ao setor de atuação

2. **Concentração**
   - **Concentração de Cedentes**: Percentual dos maiores cedentes no total
   - **Concentração de Devedores**: Percentual dos maiores devedores no total
   - **Concentração Setorial**: Distribuição dos direitos creditórios por setor
   - **Índice Herfindahl-Hirschman (IHH)**: Medida formal de concentração

3. **Garantias e Cobertura**
   - **Razão de Cobertura**: Relação entre garantias e valor dos créditos
   - **Tipos de Garantia**: Distribuição por tipos de garantia
   - **Subordinação**: Percentual de cotas subordinadas

4. **Volatilidade**
   - **Volatilidade Diária**: Desvio-padrão dos retornos diários
   - **Volatilidade Anualizada**: Volatilidade projetada para o período de um ano
   - **Drawdown Máximo**: Maior queda de valor registrada em um período

### Métricas de Composição

1. **Perfil de Cotistas**
   - **Distribuição por Tipo**: Percentual de investidores por categoria (PF, PJ, Institucionais)
   - **Número de Cotistas**: Total de investidores no fundo
   - **Ticket Médio**: Valor médio investido por cotista

2. **Composição de Ativos**
   - **Direitos Creditórios**: Percentual do patrimônio em direitos creditórios
   - **Títulos Públicos**: Percentual em títulos públicos para liquidez
   - **Outros Ativos**: Outros componentes da carteira

3. **Prazo dos Créditos**
   - **Prazo Médio**: Duration média da carteira de créditos
   - **Distribuição por Vencimento**: Percentual por faixas de vencimento
   - **Índice de Renovação**: Taxa de renovação de direitos creditórios

### Métricas Comparativas

1. **Posicionamento no Mercado**
   - **Ranking por PL**: Posição relativa em termos de tamanho
   - **Ranking por Rentabilidade**: Posição relativa em termos de performance
   - **Ranking por Risco-Retorno**: Relação entre retorno e risco

2. **Comparação com Pares**
   - **Distância da Média do Setor**: Desvio em relação à média setorial
   - **Quartis de Performance**: Posicionamento nos quartis de performance
   - **Correlação com Média do Setor**: Grau de movimentação conjunta

3. **Indicadores Relativos**
   - **Retorno Ajustado ao Risco**: Índice de Sharpe ou Sortino
   - **Alfa**: Retorno acima do esperado dado o risco
   - **Beta**: Sensibilidade à movimentação do mercado

## Interface e Visualizações

A interface do dashboard será organizada em múltiplas visões que permitem ao usuário explorar os dados em diferentes níveis de detalhe e com diferentes focos de análise.

### Visão Geral do Mercado

**Objetivo**: Fornecer uma visão rápida do estado atual do mercado de FIDCs no Brasil.

**Principais Visualizações**:
1. **Mapa de Calor do Mercado**: Visualização 2D mostrando a distribuição de FIDCs por tamanho e performance
2. **Indicadores Macro**:
   - Patrimônio Líquido Total do Mercado
   - Número de Fundos Ativos
   - Média de Rentabilidade
   - Média de Inadimplência
3. **Distribuição Setorial**: Gráfico de treemap ou sunburst mostrando a distribuição dos FIDCs por setor
4. **Tendências Recentes**:
   - Evolução do PL total nos últimos 12 meses
   - Tendência de criação/encerramento de fundos
   - Evolução da inadimplência média

**Interatividade**:
- Filtros por período, setor, tipo de fundo
- Drill-down para análise detalhada de setores específicos
- Tooltips detalhados com informações complementares

### Análise Individual de FIDCs

**Objetivo**: Permitir uma análise detalhada de um FIDC específico.

**Principais Visualizações**:
1. **Cartão de Identidade**:
   - Nome, CNPJ, Data de Constituição
   - Administrador, Gestor, Custodiante
   - Classificação ANBIMA, Tipo de Fundo
   - PL Atual, Número de Cotistas
2. **Dashboard de Performance**:
   - Série histórica de rentabilidade
   - Comparação com benchmark
   - Volatilidade e drawdowns
3. **Perfil de Risco**:
   - Gráfico radar com dimensões de risco
   - Evolução da inadimplência
   - Concentração de cedentes e devedores
4. **Composição**:
   - Gráfico de pizza da composição atual
   - Evolução da composição ao longo do tempo
   - Prazos dos direitos creditórios

**Interatividade**:
- Seleção de períodos de análise
- Comparação com benchmarks personalizáveis
- Exportação de relatórios em PDF
- Alertas e notificações configuráveis

### Comparação entre FIDCs

**Objetivo**: Facilitar a comparação direta entre dois ou mais FIDCs selecionados.

**Principais Visualizações**:
1. **Tabela Comparativa**:
   - Indicadores-chave lado a lado
   - Destaques para maiores diferenças
   - Classificação relativa em cada métrica
2. **Gráficos Comparativos**:
   - Rentabilidade acumulada sobreposta
   - Histórico de inadimplência
   - Evolução do PL
3. **Radar Chart Comparativo**:
   - Múltiplas dimensões de análise
   - Cada FIDC representado por uma cor
   - Facilidade para identificar pontos fortes e fracos

**Interatividade**:
- Adição/remoção de fundos da comparação
- Personalização das métricas apresentadas
- Normalização de escalas para comparação justa
- Exportação da análise comparativa

### Análise Setorial

**Objetivo**: Analisar o comportamento dos FIDCs agrupados por setor de atuação.

**Principais Visualizações**:
1. **Desempenho Setorial**:
   - Rentabilidade média por setor
   - Dispersão de performance intra-setor
   - Evolução temporal por setor
2. **Perfil de Risco Setorial**:
   - Inadimplência média por setor
   - Volatilidade setorial
   - Concentração típica
3. **Mapa de Posicionamento**:
   - Gráfico de dispersão (risco x retorno)
   - Cada ponto é um FIDC, agrupados por cor/setor
   - Linhas de tendência setoriais

**Interatividade**:
- Filtros temporais e por características
- Zoom em setores específicos
- Personalização de métricas de eixos
- Seleção de FIDCs para análise detalhada

## Fluxo de Dados

O dashboard será alimentado pelos dados coletados pelo sistema de webscraping já implementado, seguindo um fluxo de processamento que garante dados atualizados e métricas precisas:

1. **Coleta de Dados**: O sistema de webscraping coleta dados da CVM periodicamente
2. **Processamento**: Os dados brutos são processados para:
   - Limpeza e normalização
   - Cálculo de métricas derivadas
   - Agregação por períodos e categorias
3. **Armazenamento**: Os dados processados são armazenados em banco de dados
4. **API**: Uma API REST disponibiliza os dados para o frontend
5. **Renderização**: O frontend obtém os dados e renderiza as visualizações
6. **Interatividade**: O usuário interage com as visualizações, gerando novas consultas à API

```
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│            │     │            │     │            │     │            │
│  Coleta    ├────►│Processamento├────►│    Banco   ├────►│    API     │
│            │     │            │     │            │     │            │
└────────────┘     └────────────┘     └────────────┘     └─────┬──────┘
                                                               │
                   ┌────────────┐                              │
                   │            │                              │
                   │ Usuário    │◄─────────────────────────────┘
                   │            │
                   └─────┬──────┘
                         │
                         ▼
                   ┌────────────┐
                   │            │
                   │ Frontend   │
                   │            │
                   └────────────┘
```

## Implementação

O desenvolvimento do dashboard seguirá uma abordagem modular e iterativa, com foco na entrega de valor desde as primeiras versões:

### Fase 1: Fundamentos
- Implementação da estrutura básica do frontend
- Desenvolvimento da API para acesso aos dados
- Implementação das visualizações essenciais:
  - Visão geral do mercado
  - Página de análise individual simplificada
  - Comparação básica entre fundos

### Fase 2: Refinamento
- Adição de mais métricas e visualizações
- Implementação de filtros avançados
- Melhorias na interatividade
- Otimização de performance
- Testes com usuários e ajustes de usabilidade

### Fase 3: Personalização
- Sistema de usuários e perfis
- Dashboards personalizáveis
- Alertas e notificações
- Exportação de relatórios
- Integração com outras ferramentas

### Tecnologias Específicas
- **Frontend**: React.js, Redux, Plotly.js/ECharts, Material-UI
- **Backend**: FastAPI, pandas, NumPy, scikit-learn (para métricas estatísticas)
- **Banco de Dados**: SQLite (desenvolvimento), PostgreSQL (produção)
- **Infraestrutura**: Docker, Nginx, GitHub Actions (CI/CD)

## Extensões Futuras

Após a implementação bem-sucedida da primeira versão do dashboard, diversas extensões e melhorias podem ser consideradas:

### Análises Avançadas
- **Modelos Preditivos**: Previsão de tendências e comportamentos futuros
- **Detecção de Anomalias**: Identificação automatizada de comportamentos atípicos
- **Análise de Redes**: Visualização das relações entre cedentes, fundos e cotistas
- **Aprendizado de Máquina**: Classificação e agrupamento de fundos por características

### Novas Visualizações
- **Mapas Geográficos**: Distribuição regional de FIDCs e cedentes
- **Grafos de Relacionamento**: Visualização de relações entre entidades
- **Análise de Séries Temporais**: Ferramentas avançadas para análise temporal
- **Visualizações 3D**: Representações tridimensionais para análises multivariadas

### Integrações
- **APIs Externas**: Integração com dados macroeconômicos e de mercado
- **Exportação de Dados**: Formatos compatíveis com ferramentas de análise
- **Notificações**: Alertas por email ou outros canais
- **Mobile**: Versão adaptada para dispositivos móveis

## Referências

1. CVM - Comissão de Valores Mobiliários. "Instrução CVM 356"
2. ANBIMA - Associação Brasileira das Entidades dos Mercados Financeiro e de Capitais. "Guia de FIDCs"
3. Few, Stephen. "Information Dashboard Design: Displaying Data for At-a-Glance Monitoring"
4. Tufte, Edward. "The Visual Display of Quantitative Information"
5. Murray, Scott. "Interactive Data Visualization for the Web"
6. Cairo, Alberto. "The Functional Art: An Introduction to Information Graphics and Visualization" 