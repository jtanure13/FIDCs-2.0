"""
Respostas simuladas para APIs externas usadas nos testes.
"""
import io
import zipfile
import pandas as pd

def create_mock_zip_response(file_name, csv_content):
    """
    Cria um conteúdo de resposta ZIP simulado para testes.
    
    Args:
        file_name: Nome do arquivo CSV dentro do ZIP
        csv_content: Conteúdo do arquivo CSV
        
    Returns:
        bytes: Conteúdo do arquivo ZIP
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr(file_name, csv_content)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

# Conteúdo CSV para simular respostas da CVM
CARACTERISTICAS_FUNDO_CSV = """DT_COMPTC;CNPJ_FUNDO;TP_FUNDO_CLASSE;VL_PATRIM_LIQ
2023-01-01;12345678901234;A;1000000.50
2023-01-01;98765432109876;B;2500000.75
2023-01-01;11111111111111;A;3000000.25"""

PATRIMONIO_LIQUIDO_CSV = """DT_COMPTC;CNPJ_FUNDO;TP_FUNDO_CLASSE;VL_TOTAL;VL_QUOTA
2023-01-01;12345678901234;A;1100000.50;1.05
2023-01-01;98765432109876;B;2600000.75;1.10
2023-01-01;11111111111111;A;3100000.25;1.15"""

# Cria respostas ZIP simuladas
CARACTERISTICAS_FUNDO_ZIP = create_mock_zip_response(
    "inf_mensal_fidc_tab_I_202301.csv",
    CARACTERISTICAS_FUNDO_CSV
)

PATRIMONIO_LIQUIDO_ZIP = create_mock_zip_response(
    "inf_mensal_fidc_tab_IV_202301.csv",
    PATRIMONIO_LIQUIDO_CSV
)

# Respostas de erro simuladas
ERROR_RESPONSE_404 = {
    "status_code": 404,
    "reason": "Not Found",
    "content": b"File not found"
}

ERROR_RESPONSE_500 = {
    "status_code": 500,
    "reason": "Internal Server Error",
    "content": b"Server error"
}

# Função para criar DataFrame a partir do conteúdo CSV
def csv_to_dataframe(csv_content, sep=';'):
    """
    Converte conteúdo CSV em DataFrame.
    
    Args:
        csv_content: Conteúdo CSV como string
        sep: Separador de colunas
        
    Returns:
        pandas.DataFrame: DataFrame com os dados do CSV
    """
    return pd.read_csv(io.StringIO(csv_content), sep=sep)

# DataFrames correspondentes às respostas CSV
CARACTERISTICAS_FUNDO_DF = csv_to_dataframe(CARACTERISTICAS_FUNDO_CSV)
PATRIMONIO_LIQUIDO_DF = csv_to_dataframe(PATRIMONIO_LIQUIDO_CSV) 