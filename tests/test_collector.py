"""
Testes para o módulo collector (src.core.collector).
"""
import unittest
import pandas as pd
import os
from unittest.mock import patch, MagicMock, call
import pytest
from src.core.collector import CvmDataCollector
from tests.fixtures.sample_data import CLEAN_DATAFRAME

class TestCvmDataCollector(unittest.TestCase):
    """Testes para a classe CvmDataCollector."""
    
    def setUp(self):
        """Configuração que executa antes de cada teste."""
        # Mock dos loggers
        self.execution_logger = MagicMock()
        self.error_logger = MagicMock()
        self.data_logger = MagicMock()
        
        # Configuração de tabela para teste
        self.test_config = {
            "name": "caracteristicas_fundo",
            "prefix": "inf_mensal_fidc_tab_I",
            "tab_code": "I",
            "P_Keys": ["CNPJ", "Data", "TP_FUNDO_CLASSE"]
        }
        
        # Inicializa o coletor
        self.collector = CvmDataCollector(
            self.test_config,
            self.execution_logger,
            self.error_logger,
            self.data_logger
        )
        
        # Mock para os.makedirs
        self.makedirs_patcher = patch('os.makedirs')
        self.mock_makedirs = self.makedirs_patcher.start()
        
    def tearDown(self):
        """Limpeza após cada teste."""
        self.makedirs_patcher.stop()
    
    def test_initialization(self):
        """Testa se o coletor é inicializado corretamente."""
        # Verificar se os atributos foram configurados corretamente
        self.assertEqual(self.collector.table_config, self.test_config)
        self.assertEqual(self.collector.table_name, "caracteristicas_fundo")
        self.assertEqual(self.collector.file_prefix, "inf_mensal_fidc_tab_I")
        self.assertEqual(self.collector.execution_logger, self.execution_logger)
        self.assertEqual(self.collector.error_logger, self.error_logger)
        self.assertEqual(self.collector.data_logger, self.data_logger)
        self.assertEqual(self.collector.url_base, 'https://dados.cvm.gov.br/dados/FIDC/DOC/INF_MENSAL/DADOS/')
    
    @patch('src.core.collector.CvmDataCollector._importa_dados')
    def test_collect_data_success(self, mock_importa_dados):
        """Testa coleta de dados bem-sucedida."""
        # Mock do método _importa_dados para retornar dados de teste
        mock_importa_dados.return_value = CLEAN_DATAFRAME.copy()
        
        # Mock do método to_csv para não salvar arquivo real
        with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
            # Chamar o método
            result = self.collector.collect_data()
            
            # Verificar se os diretórios foram criados
            self.mock_makedirs.assert_called_once_with('data/raw', exist_ok=True)
            
            # Verificar se _importa_dados foi chamado corretamente
            mock_importa_dados.assert_called_once_with(data_inicio='2020-01-01')
            
            # Verificar se os dados foram salvos
            mock_to_csv.assert_called_once_with('data/raw/caracteristicas_fundo_raw.csv', index=False)
            
            # Verificar se os logs foram feitos
            self.execution_logger.info.assert_called()
            self.data_logger.info.assert_called()
            
            # Verificar o resultado
            self.assertIsInstance(result, pd.DataFrame)
            self.assertEqual(len(result), 3)
    
    @patch('src.core.collector.CvmDataCollector._importa_dados')
    def test_collect_data_empty(self, mock_importa_dados):
        """Testa comportamento quando não há dados para coletar."""
        # Mock do método _importa_dados para retornar None
        mock_importa_dados.return_value = None
        
        # Chamar o método
        result = self.collector.collect_data()
        
        # Verificar se os diretórios foram criados
        self.mock_makedirs.assert_called_once_with('data/raw', exist_ok=True)
        
        # Verificar se _importa_dados foi chamado corretamente
        mock_importa_dados.assert_called_once_with(data_inicio='2020-01-01')
        
        # Verificar se os logs foram feitos
        self.data_logger.warning.assert_called_once()
        
        # Verificar o resultado
        self.assertIsNone(result)
    
    @patch('src.core.collector.CvmDataCollector._importa_dados')
    def test_collect_data_error(self, mock_importa_dados):
        """Testa tratamento de erros durante a coleta."""
        # Mock do método _importa_dados para lançar exceção
        mock_importa_dados.side_effect = Exception("Erro de teste")
        
        # Chamar o método
        result = self.collector.collect_data()
        
        # Verificar se os logs de erro foram feitos
        self.error_logger.error.assert_called_once()
        
        # Verificar o resultado
        self.assertIsNone(result)
    
    @patch('src.core.scraper.CvmScraper.baixar_extrair_csv')
    @patch('pandas.date_range')
    @patch('pandas.to_datetime')
    def test_importa_dados(self, mock_to_datetime, mock_date_range, mock_baixar_extrair):
        """Testa o método _importa_dados."""
        # Configurar mocks
        mock_to_datetime.return_value = pd.Timestamp('2023-01-01')
        mock_date_range.return_value = pd.DatetimeIndex([
            pd.Timestamp('2023-01-01'),
            pd.Timestamp('2023-02-01')
        ])
        
        # Criar DataFrames de teste para cada mês
        df1 = pd.DataFrame({
            'DT_COMPTC': ['2023-01-01', '2023-01-01'],
            'CNPJ_FUNDO': ['123', '456'],
            'VALOR': [100, 200]
        })
        
        df2 = pd.DataFrame({
            'DT_COMPTC': ['2023-02-01', '2023-02-01'],
            'CNPJ_FUNDO_CLASSE': ['789', '012'],
            'VALOR': [300, 400]
        })
        
        # Configurar mock para retornar os DataFrames
        mock_baixar_extrair.side_effect = [df1, df2]
        
        # Mock para tqdm
        with patch('src.core.collector.tqdm') as mock_tqdm:
            # Configurar mock tqdm para funcionar com o for loop
            mock_iter = MagicMock()
            mock_iter.__iter__.return_value = iter([pd.Timestamp('2023-01-01'), pd.Timestamp('2023-02-01')])
            mock_tqdm.return_value = mock_iter
            
            # Chamar o método
            result = self.collector._importa_dados('2023-01-01')
            
            # Verificar o resultado
            self.assertIsInstance(result, pd.DataFrame)
            self.assertEqual(len(result), 4)  # 4 registros no total (2 + 2)
    
    @patch('pandas.date_range')
    def test_importa_dados_empty_range(self, mock_date_range):
        """Testa comportamento quando o range de datas está vazio."""
        # Configurar mock para retornar um range vazio
        mock_date_range.return_value = pd.DatetimeIndex([])
        
        # Mock para print
        with patch('builtins.print') as mock_print:
            # Chamar o método
            result = self.collector._importa_dados('2023-01-01')
            
            # Verificar o resultado
            self.assertIsNone(result)
            
            # Verificar se a mensagem foi impressa
            mock_print.assert_called_with("🚫 Nenhum período para baixar.")
    
    @patch('src.core.scraper.CvmScraper.baixar_extrair_csv')
    @patch('pandas.date_range')
    @patch('pandas.to_datetime')
    def test_importa_dados_all_errors(self, mock_to_datetime, mock_date_range, mock_baixar_extrair):
        """Testa comportamento quando todos os downloads falham."""
        # Configurar mocks
        mock_to_datetime.return_value = pd.Timestamp('2023-01-01')
        mock_date_range.return_value = pd.DatetimeIndex([
            pd.Timestamp('2023-01-01'),
            pd.Timestamp('2023-02-01')
        ])
        
        # Configurar mock para lançar exceções
        mock_baixar_extrair.side_effect = Exception("Erro de teste")
        
        # Mock para tqdm
        with patch('src.core.collector.tqdm') as mock_tqdm:
            # Configurar mock tqdm para funcionar com o for loop
            mock_iter = MagicMock()
            mock_iter.__iter__.return_value = iter([pd.Timestamp('2023-01-01'), pd.Timestamp('2023-02-01')])
            mock_tqdm.return_value = mock_iter
            
            # Mock para print
            with patch('builtins.print') as mock_print:
                # Chamar o método
                result = self.collector._importa_dados('2023-01-01')
                
                # Verificar o resultado
                self.assertIsNone(result)
                
                # Verificar se a mensagem foi impressa
                mock_print.assert_called_with("🚫 Nenhum dado novo.")


if __name__ == '__main__':
    unittest.main() 