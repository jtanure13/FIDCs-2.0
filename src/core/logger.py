"""
Configuração do sistema de logging da aplicação.
"""
import os
import logging
from datetime import datetime
from typing import Tuple

class Logger:
    """
    Classe responsável pela configuração e gestão do sistema de logging.
    Fornece três tipos de logs:
    - execution_logs: para o fluxo normal de execução
    - error_logs: para erros e exceções
    - data_logs: para operações de processamento de dados
    """
    
    def __init__(self):
        """
        Inicializa o sistema de logging com três tipos de loggers.
        """
        # Criar diretórios de logs se não existirem
        os.makedirs('logs/execution_logs', exist_ok=True)
        os.makedirs('logs/error_logs', exist_ok=True)
        os.makedirs('logs/data_logs', exist_ok=True)
        
        # Data atual para nome dos arquivos
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Configurar loggers
        self.execution_logger = self._setup_execution_logger()
        self.error_logger = self._setup_error_logger()
        self.data_logger = self._setup_data_logger()
    
    def _setup_execution_logger(self) -> logging.Logger:
        """
        Configura o logger para o fluxo de execução.
        
        Returns:
            logging.Logger: Logger configurado para execução
        """
        execution_logger = logging.getLogger('execution')
        if not execution_logger.handlers:
            execution_logger.setLevel(logging.INFO)
            execution_handler = logging.FileHandler(f'logs/execution_logs/execution_{self.current_date}.log')
            execution_format = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s')
            execution_handler.setFormatter(execution_format)
            execution_logger.addHandler(execution_handler)
        return execution_logger
    
    def _setup_error_logger(self) -> logging.Logger:
        """
        Configura o logger para erros.
        
        Returns:
            logging.Logger: Logger configurado para erros
        """
        error_logger = logging.getLogger('error')
        if not error_logger.handlers:
            error_logger.setLevel(logging.ERROR)
            error_handler = logging.FileHandler(f'logs/error_logs/error_{self.current_date}.log')
            error_format = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s\n%(exc_info)s')
            error_handler.setFormatter(error_format)
            error_logger.addHandler(error_handler)
        return error_logger
    
    def _setup_data_logger(self) -> logging.Logger:
        """
        Configura o logger para operações de dados.
        
        Returns:
            logging.Logger: Logger configurado para dados
        """
        data_logger = logging.getLogger('data')
        if not data_logger.handlers:
            data_logger.setLevel(logging.INFO)
            data_handler = logging.FileHandler(f'logs/data_logs/data_{self.current_date}.log')
            data_format = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s')
            data_handler.setFormatter(data_format)
            data_logger.addHandler(data_handler)
        return data_logger
    
    def get_loggers(self) -> Tuple[logging.Logger, logging.Logger, logging.Logger]:
        """
        Retorna os três loggers configurados.
        
        Returns:
            Tuple[logging.Logger, logging.Logger, logging.Logger]: 
                execution_logger, error_logger, data_logger
        """
        return self.execution_logger, self.error_logger, self.data_logger 