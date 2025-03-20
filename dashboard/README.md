# Dashboard de Análise de FIDCs

Este projeto implementa um dashboard interativo para análise e visualização de dados de Fundos de Investimento em Direitos Creditórios (FIDCs) a partir de dados coletados pelo sistema de webscraping da CVM.

## Estrutura do Projeto

```
dashboard/
├── docs/                      # Documentação detalhada
│   ├── DASHBOARD.md           # Especificações completas do dashboard
│   └── ADVANCED_METRICS.md    # Métricas avançadas para implementação futura
│
├── src/                       # Código-fonte
│   ├── backend/               # Backend em Python/FastAPI
│   │   ├── api/               # Endpoints da API
│   │   ├── models/            # Modelos de dados
│   │   ├── services/          # Serviços de processamento de dados
│   │   └── utils/             # Utilitários
│   │
│   └── frontend/              # Frontend em React.js
│       ├── components/        # Componentes reutilizáveis
│       ├── pages/             # Páginas do dashboard
│       ├── services/          # Serviços e conexão com API
│       ├── utils/             # Utilitários
│       └── assets/            # Recursos estáticos (imagens, ícones)
│
└── README.md                  # Este arquivo
```

## Visão Geral

O dashboard oferece diferentes visões para análise de FIDCs, incluindo:

1. **Visão Geral do Mercado**: Panorama completo do mercado de FIDCs no Brasil
2. **Análise Individual**: Análise detalhada de FIDCs específicos
3. **Comparação**: Ferramentas para comparar diferentes FIDCs
4. **Análise Setorial**: Análise por setor de atuação

## Documentação

Para detalhes completos sobre o projeto, consulte os seguintes documentos:

- [Especificações do Dashboard](docs/DASHBOARD.md): Documentação completa do design e funcionalidades
- [Métricas Avançadas](docs/ADVANCED_METRICS.md): Documentação de métricas e técnicas avançadas para implementação futura

## Tecnologias Utilizadas

### Backend
- Python 3.9+
- FastAPI
- Pandas, NumPy
- SQLite/PostgreSQL

### Frontend
- React.js
- Plotly.js/ECharts
- Material-UI
- Redux

## Desenvolvimento Futuro

Este projeto será desenvolvido em fases, conforme detalhado na documentação. A primeira fase focará nas funcionalidades essenciais e visualizações básicas, enquanto fases posteriores incluirão recursos mais avançados e análises sofisticadas.

## Integração

Este dashboard consome dados coletados pelo sistema de webscraping de FIDCs, localizado no diretório principal. Os dados são processados e transformados para alimentar as visualizações e análises apresentadas no dashboard. 