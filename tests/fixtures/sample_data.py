"""
Dados de exemplo para uso nos testes.
"""
import pandas as pd

# Configurações de tabelas para testes
SAMPLE_TABLES = [
    {
        "name": "caracteristicas_fundo",
        "prefix": "inf_mensal_fidc_tab_I",
        "tab_code": "I",
        "P_Keys": ["CNPJ", "Data", "TP_FUNDO_CLASSE"]
    },
    {
        "name": "patrimonio_liquido",
        "prefix": "inf_mensal_fidc_tab_IV",
        "tab_code": "IV",
        "P_Keys": ["CNPJ", "Data", "TP_FUNDO_CLASSE"]
    }
]

# DataFrame sem duplicatas
CLEAN_DATAFRAME = pd.DataFrame({
    'CNPJ': ['123', '456', '789'],
    'Data': ['2023-01-01', '2023-01-01', '2023-01-01'],
    'TP_FUNDO_CLASSE': ['A', 'B', 'C'],
    'Valor_Int': [100, 200, 300],
    'Valor_Float': [1.1, 2.2, 3.3],
    'Texto': ['Texto1', 'Texto2', 'Texto3']
})

# DataFrame com duplicatas de CNPJ e Data
DUPLICATED_DATAFRAME = pd.DataFrame({
    'CNPJ': ['123', '123', '789', '789'],
    'Data': ['2023-01-01', '2023-01-01', '2023-01-01', '2023-02-01'],
    'TP_FUNDO_CLASSE': ['A', '', 'C', 'D'],
    'Valor': [100, 200, 300, 400]
})

# DataFrame com problemas (muitas duplicatas)
PROBLEMATIC_DATAFRAME = pd.DataFrame({
    'CNPJ': ['123'] * 300 + ['456'],
    'Data': ['2023-01-01'] * 301,
    'TP_FUNDO_CLASSE': ['A'] * 300 + ['B'],
    'Valor': list(range(300)) + [999]
})

# DataFrame com dois meses diferentes
MULTI_MONTH_DATAFRAME = pd.DataFrame({
    'CNPJ': ['123', '456', '123', '456'],
    'Data': ['2023-01-01', '2023-01-01', '2023-02-01', '2023-02-01'],
    'TP_FUNDO_CLASSE': ['A', 'B', 'A', 'B'],
    'Valor': [100, 200, 150, 250]
})

# DataFrame com tipos diferentes para testar inferência de tipos
MIXED_TYPES_DATAFRAME = pd.DataFrame({
    'CNPJ': ['123', '456', '789'],
    'Data': ['2023-01-01', '2023-01-01', '2023-01-01'],
    'TP_FUNDO_CLASSE': ['A', 'B', 'C'],
    'Valor_Int': [100, 200, 300],
    'Valor_Float': [1.1, 2.2, 3.3],
    'Texto': ['Texto1', 'Texto2', 'Texto3'],
    'Boolean': [True, False, True]
}) 