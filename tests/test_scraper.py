"""
Testes para o módulo scraper (src.core.scraper).
"""
import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
import pytest
from datetime import datetime
import io
import zipfile
from src.core.scraper import CvmScraper
from tests.fixtures.mock_responses import CARACTERISTICAS_FUNDO_ZIP, CARACTERISTICAS_FUNDO_CSV

class TestCvmScraper(unittest.TestCase):
    """Testes para a classe CvmScraper."""
    
    def setUp(self):
        """Configuração que executa antes de cada teste."""
        # Não precisamos de muito setup, pois CvmScraper usa métodos estáticos
        pass
    
    @patch('requests.get')
    def test_baixar_extrair_csv(self, mock_get):
        """Testa a extração de CSV de um arquivo ZIP."""
        # Configurar o mock para retornar um ZIP simulado
        mock_response = MagicMock()
        mock_response.content = CARACTERISTICAS_FUNDO_ZIP
        mock_get.return_value = mock_response
        
        # Chamar o método
        result = CvmScraper.baixar_extrair_csv(
            "https://exemplo.com/arquivo.zip",
            "inf_mensal_fidc_tab_I_202301.csv"
        )
        
        # Verificar o resultado
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)  # 3 linhas no CSV
        self.assertIn('DT_COMPTC', result.columns)
        self.assertIn('CNPJ_FUNDO', result.columns)
        self.assertIn('TP_FUNDO_CLASSE', result.columns)
        self.assertIn('VL_PATRIM_LIQ', result.columns)
    
    @patch('requests.get')
    def test_baixar_extrair_csv_error(self, mock_get):
        """Testa o tratamento de erros ao extrair CSV."""
        # Configurar o mock para lançar uma exceção
        mock_get.side_effect = Exception("Erro de conexão")
        
        # Chamar o método deve lançar a exceção
        with self.assertRaises(Exception):
            CvmScraper.baixar_extrair_csv(
                "https://exemplo.com/arquivo.zip",
                "arquivo_inexistente.csv"
            )
    
    @patch('pandas.date_range')
    @patch('src.core.scraper.CvmScraper.baixar_extrair_csv')
    def test_importa_dados_success(self, mock_baixar_extrair, mock_date_range):
        """Testa a importação de dados para múltiplos meses."""
        # Configurar mock para retornar datas específicas
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
        
        # Chamar o método
        result = CvmScraper.importa_dados("prefixo_teste", "2023-01-01")
        
        # Verificar o resultado
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 4)  # 4 registros no total (2 + 2)
        
        # Verificar se as colunas foram renomeadas corretamente
        self.assertIn('Data', result.columns)
        self.assertIn('CNPJ', result.columns)
        
        # Verificar se os dados foram concatenados corretamente
        cnpjs = list(result['CNPJ'].values)
        self.assertIn('123', cnpjs)
        self.assertIn('456', cnpjs)
        self.assertIn('789', cnpjs)
        self.assertIn('012', cnpjs)
    
    @patch('pandas.date_range')
    @patch('src.core.scraper.CvmScraper.baixar_extrair_csv')
    def test_importa_dados_empty(self, mock_baixar_extrair, mock_date_range):
        """Testa o comportamento quando não há dados para importar."""
        # Configurar mock para retornar um range vazio
        mock_date_range.return_value = pd.DatetimeIndex([])
        
        # Chamar o método
        result = CvmScraper.importa_dados("prefixo_teste", "2023-01-01")
        
        # Verificar o resultado
        self.assertIsNone(result)
        # Verificar que o baixar_extrair_csv não foi chamado
        mock_baixar_extrair.assert_not_called()
    
    @patch('pandas.date_range')
    @patch('src.core.scraper.CvmScraper.baixar_extrair_csv')
    def test_importa_dados_partial_errors(self, mock_baixar_extrair, mock_date_range):
        """Testa o tratamento de erros parciais durante a importação."""
        # Configurar mock para retornar datas específicas
        mock_date_range.return_value = pd.DatetimeIndex([
            pd.Timestamp('2023-01-01'),
            pd.Timestamp('2023-02-01'),
            pd.Timestamp('2023-03-01')
        ])
        
        # Criar DataFrames de teste para os meses bem-sucedidos
        df1 = pd.DataFrame({
            'DT_COMPTC': ['2023-01-01'],
            'CNPJ_FUNDO': ['123'],
            'VALOR': [100]
        })
        
        df3 = pd.DataFrame({
            'DT_COMPTC': ['2023-03-01'],
            'CNPJ_FUNDO': ['789'],
            'VALOR': [300]
        })
        
        # Configurar mock para sucesso, erro, sucesso
        mock_baixar_extrair.side_effect = [
            df1,  # Janeiro ok
            Exception("Erro no mês 2"),  # Fevereiro falha
            df3   # Março ok
        ]
        
        # Chamar o método
        result = CvmScraper.importa_dados("prefixo_teste", "2023-01-01")
        
        # Verificar o resultado
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)  # 2 registros (1 + 1), o do meio foi pulado
        
        # Verificar se os dados foram concatenados corretamente (sem o mês que falhou)
        cnpjs = list(result['CNPJ'].values)
        self.assertIn('123', cnpjs)
        self.assertIn('789', cnpjs)
    
    @patch('pandas.date_range')
    @patch('src.core.scraper.CvmScraper.baixar_extrair_csv')
    def test_importa_dados_all_errors(self, mock_baixar_extrair, mock_date_range):
        """Testa o comportamento quando todos os meses falham."""
        # Configurar mock para retornar datas específicas
        mock_date_range.return_value = pd.DatetimeIndex([
            pd.Timestamp('2023-01-01'),
            pd.Timestamp('2023-02-01')
        ])
        
        # Configurar mock para falhar em todas as chamadas
        mock_baixar_extrair.side_effect = [
            Exception("Erro no mês 1"),
            Exception("Erro no mês 2")
        ]
        
        # Chamar o método
        result = CvmScraper.importa_dados("prefixo_teste", "2023-01-01")
        
        # Verificar o resultado
        self.assertIsNone(result)
        
        # Verificar que o baixar_extrair_csv foi chamado para todos os meses
        self.assertEqual(mock_baixar_extrair.call_count, 2)
    
    @patch('pandas.to_datetime')
    @patch('pandas.date_range')
    def test_importa_dados_data_conversion(self, mock_date_range, mock_to_datetime):
        """Testa a conversão de datas na importação."""
        # Configurar mocks
        mock_to_datetime.return_value = "2023-01-01_convertida"
        mock_date_range.return_value = pd.DatetimeIndex([])
        
        # Chamar o método
        CvmScraper.importa_dados("prefixo_teste", "2023-01-01")
        
        # Verificar a conversão da data
        mock_to_datetime.assert_called_once_with("2023-01-01")


if __name__ == '__main__':
    unittest.main() 