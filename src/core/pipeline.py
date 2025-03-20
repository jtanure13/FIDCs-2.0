"""
Módulo principal para a execução do pipeline de processamento de FIDCs.
"""
import os
import pandas as pd
from typing import Dict, List, Any, Optional
import logging
from tqdm import tqdm

from src.core.logger import Logger
from src.core.collector import CvmDataCollector
from src.core.processor import DataProcessor
from src.core.database import DatabaseHandler

class FidcPipeline:
    """
    Classe principal que gerencia o pipeline completo de coleta, processamento e armazenamento
    dos dados de FIDCs da CVM.
    """
    
    def __init__(self, tables_config: List[Dict[str, Any]]):
        """
        Inicializa o pipeline de processamento.
        
        Args:
            tables_config: Lista de configurações das tabelas a serem processadas
        """
        self.tables_config = tables_config
        
        # Configuração de logging
        logger_manager = Logger()
        self.execution_logger, self.error_logger, self.data_logger = logger_manager.get_loggers()
        
        # Inicializar gerenciador de banco de dados
        self.db_handler = DatabaseHandler(
            self.execution_logger, 
            self.error_logger, 
            self.data_logger
        )
    
    def setup_directories(self) -> None:
        """
        Garante que os diretórios necessários existam.
        """
        os.makedirs('data/raw', exist_ok=True)
        os.makedirs('data/database', exist_ok=True)
        os.makedirs('backup', exist_ok=True)
        os.makedirs('duplicatas', exist_ok=True)
        self.execution_logger.info("Diretórios base criados")
    
    def process_table(self, table_config: Dict[str, Any], data_inicio: str = '2020-01-01') -> bool:
        """
        Processa uma tabela específica, executando todas as etapas do pipeline.
        
        Args:
            table_config: Configuração da tabela a ser processada
            data_inicio: Data de início para coleta dos dados (formato: 'YYYY-MM-DD')
            
        Returns:
            True se o processamento foi bem-sucedido, False caso contrário
        """
        table_name = table_config['name']
        self.execution_logger.info(f"Iniciando processamento para tabela {table_name}")
        
        # Criar instâncias específicas para esta tabela
        collector = CvmDataCollector(
            table_config, 
            self.execution_logger, 
            self.error_logger, 
            self.data_logger
        )
        processor = DataProcessor(
            table_config, 
            self.execution_logger, 
            self.error_logger, 
            self.data_logger
        )
        
        # Coleta de dados da CVM
        df = collector.collect_data(data_inicio=data_inicio)
        if df is None:
            self.execution_logger.warning(f"Nenhum dado disponível para {table_name}. Pulando para a próxima tabela.")
            return False
        
        # Processamento de dados
        df_processado = processor.process_data(df)
        if df_processado is None:
            self.execution_logger.warning(f"Problemas no processamento de dados para {table_name}. Pulando para a próxima tabela.")
            return False

        # Criando backup
        processor.create_backup(df_processado)
        
        # Criando tabelas (caso não existam) no Banco de Dados
        self.db_handler.create_or_update_table(df_processado, table_name)
        
        # Sobrescrevendo dados no banco de dados
        self.db_handler.delete_insert_data(df_processado, table_name)
        
        self.execution_logger.info(f"Processamento para tabela {table_name} finalizado com sucesso")
        return True
    
    def run(self, data_inicio: str = '2020-01-01') -> bool:
        """
        Executa o pipeline completo para todas as tabelas configuradas.
        
        Args:
            data_inicio: Data de início para coleta dos dados (formato: 'YYYY-MM-DD')
            
        Returns:
            True se a execução foi bem-sucedida, False caso contrário
        """
        try:
            self.execution_logger.info("Iniciando execução do sistema de coleta e processamento de FIDCs")
            
            # Garantir que os diretórios necessários existam
            self.setup_directories()
            
            # Contador para mostrar progresso
            total_tables = len(self.tables_config)
            successful_tables = 0
            
            print(f"🚀 Iniciando processamento de {total_tables} tabelas de FIDCs...\n")
            
            # Iterando por cada arquivo/tabela com barra de progresso
            with tqdm(total=total_tables, desc="Processando tabelas", unit="tabela", leave=True) as pbar:
                for table_config in self.tables_config:
                    table_name = table_config['name']
                    pbar.set_description(f"Processando {table_name}")
                    
                    # Processar tabela
                    success = self.process_table(table_config, data_inicio)
                    
                    # Atualizar status na barra de progresso
                    if success:
                        successful_tables += 1
                        pbar.set_postfix({"Status": "OK", "Total Sucesso": f"{successful_tables}/{total_tables}"})
                    else:
                        pbar.set_postfix({"Status": "FALHA", "Total Sucesso": f"{successful_tables}/{total_tables}"})
                    
                    pbar.update(1)
                    print("")  # Linha em branco para separar as tabelas
            
            # Resumo final
            self.execution_logger.info(f"Execução do sistema finalizada: {successful_tables}/{total_tables} tabelas processadas com sucesso")
            
            if successful_tables == total_tables:
                print(f"\n✅ Processamento concluído com sucesso! Todas as {total_tables} tabelas foram processadas.")
            else:
                print(f"\n⚠️ Processamento concluído: {successful_tables}/{total_tables} tabelas processadas com sucesso.")
                print(f"   {total_tables - successful_tables} tabelas não foram processadas corretamente. Consulte os logs para mais detalhes.")
            
            return True
            
        except Exception as e:
            self.error_logger.error("Erro durante a execução do sistema", exc_info=True)
            print(f"\n❌ Erro durante a execução: {str(e)}")
            print(f"❌ Erro durante a execução: {str(e)}")
            return False 