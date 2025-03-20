"""
Testes para o módulo logger (src.core.logger).
"""
import unittest
import os
import logging
from unittest.mock import patch, MagicMock, call
import pytest
from datetime import datetime
from src.core.logger import Logger

class TestLogger(unittest.TestCase):
    """Testes para a classe Logger."""
    
    def setUp(self):
        """Configuração que executa antes de cada teste."""
        # Patch para evitar criação de diretórios reais
        self.makedirs_patcher = patch('os.makedirs')
        self.mock_makedirs = self.makedirs_patcher.start()
        
        # Patch para evitar criação de arquivos de log reais
        self.file_handler_patcher = patch('logging.FileHandler')
        self.mock_file_handler = self.file_handler_patcher.start()
        mock_handler_instance = MagicMock()
        self.mock_file_handler.return_value = mock_handler_instance
        
        # Patch para os loggers
        self.logger_patcher = patch('logging.getLogger')
        self.mock_logger = self.logger_patcher.start()
        mock_logger_instance = MagicMock()
        self.mock_logger.return_value = mock_logger_instance
        
        # Patch para datetime.now
        self.datetime_patcher = patch('src.core.logger.datetime')
        self.mock_datetime = self.datetime_patcher.start()
        mock_now = MagicMock()
        mock_now.strftime.return_value = '2023-01-01'
        self.mock_datetime.now.return_value = mock_now
        
    def tearDown(self):
        """Limpeza após cada teste."""
        self.makedirs_patcher.stop()
        self.file_handler_patcher.stop()
        self.logger_patcher.stop()
        self.datetime_patcher.stop()
    
    def test_logger_initialization(self):
        """Testa se o logger é inicializado corretamente."""
        # Inicializar o logger
        logger = Logger()
        
        # Verificar se os diretórios foram criados
        expected_calls = [
            call('logs/execution_logs', exist_ok=True),
            call('logs/error_logs', exist_ok=True),
            call('logs/data_logs', exist_ok=True)
        ]
        self.mock_makedirs.assert_has_calls(expected_calls, any_order=True)
        
        # Verificar se os loggers foram configurados
        self.assertEqual(self.mock_logger.call_count, 3)
        self.mock_logger.assert_any_call('execution')
        self.mock_logger.assert_any_call('error')
        self.mock_logger.assert_any_call('data')
    
    def test_logger_file_creation(self):
        """Testa se os arquivos de log são criados corretamente."""
        # Inicializar o logger
        logger = Logger()
        
        # Verificar se os FileHandlers foram criados com os caminhos corretos
        expected_calls = [
            call('logs/execution_logs/execution_2023-01-01.log'),
            call('logs/error_logs/error_2023-01-01.log'),
            call('logs/data_logs/data_2023-01-01.log')
        ]
        self.mock_file_handler.assert_has_calls(expected_calls, any_order=True)
    
    def test_get_loggers(self):
        """Testa o método get_loggers."""
        # Inicializar o logger
        logger = Logger()
        
        # Obter os loggers
        execution_logger, error_logger, data_logger = logger.get_loggers()
        
        # Verificar se os loggers retornados são os esperados
        self.assertEqual(execution_logger, logger.execution_logger)
        self.assertEqual(error_logger, logger.error_logger)
        self.assertEqual(data_logger, logger.data_logger)
    
    def test_logger_formatter(self):
        """Testa se os formatadores são configurados corretamente."""
        # Patch para capturar os formatadores
        with patch('logging.Formatter') as mock_formatter:
            # Inicializar o logger
            logger = Logger()
            
            # Verificar se os formatadores foram criados com os formatos corretos
            expected_formats = [
                '[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s',
                '[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s\n%(exc_info)s',
                '[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s'
            ]
            
            format_calls = [call[0][0] for call in mock_formatter.call_args_list]
            for expected_format in expected_formats:
                self.assertIn(expected_format, format_calls)
    
    def test_handler_added_to_logger(self):
        """Testa se os handlers são adicionados aos loggers."""
        # Inicializar o logger
        logger = Logger()
        
        # Verificar se os handlers foram adicionados aos loggers
        mock_logger_instance = self.mock_logger.return_value
        self.assertEqual(mock_logger_instance.addHandler.call_count, 3)
    
    def test_logger_levels(self):
        """Testa se os níveis de log são configurados corretamente."""
        # Inicializar o logger
        logger = Logger()
        
        # Verificar se os níveis foram configurados corretamente
        mock_logger_instance = self.mock_logger.return_value
        mock_logger_instance.setLevel.assert_any_call(logging.INFO)
        mock_logger_instance.setLevel.assert_any_call(logging.ERROR)


if __name__ == '__main__':
    unittest.main() 