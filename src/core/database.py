"""
Módulo para operações de banco de dados relacionadas a FIDCs.
"""
import pandas as pd
import sqlite3
from typing import Dict, Any, Optional
import logging

class DatabaseHandler:
    """
    Classe responsável pelas operações de banco de dados para FIDCs.
    """
    
    def __init__(self, 
                 execution_logger: logging.Logger, 
                 error_logger: logging.Logger, 
                 data_logger: logging.Logger,
                 db_path: str = 'data/database/fidcs.db'):
        """
        Inicializa o gerenciador de banco de dados.
        
        Args:
            execution_logger: Logger para o fluxo de execução
            error_logger: Logger para erros
            data_logger: Logger para operações de dados
            db_path: Caminho para o arquivo do banco de dados SQLite
        """
        self.db_path = db_path
        self.execution_logger = execution_logger
        self.error_logger = error_logger
        self.data_logger = data_logger
    
    def create_or_update_table(self, df: pd.DataFrame, table_name: str) -> bool:
        """
        Cria ou atualiza uma tabela no banco de dados com base no DataFrame fornecido.
        
        Args:
            df: DataFrame contendo os dados
            table_name: Nome da tabela a ser criada/atualizada
            
        Returns:
            True se a operação foi bem-sucedida, False caso contrário
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Monta lista com as colunas e seus tipos inferidos
            tipos_sql = []
            for col in df.columns:
                if pd.api.types.is_integer_dtype(df[col]):
                    tipo = "INTEGER"
                elif pd.api.types.is_float_dtype(df[col]):
                    tipo = "REAL"
                else:
                    tipo = "TEXT"
                tipos_sql.append(f'"{col}" {tipo}')

            # Query SQL para criar a tabela
            create_table_query = f'''
            CREATE TABLE IF NOT EXISTS "{table_name}" (
                {', '.join(tipos_sql)}
            );
            '''
            
            cursor.execute(create_table_query)
            conn.commit()
            cursor.close()
            conn.close()
            
            self.execution_logger.info(f"Tabela {table_name} criada/atualizada no banco de dados")
            return True
            
        except Exception as e:
            self.error_logger.error(f"Erro ao criar/atualizar tabela {table_name}", exc_info=True)
            return False
    
    def delete_insert_data(self, df: pd.DataFrame, table_name: str) -> bool:
        """
        Deleta dados existentes para os meses presentes no DataFrame e insere os novos dados.
        
        Args:
            df: DataFrame contendo os novos dados
            table_name: Nome da tabela onde os dados serão inseridos
            
        Returns:
            True se a operação foi bem-sucedida, False caso contrário
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Obtenção dos meses para deletar e atualizar
            meses_atualizar = df['Data'].unique()
            print(f"🚨 Removendo dados antigos de {table_name} para os meses baixados.")

            for mes in meses_atualizar:
                query = f'''
                DELETE FROM "{table_name}" WHERE strftime('%Y-%m', Data) = ?
                '''
                cursor.execute(query, (mes,))

            conn.commit()

            df.to_sql(table_name, conn, if_exists='append', index=False)
            
            cursor.close()
            conn.close()
            
            self.execution_logger.info(f"Dados deletados e inseridos na tabela {table_name} para os meses baixados")
            self.data_logger.info(f"Dados inseridos em {table_name}: {len(df)} registros")
            return True
            
        except Exception as e:
            self.error_logger.error(f"Erro ao deletar/inserir dados na tabela {table_name}", exc_info=True)
            return False 