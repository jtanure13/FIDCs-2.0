"""
Testes para o módulo pipeline (src.core.pipeline).
"""
import unittest
import pandas as pd
from unittest.mock import patch, MagicMock, call
import pytest
from src.core.pipeline import Pipeline
from tests.fixtures.sample_data import CLEAN_DATAFRAME

class TestPipeline(unittest.TestCase):
    """Testes para a classe Pipeline."""
    
    def setUp(self):
        """Configuração que executa antes de cada teste."""
        # Mock dos loggers
        self.execution_logger = MagicMock()
        self.error_logger = MagicMock()
        self.data_logger = MagicMock()
        
        # Mock dos componentes
        self.collector = MagicMock()
        self.processor = MagicMock()
        self.db_handler = MagicMock()
        
        # Configuração de teste
        self.config = {
            'tabelas': [
                {
                    'name': 'tabela_teste',
                    'prefix': 'teste',
                    'tab_code': '1',
                    'P_Keys': ['CNPJ', 'Data']
                }
            ]
        }
        
        # Inicializar o pipeline
        self.pipeline = Pipeline(
            self.execution_logger,
            self.error_logger,
            self.data_logger,
            self.collector,
            self.processor,
            self.db_handler
        )
        
    def test_initialization(self):
        """Testa se o pipeline é inicializado corretamente."""
        # Verificar se os atributos foram configurados corretamente
        self.assertEqual(self.pipeline.execution_logger, self.execution_logger)
        self.assertEqual(self.pipeline.error_logger, self.error_logger)
        self.assertEqual(self.pipeline.data_logger, self.data_logger)
        self.assertEqual(self.pipeline.collector, self.collector)
        self.assertEqual(self.pipeline.processor, self.processor)
        self.assertEqual(self.pipeline.db_handler, self.db_handler)
    
    def test_run_pipeline_success(self):
        """Testa a execução bem-sucedida do pipeline."""
        # DataFrame de teste
        test_df = CLEAN_DATAFRAME.copy()
        
        # Configurar mocks
        self.collector.collect_data.return_value = test_df
        self.processor.process_data.return_value = test_df
        self.db_handler.create_or_update_table.return_value = True
        self.db_handler.delete_insert_data.return_value = True
        
        # Chamar o método
        result = self.pipeline.run_pipeline(self.config)
        
        # Verificar o resultado
        self.assertTrue(result)
        
        # Verificar se os métodos foram chamados corretamente
        self.collector.collect_data.assert_called_once_with(self.config['tabelas'][0])
        self.processor.process_data.assert_called_once()
        self.db_handler.create_or_update_table.assert_called_once_with(test_df, 'tabela_teste')
        self.db_handler.delete_insert_data.assert_called_once_with(test_df, 'tabela_teste')
        
        # Verificar logs
        self.execution_logger.info.assert_called()
    
    def test_run_pipeline_no_data(self):
        """Testa o caso em que não há dados para processar."""
        # Configurar mock para retornar None (sem dados)
        self.collector.collect_data.return_value = None
        
        # Chamar o método
        result = self.pipeline.run_pipeline(self.config)
        
        # Verificar o resultado
        self.assertFalse(result)
        
        # Verificar se apenas o collector foi chamado e os outros métodos não
        self.collector.collect_data.assert_called_once()
        self.processor.process_data.assert_not_called()
        self.db_handler.create_or_update_table.assert_not_called()
        self.db_handler.delete_insert_data.assert_not_called()
        
        # Verificar logs
        self.execution_logger.warning.assert_called_once()
    
    def test_run_pipeline_processing_error(self):
        """Testa o caso em que ocorre um erro durante o processamento."""
        # DataFrame de teste
        test_df = CLEAN_DATAFRAME.copy()
        
        # Configurar mocks
        self.collector.collect_data.return_value = test_df
        self.processor.process_data.return_value = None  # Erro no processamento
        
        # Chamar o método
        result = self.pipeline.run_pipeline(self.config)
        
        # Verificar o resultado
        self.assertFalse(result)
        
        # Verificar se os métodos foram chamados corretamente
        self.collector.collect_data.assert_called_once()
        self.processor.process_data.assert_called_once()
        self.db_handler.create_or_update_table.assert_not_called()
        self.db_handler.delete_insert_data.assert_not_called()
        
        # Verificar logs
        self.error_logger.error.assert_called_once()
    
    def test_run_pipeline_create_table_error(self):
        """Testa o caso em que ocorre um erro ao criar a tabela."""
        # DataFrame de teste
        test_df = CLEAN_DATAFRAME.copy()
        
        # Configurar mocks
        self.collector.collect_data.return_value = test_df
        self.processor.process_data.return_value = test_df
        self.db_handler.create_or_update_table.return_value = False  # Erro ao criar tabela
        
        # Chamar o método
        result = self.pipeline.run_pipeline(self.config)
        
        # Verificar o resultado
        self.assertFalse(result)
        
        # Verificar se os métodos foram chamados corretamente
        self.collector.collect_data.assert_called_once()
        self.processor.process_data.assert_called_once()
        self.db_handler.create_or_update_table.assert_called_once()
        self.db_handler.delete_insert_data.assert_not_called()
        
        # Verificar logs
        self.error_logger.error.assert_called_once()
    
    def test_run_pipeline_insert_data_error(self):
        """Testa o caso em que ocorre um erro ao inserir os dados."""
        # DataFrame de teste
        test_df = CLEAN_DATAFRAME.copy()
        
        # Configurar mocks
        self.collector.collect_data.return_value = test_df
        self.processor.process_data.return_value = test_df
        self.db_handler.create_or_update_table.return_value = True
        self.db_handler.delete_insert_data.return_value = False  # Erro ao inserir dados
        
        # Chamar o método
        result = self.pipeline.run_pipeline(self.config)
        
        # Verificar o resultado
        self.assertFalse(result)
        
        # Verificar se os métodos foram chamados corretamente
        self.collector.collect_data.assert_called_once()
        self.processor.process_data.assert_called_once()
        self.db_handler.create_or_update_table.assert_called_once()
        self.db_handler.delete_insert_data.assert_called_once()
        
        # Verificar logs
        self.error_logger.error.assert_called_once()
    
    def test_run_pipeline_multiple_tables(self):
        """Testa a execução do pipeline com múltiplas tabelas."""
        # DataFrame de teste
        test_df = CLEAN_DATAFRAME.copy()
        
        # Configuração com múltiplas tabelas
        multi_config = {
            'tabelas': [
                {
                    'name': 'tabela_1',
                    'prefix': 'teste1',
                    'tab_code': '1',
                    'P_Keys': ['CNPJ', 'Data']
                },
                {
                    'name': 'tabela_2',
                    'prefix': 'teste2',
                    'tab_code': '2',
                    'P_Keys': ['CNPJ', 'Data']
                }
            ]
        }
        
        # Configurar mocks
        self.collector.collect_data.return_value = test_df
        self.processor.process_data.return_value = test_df
        self.db_handler.create_or_update_table.return_value = True
        self.db_handler.delete_insert_data.return_value = True
        
        # Chamar o método
        result = self.pipeline.run_pipeline(multi_config)
        
        # Verificar o resultado
        self.assertTrue(result)
        
        # Verificar se os métodos foram chamados para cada tabela
        self.assertEqual(self.collector.collect_data.call_count, 2)
        self.assertEqual(self.processor.process_data.call_count, 2)
        self.assertEqual(self.db_handler.create_or_update_table.call_count, 2)
        self.assertEqual(self.db_handler.delete_insert_data.call_count, 2)
    
    def test_run_pipeline_exception(self):
        """Testa o tratamento de exceções gerais no pipeline."""
        # Configurar mock para lançar exceção
        self.collector.collect_data.side_effect = Exception("Erro inesperado")
        
        # Chamar o método
        result = self.pipeline.run_pipeline(self.config)
        
        # Verificar o resultado
        self.assertFalse(result)
        
        # Verificar se o log de erro foi feito
        self.error_logger.error.assert_called_once()
    
    @patch('pandas.DataFrame.to_csv')
    def test_export_data_csv(self, mock_to_csv):
        """Testa a exportação de dados para CSV."""
        # DataFrame de teste
        test_df = CLEAN_DATAFRAME.copy()
        
        # Mock para o collector retornar dados
        self.collector.collect_data.return_value = test_df
        
        # Chamar o método
        result = self.pipeline.export_data(self.config, 'csv', 'pasta_teste')
        
        # Verificar o resultado
        self.assertTrue(result)
        
        # Verificar se o collector foi chamado
        self.collector.collect_data.assert_called_once()
        
        # Verificar se to_csv foi chamado
        mock_to_csv.assert_called_once()
        
        # Verificar logs
        self.execution_logger.info.assert_called()
    
    @patch('pandas.DataFrame.to_excel')
    def test_export_data_excel(self, mock_to_excel):
        """Testa a exportação de dados para Excel."""
        # DataFrame de teste
        test_df = CLEAN_DATAFRAME.copy()
        
        # Mock para o collector retornar dados
        self.collector.collect_data.return_value = test_df
        
        # Chamar o método
        result = self.pipeline.export_data(self.config, 'excel', 'pasta_teste')
        
        # Verificar o resultado
        self.assertTrue(result)
        
        # Verificar se o collector foi chamado
        self.collector.collect_data.assert_called_once()
        
        # Verificar se to_excel foi chamado
        mock_to_excel.assert_called_once()
    
    def test_export_data_invalid_format(self):
        """Testa a exportação com formato inválido."""
        # Chamar o método com formato inválido
        result = self.pipeline.export_data(self.config, 'formato_invalido', 'pasta_teste')
        
        # Verificar o resultado
        self.assertFalse(result)
        
        # Verificar se o logger foi chamado
        self.error_logger.error.assert_called_once()
    
    def test_export_data_no_data(self):
        """Testa o caso em que não há dados para exportar."""
        # Mock para o collector não retornar dados
        self.collector.collect_data.return_value = None
        
        # Chamar o método
        result = self.pipeline.export_data(self.config, 'csv', 'pasta_teste')
        
        # Verificar o resultado
        self.assertFalse(result)
        
        # Verificar logs
        self.execution_logger.warning.assert_called_once()


if __name__ == '__main__':
    unittest.main() 