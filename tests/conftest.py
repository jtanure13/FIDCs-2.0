"""
Configurações globais do pytest para o projeto de FIDCs.
"""
import pytest
import tempfile
import os
import pandas as pd
from unittest.mock import MagicMock
import io
import zipfile

@pytest.fixture
def mock_loggers():
    """Fixture para fornecer mocks dos loggers para testes."""
    execution_logger = MagicMock()
    error_logger = MagicMock()
    data_logger = MagicMock()
    return execution_logger, error_logger, data_logger

@pytest.fixture
def temp_dir():
    """Fixture para criar diretório temporário para testes."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def sample_table_config():
    """Fixture para configuração de tabela de teste."""
    return {
        "name": "caracteristicas_fundo",
        "prefix": "inf_mensal_fidc_tab_I",
        "tab_code": "I",
        "P_Keys": ["CNPJ", "Data", "TP_FUNDO_CLASSE"]
    }

@pytest.fixture
def sample_dataframe():
    """Fixture para fornecer um DataFrame de exemplo para testes."""
    return pd.DataFrame({
        'CNPJ': ['123', '456', '789'],
        'Data': ['2023-01-01', '2023-01-01', '2023-01-01'],
        'TP_FUNDO_CLASSE': ['A', 'B', 'C'],
        'Valor': [100, 200, 300]
    })

@pytest.fixture
def dataframe_with_duplicates():
    """Fixture para fornecer um DataFrame com duplicatas para testes."""
    return pd.DataFrame({
        'CNPJ': ['123', '123', '789'],
        'Data': ['2023-01-01', '2023-01-01', '2023-01-01'],
        'TP_FUNDO_CLASSE': ['A', '', 'C'],
        'Valor': [100, 200, 300]
    })

@pytest.fixture
def sample_zip_content():
    """Fixture para simular o conteúdo de um arquivo ZIP da CVM."""
    # Cria um arquivo ZIP em memória
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        # Cria um CSV em memória
        csv_content = "DT_COMPTC;CNPJ_FUNDO;VALOR\n2023-01-01;12345678901234;1000.50\n2023-01-01;98765432109876;2500.75"
        zip_file.writestr("inf_mensal_fidc_tab_I_202301.csv", csv_content)
    
    # Retorna o buffer com o conteúdo do ZIP
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

@pytest.fixture
def mock_database_connection():
    """Fixture para fornecer uma conexão mockada de banco de dados."""
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    return mock_connection, mock_cursor 