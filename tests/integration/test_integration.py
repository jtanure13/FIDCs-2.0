"""
Testes de integração para o sistema de coleta e processamento de FIDCs.
"""
import unittest
import os
import pandas as pd
import tempfile
import sqlite3
from unittest.mock import patch, MagicMock
import pytest
from src.core.logger import Logger
from src.core.scraper import CvmScraper
from src.core.collector import CvmDataCollector
from src.core.processor import DataProcessor
from src.core.database import DatabaseHandler
from src.core.pipeline import Pipeline

class TestIntegration(unittest.TestCase):
    """Testes de integração para os componentes do sistema."""
    
    def setUp(self):
        """Configuração que executa antes de cada teste."""
        # Criar diretório temporário para logs e arquivos de teste
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Inicializar o logger com o diretório temporário
        self.logger = Logger(log_dir=os.path.join(self.temp_dir.name, 'logs'))
        self.execution_logger, self.error_logger, self.data_logger = self.logger.get_loggers()
        
        # Configuração de teste
        self.config = {
            'tabelas': [
                {
                    'name': 'caracteristicas_fidc',
                    'prefix': 'inf_cadastral_fi',
                    'tab_code': '1',
                    'P_Keys': ['CNPJ_FUNDO', 'DT_COMPTC']
                }
            ]
        }
        
        # Caminho do banco de dados temporário
        self.db_path = os.path.join(self.temp_dir.name, 'test_db.sqlite')
        
    def tearDown(self):
        """Limpeza após cada teste."""
        # Remover arquivos temporários
        self.temp_dir.cleanup()
    
    @patch('src.core.scraper.CvmScraper.baixar_extrair_csv')
    def test_pipeline_integration(self, mock_baixar_extrair):
        """Testa a integração entre Collector, Processor e DatabaseHandler."""
        # Criar um DataFrame de teste para simular os dados baixados
        test_df = pd.DataFrame({
            'CNPJ_FUNDO': ['12345678901234', '23456789012345', '34567890123456'],
            'DT_COMPTC': ['2023-01-31', '2023-01-31', '2023-01-31'],
            'TP_FUNDO': ['FIDC', 'FIDC', 'FIDC'],
            'VL_TOTAL': ['1000000,00', '2000000,00', '3000000,00'],
            'QT_COTAS': ['1000', '2000', '3000']
        })
        
        # Configurar o mock para retornar o DataFrame de teste
        mock_baixar_extrair.return_value = test_df
        
        # Inicializar os componentes
        collector = CvmDataCollector(
            self.execution_logger,
            self.error_logger,
            self.data_logger
        )
        
        processor = DataProcessor(
            self.execution_logger,
            self.error_logger,
            self.data_logger
        )
        
        db_handler = DatabaseHandler(
            self.execution_logger,
            self.error_logger,
            self.data_logger,
            db_path=self.db_path
        )
        
        # Inicializar o pipeline com os componentes reais
        pipeline = Pipeline(
            self.execution_logger,
            self.error_logger,
            self.data_logger,
            collector,
            processor,
            db_handler
        )
        
        # Executar o pipeline
        result = pipeline.run_pipeline(self.config)
        
        # Verificar o resultado
        self.assertTrue(result)
        
        # Verificar se o banco de dados foi criado
        self.assertTrue(os.path.exists(self.db_path))
        
        # Conectar ao banco de dados e verificar se a tabela foi criada com os dados
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verificar se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='caracteristicas_fidc'")
        tables = cursor.fetchall()
        self.assertEqual(len(tables), 1)
        
        # Verificar o número de registros
        cursor.execute('SELECT COUNT(*) FROM caracteristicas_fidc')
        count = cursor.fetchone()[0]
        self.assertEqual(count, 3)
        
        # Fechar conexão
        cursor.close()
        conn.close()
    
    @patch('src.core.scraper.CvmScraper.baixar_extrair_csv')
    def test_data_processing_integration(self, mock_baixar_extrair):
        """Testa a integração entre Collector e Processor."""
        # Criar um DataFrame de teste com duplicatas e tipos que precisam de conversão
        test_df = pd.DataFrame({
            'CNPJ_FUNDO': ['12345678901234', '12345678901234', '34567890123456'],  # Duplicata
            'DT_COMPTC': ['31/01/2023', '31/01/2023', '31/01/2023'],  # Formato de data brasileiro
            'TP_FUNDO': ['FIDC', 'FIDC', 'FIDC'],
            'VL_TOTAL': ['1000000,00', '1500000,00', '3000000,00'],  # Valores com vírgula
            'QT_COTAS': ['1000', '1200', '3000']  # Strings que precisam ser convertidas para int
        })
        
        # Configurar o mock para retornar o DataFrame de teste
        mock_baixar_extrair.return_value = test_df
        
        # Inicializar os componentes
        collector = CvmDataCollector(
            self.execution_logger,
            self.error_logger,
            self.data_logger
        )
        
        processor = DataProcessor(
            self.execution_logger,
            self.error_logger,
            self.data_logger
        )
        
        # Coletar os dados
        collected_data = collector.collect_data(self.config['tabelas'][0])
        
        # Verificar se os dados foram coletados
        self.assertIsNotNone(collected_data)
        self.assertEqual(len(collected_data), 3)
        
        # Processar os dados
        processed_data = processor.process_data(
            collected_data,
            duplicate_keys=['CNPJ_FUNDO', 'DT_COMPTC'],
            date_cols=['DT_COMPTC'],
            int_cols=['QT_COTAS'],
            float_cols=['VL_TOTAL']
        )
        
        # Verificar se os dados foram processados corretamente
        self.assertIsNotNone(processed_data)
        
        # Verificar se as duplicatas foram removidas
        self.assertEqual(len(processed_data), 2)
        
        # Verificar se os tipos foram convertidos corretamente
        self.assertTrue(pd.api.types.is_datetime64_dtype(processed_data['DT_COMPTC']))
        self.assertTrue(pd.api.types.is_integer_dtype(processed_data['QT_COTAS']))
        self.assertTrue(pd.api.types.is_float_dtype(processed_data['VL_TOTAL']))
        
        # Verificar se o último valor foi mantido para a linha duplicada (padrão keep='last')
        duplicated_row = processed_data[processed_data['CNPJ_FUNDO'] == '12345678901234']
        self.assertEqual(duplicated_row['VL_TOTAL'].iloc[0], 1500000.0)
    
    @patch('src.core.scraper.CvmScraper.baixar_extrair_csv')
    @patch('os.makedirs')
    def test_export_integration(self, mock_makedirs, mock_baixar_extrair):
        """Testa a integração entre o Collector e a funcionalidade de exportação."""
        # Criar um DataFrame de teste
        test_df = pd.DataFrame({
            'CNPJ_FUNDO': ['12345678901234', '23456789012345', '34567890123456'],
            'DT_COMPTC': ['2023-01-31', '2023-01-31', '2023-01-31'],
            'TP_FUNDO': ['FIDC', 'FIDC', 'FIDC'],
            'VL_TOTAL': ['1000000,00', '2000000,00', '3000000,00'],
            'QT_COTAS': ['1000', '2000', '3000']
        })
        
        # Configurar o mock para retornar o DataFrame de teste
        mock_baixar_extrair.return_value = test_df
        
        # Inicializar os componentes
        collector = CvmDataCollector(
            self.execution_logger,
            self.error_logger,
            self.data_logger
        )
        
        processor = DataProcessor(
            self.execution_logger,
            self.error_logger,
            self.data_logger
        )
        
        db_handler = DatabaseHandler(
            self.execution_logger,
            self.error_logger,
            self.data_logger,
            db_path=self.db_path
        )
        
        # Inicializar o pipeline com os componentes reais
        pipeline = Pipeline(
            self.execution_logger,
            self.error_logger,
            self.data_logger,
            collector,
            processor,
            db_handler
        )
        
        # Testar exportação para CSV
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            result_csv = pipeline.export_data(self.config, 'csv', self.temp_dir.name)
            self.assertTrue(result_csv)
            mock_to_csv.assert_called_once()
        
        # Testar exportação para Excel
        with patch('pandas.DataFrame.to_excel') as mock_to_excel:
            result_excel = pipeline.export_data(self.config, 'excel', self.temp_dir.name)
            self.assertTrue(result_excel)
            mock_to_excel.assert_called_once()


if __name__ == '__main__':
    unittest.main() 