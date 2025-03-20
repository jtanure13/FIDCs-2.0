"""
Testes para o módulo database (src.core.database).
"""
import unittest
import pandas as pd
import sqlite3
from unittest.mock import patch, MagicMock, call
import pytest
from src.core.database import DatabaseHandler
from tests.fixtures.sample_data import CLEAN_DATAFRAME, MULTI_MONTH_DATAFRAME

class TestDatabaseHandler(unittest.TestCase):
    """Testes para a classe DatabaseHandler."""
    
    def setUp(self):
        """Configuração que executa antes de cada teste."""
        # Mock dos loggers
        self.execution_logger = MagicMock()
        self.error_logger = MagicMock()
        self.data_logger = MagicMock()
        
        # Usar banco de dados em memória para testes
        self.db_handler = DatabaseHandler(
            self.execution_logger,
            self.error_logger,
            self.data_logger,
            db_path=':memory:'
        )
        
        # DataFrame de teste
        self.test_df = CLEAN_DATAFRAME.copy()
        
    def test_initialization(self):
        """Testa se o handler é inicializado corretamente."""
        # Verificar se os atributos foram configurados corretamente
        self.assertEqual(self.db_handler.db_path, ':memory:')
        self.assertEqual(self.db_handler.execution_logger, self.execution_logger)
        self.assertEqual(self.db_handler.error_logger, self.error_logger)
        self.assertEqual(self.db_handler.data_logger, self.data_logger)
    
    @patch('sqlite3.connect')
    def test_create_or_update_table(self, mock_connect):
        """Testa a criação/atualização de tabela no banco de dados."""
        # Configurar mocks para o cursor e conexão
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        # Chamar o método
        result = self.db_handler.create_or_update_table(self.test_df, 'tabela_teste')
        
        # Verificar o resultado
        self.assertTrue(result)
        
        # Verificar se o connect foi chamado com o caminho correto
        mock_connect.assert_called_once_with(':memory:')
        
        # Verificar se o cursor foi executado
        mock_cursor.execute.assert_called_once()
        
        # Verificar se a query CREATE TABLE foi formada corretamente
        query = mock_cursor.execute.call_args[0][0]
        self.assertIn('CREATE TABLE IF NOT EXISTS "tabela_teste"', query)
        self.assertIn('"CNPJ" TEXT', query)
        self.assertIn('"Data" TEXT', query)
        self.assertIn('"TP_FUNDO_CLASSE" TEXT', query)
        self.assertIn('"Valor_Int" INTEGER', query)
        self.assertIn('"Valor_Float" REAL', query)
        
        # Verificar se o commit e close foram chamados
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
        
        # Verificar se os logs foram feitos
        self.execution_logger.info.assert_called_once()
    
    @patch('sqlite3.connect')
    def test_create_or_update_table_error(self, mock_connect):
        """Testa o tratamento de erros na criação/atualização de tabela."""
        # Configurar mock para lançar exceção
        mock_connect.side_effect = Exception("Erro de teste")
        
        # Chamar o método
        result = self.db_handler.create_or_update_table(self.test_df, 'tabela_teste')
        
        # Verificar o resultado
        self.assertFalse(result)
        
        # Verificar se os logs de erro foram feitos
        self.error_logger.error.assert_called_once()
    
    def test_create_table_diferent_column_types(self):
        """Testa se os tipos de coluna são inferidos corretamente para diferentes tipos de dados."""
        # Criar um DataFrame com diferentes tipos de dados
        df = pd.DataFrame({
            'Col_Int': [1, 2, 3],
            'Col_Float': [1.1, 2.2, 3.3],
            'Col_Str': ['a', 'b', 'c'],
            'Col_Bool': [True, False, True],
            'Col_Date': pd.date_range('2023-01-01', periods=3),
            'Col_Mixed': [1, 'a', 2.5]  # Deve inferir como TEXT
        })
        
        with patch('sqlite3.connect') as mock_connect:
            # Configurar mocks para o cursor e conexão
            mock_cursor = MagicMock()
            mock_conn = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_connect.return_value = mock_conn
            
            # Chamar o método
            self.db_handler.create_or_update_table(df, 'tabela_teste')
            
            # Verificar a query CREATE TABLE
            query = mock_cursor.execute.call_args[0][0]
            
            # Verificar os tipos inferidos
            self.assertIn('"Col_Int" INTEGER', query)
            self.assertIn('"Col_Float" REAL', query)
            self.assertIn('"Col_Str" TEXT', query)
            self.assertIn('"Col_Bool" TEXT', query)  # Booleanos são armazenados como texto em SQLite
            self.assertIn('"Col_Date" TEXT', query)  # Datas são armazenadas como texto
            self.assertIn('"Col_Mixed" TEXT', query)  # Tipo misto é armazenado como texto
    
    @patch('sqlite3.connect')
    def test_delete_insert_data(self, mock_connect):
        """Testa a deleção e inserção de dados."""
        # Usar um DataFrame com apenas um mês
        df = self.test_df.copy()
        
        # Configurar mocks para o cursor e conexão
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        # Mock para to_sql
        with patch.object(pd.DataFrame, 'to_sql') as mock_to_sql:
            # Chamar o método
            result = self.db_handler.delete_insert_data(df, 'tabela_teste')
            
            # Verificar o resultado
            self.assertTrue(result)
            
            # Verificar se o connect foi chamado com o caminho correto
            mock_connect.assert_called_once_with(':memory:')
            
            # Verificar se o cursor foi executado para cada mês único
            mock_cursor.execute.assert_called_once()
            
            # Verificar a query DELETE
            delete_query = mock_cursor.execute.call_args[0][0]
            self.assertIn('DELETE FROM "tabela_teste"', delete_query)
            
            # Verificar se to_sql foi chamado corretamente
            mock_to_sql.assert_called_once_with(
                'tabela_teste', mock_conn, if_exists='append', index=False
            )
            
            # Verificar se o commit e close foram chamados
            mock_conn.commit.assert_called_once()
            mock_cursor.close.assert_called_once()
            mock_conn.close.assert_called_once()
            
            # Verificar se os logs foram feitos
            self.execution_logger.info.assert_called_once()
            self.data_logger.info.assert_called_once()
    
    @patch('sqlite3.connect')
    def test_delete_insert_data_multi_month(self, mock_connect):
        """Testa a deleção e inserção de dados para múltiplos meses."""
        # Usar um DataFrame com dois meses diferentes
        df = MULTI_MONTH_DATAFRAME.copy()
        
        # Configurar mocks para o cursor e conexão
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        # Mock para to_sql
        with patch.object(pd.DataFrame, 'to_sql') as mock_to_sql:
            # Chamar o método
            result = self.db_handler.delete_insert_data(df, 'tabela_teste')
            
            # Verificar o resultado
            self.assertTrue(result)
            
            # Verificar se o cursor foi executado para cada mês único (2 vezes)
            self.assertEqual(mock_cursor.execute.call_count, 2)
            
            # Verificar se to_sql foi chamado uma vez
            mock_to_sql.assert_called_once()
    
    @patch('sqlite3.connect')
    def test_delete_insert_data_error(self, mock_connect):
        """Testa o tratamento de erros na deleção/inserção de dados."""
        # Configurar mock para lançar exceção
        mock_connect.side_effect = Exception("Erro de teste")
        
        # Chamar o método
        result = self.db_handler.delete_insert_data(self.test_df, 'tabela_teste')
        
        # Verificar o resultado
        self.assertFalse(result)
        
        # Verificar se os logs de erro foram feitos
        self.error_logger.error.assert_called_once()


if __name__ == '__main__':
    unittest.main() 