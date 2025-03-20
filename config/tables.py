# Configuração das tabelas e seus metadados

# Dicionário que mapeia cada arquivo CSV ao seu nome de tabela
ARQUIVOS_FONTE_PROCESSADO = {
    "inf_mensal_fidc_tab_I_": "Características Fundo",
    "inf_mensal_fidc_tab_II_": "Carteira Ativos",
    "inf_mensal_fidc_tab_III_": "Passivos e Derivativos",
    "inf_mensal_fidc_tab_IV_": "Patrimônio Líquido",
    "inf_mensal_fidc_tab_V_": "Prazos Créditos",
    "inf_mensal_fidc_tab_VI_": "Inadimplência",
    "inf_mensal_fidc_tab_VII_": "Cedentes e Tomadores",
    "inf_mensal_fidc_tab_IX_": "Preços Mercado",
    "inf_mensal_fidc_tab_X_": "Risco Crédito",
    "inf_mensal_fidc_tab_X_1_": "Classes e Cotistas",
    "inf_mensal_fidc_tab_X_1_1_": "Distribuição Cotistas",
    "inf_mensal_fidc_tab_X_2_": "Cotas e Valores",
    "inf_mensal_fidc_tab_X_3_": "Rentabilidade",
    "inf_mensal_fidc_tab_X_4_": "Operações Estruturadas",
    "inf_mensal_fidc_tab_X_5_": "Liquidez Ativos",
    "inf_mensal_fidc_tab_X_6_": "Performance Fundo",
    "inf_mensal_fidc_tab_X_7_": "Garantias e Seguros"
}

# Lista de tabelas com seus metadados
TABLES = [
    {"name": "caracteristicas_fundo", "prefix": "inf_mensal_fidc_tab_I", "tab_code": "I", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE']},
    {"name": "patrimonio_liquido", "prefix": "inf_mensal_fidc_tab_IV", "tab_code": "IV", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE']},
    {"name": "carteira_ativos", "prefix": "inf_mensal_fidc_tab_II", "tab_code": "II", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE']},
    {"name": "passivos_derivativos", "prefix": "inf_mensal_fidc_tab_III", "tab_code": "III", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE']},
    {"name": "prazos_creditos", "prefix": "inf_mensal_fidc_tab_V", "tab_code": "V", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE']},
    {"name": "inadimplencia", "prefix": "inf_mensal_fidc_tab_VI", "tab_code": "VI", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE']},
    {"name": "cedentes_tomadores", "prefix": "inf_mensal_fidc_tab_VII", "tab_code": "VII", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE']},
    {"name": "precos_mercado", "prefix": "inf_mensal_fidc_tab_IX", "tab_code": "IX", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE']},
    {"name": "risco_credito", "prefix": "inf_mensal_fidc_tab_X", "tab_code": "X", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE']},
    {"name": "classes_cotistas", "prefix": "inf_mensal_fidc_tab_X_1", "tab_code": "X_1", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE', 'TAB_X_CLASSE_SERIE']},
    {"name": "distribuicao_cotistas", "prefix": "inf_mensal_fidc_tab_X_1_1", "tab_code": "X_1_1", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE']},
    {"name": "cotas_valores", "prefix": "inf_mensal_fidc_tab_X_2", "tab_code": "X_2", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE', 'TAB_X_CLASSE_SERIE']},
    {"name": "rentabilidade", "prefix": "inf_mensal_fidc_tab_X_3", "tab_code": "X_3", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE', 'TAB_X_CLASSE_SERIE']},
    {"name": "operacoes_estruturadas", "prefix": "inf_mensal_fidc_tab_X_4", "tab_code": "X_4", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE', 'TAB_X_CLASSE_SERIE', 'TAB_X_TP_OPER']},
    {"name": "liquidez_ativos", "prefix": "inf_mensal_fidc_tab_X_5", "tab_code": "X_5", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE']},
    {"name": "performance_fundo", "prefix": "inf_mensal_fidc_tab_X_6", "tab_code": "X_6", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE', 'TAB_X_CLASSE_SERIE']},
    {"name": "garantias_seguros", "prefix": "inf_mensal_fidc_tab_X_7", "tab_code": "X_7", 'P_Keys': ['CNPJ', 'Data', 'TP_FUNDO_CLASSE']},
]