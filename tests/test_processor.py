"""
Testes para o módulo processor (src.core.processor).
"""
import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock, call
import pytest
from src.core.processor import DataProcessor
from tests.fixtures.sample_data import (
    CLEAN_DATAFRAME, 
    DUPLICATED_DATAFRAME, 
    PROBLEMATIC_DATAFRAME,
    MIXED_TYPES_DATAFRAME
)

class TestDataProcessor(unittest.TestCase):
    """Testes para a classe DataProcessor."""
    
    def setUp(self):
        """Configuração que executa antes de cada teste."""
        # Mock dos loggers
        self.execution_logger = MagicMock()
        self.error_logger = MagicMock()
        self.data_logger = MagicMock()
        
        # Configuração de tabela de teste
        self.test_config = {
            "name": "tabela_teste",
            "P_Keys": ["CNPJ", "Data", "TP_FUNDO_CLASSE"]
        }
        
        # Inicializa o processador
        self.processor = DataProcessor(
            self.test_config,
            self.execution_logger,
            self.error_logger,
            self.data_logger
        )
        
        # Diretório temporário para testes
        self.temp_dir = tempfile.TemporaryDirectory()
        # Patcheando os.makedirs para usar diretório temporário
        self.makedirs_patcher = patch('os.makedirs')
        self.mock_makedirs = self.makedirs_patcher.start()
    
    def tearDown(self):
        """Limpeza após cada teste."""
        self.makedirs_patcher.stop()
        self.temp_dir.cleanup()
    
    def test_initialization(self):
        """Testa se o processador é inicializado corretamente."""
        # Verificar se os atributos foram configurados corretamente
        self.assertEqual(self.processor.execution_logger, self.execution_logger)
        self.assertEqual(self.processor.error_logger, self.error_logger)
        self.assertEqual(self.processor.data_logger, self.data_logger)
    
    def test_remove_duplicados(self):
        """Testa a remoção de registros duplicados."""
        # Usar um DataFrame com duplicatas
        df = DUPLICATED_DATAFRAME.copy()
        
        # Chamar o método
        result = self.processor.remove_duplicados(df, chaves=['CNPJ', 'Data'])
        
        # Verificar se os duplicados foram removidos
        self.assertEqual(len(result), 3)  # Deve ter 3 registros únicos
        self.assertEqual(self.data_logger.info.call_count, 1)
        
        # Teste sem nenhum duplicado
        clean_df = CLEAN_DATAFRAME.copy()
        result = self.processor.remove_duplicados(clean_df, chaves=['CNPJ', 'Data'])
        # Verificar se nada foi removido
        self.assertEqual(len(result), len(clean_df))
        
        # Teste com DataFrame vazio
        empty_df = pd.DataFrame()
        result = self.processor.remove_duplicados(empty_df, chaves=['CNPJ', 'Data'])
        # Verificar se retornou o mesmo DataFrame vazio
        self.assertTrue(result.empty)
    
    def test_remove_duplicados_with_keep_first(self):
        """Testa a remoção de registros duplicados mantendo o primeiro registro."""
        # Usar um DataFrame com duplicatas
        df = DUPLICATED_DATAFRAME.copy()
        
        # Chamar o método com keep='first'
        result = self.processor.remove_duplicados(df, chaves=['CNPJ', 'Data'], keep='first')
        
        # Verificar se os duplicados foram removidos mantendo o primeiro
        self.assertEqual(len(result), 3)  # Deve ter 3 registros únicos
        
        # Verificar se o primeiro registro foi mantido (valor deve ser diferente do método padrão)
        # No caso de duplicados, o padrão 'last' mantém o último valor
        first_kept = result[result['CNPJ'] == 'CNPJ-1']
        self.assertEqual(first_kept.iloc[0]['Valor_Float'], 100.0)  # Primeiro valor
    
    def test_remove_duplicados_error(self):
        """Testa o tratamento de erros na remoção de duplicados."""
        # Criar um DataFrame mockado que lança exceção ao chamar drop_duplicates
        df_mock = MagicMock()
        df_mock.drop_duplicates.side_effect = Exception("Erro de teste")
        
        # Chamar o método
        result = self.processor.remove_duplicados(df_mock, chaves=['CNPJ', 'Data'])
        
        # Verificar se retornou None
        self.assertIsNone(result)
        
        # Verificar se o log de erro foi feito
        self.error_logger.error.assert_called_once()
    
    def test_convert_date_columns(self):
        """Testa a conversão de colunas de data."""
        # Criar um DataFrame com coluna de data
        df = pd.DataFrame({
            'Data': ['31/01/2023', '15/02/2023', '20/03/2023'],
            'Outra_Coluna': [1, 2, 3]
        })
        
        # Chamar o método
        result = self.processor.convert_date_columns(df, date_cols=['Data'])
        
        # Verificar se as datas foram convertidas
        self.assertTrue(pd.api.types.is_datetime64_dtype(result['Data']))
        self.assertEqual(result['Data'].dt.year.iloc[0], 2023)
        self.assertEqual(result['Data'].dt.month.iloc[0], 1)
        self.assertEqual(result['Data'].dt.day.iloc[0], 31)
        
        # Verificar logs
        self.execution_logger.info.assert_called_once()
        
    def test_convert_date_columns_with_format(self):
        """Testa a conversão de colunas de data com formato específico."""
        # Criar um DataFrame com coluna de data em formato diferente
        df = pd.DataFrame({
            'Data': ['2023-01-31', '2023-02-15', '2023-03-20'],
            'Outra_Coluna': [1, 2, 3]
        })
        
        # Chamar o método com formato específico
        result = self.processor.convert_date_columns(df, date_cols=['Data'], date_format='%Y-%m-%d')
        
        # Verificar se as datas foram convertidas
        self.assertTrue(pd.api.types.is_datetime64_dtype(result['Data']))
        self.assertEqual(result['Data'].dt.year.iloc[0], 2023)
        self.assertEqual(result['Data'].dt.month.iloc[0], 1)
        self.assertEqual(result['Data'].dt.day.iloc[0], 31)
    
    def test_convert_date_columns_error(self):
        """Testa o tratamento de erros na conversão de datas."""
        # Criar um DataFrame com datas inválidas
        df = pd.DataFrame({
            'Data': ['31/01/2023', 'data_invalida', '20/03/2023'],
            'Outra_Coluna': [1, 2, 3]
        })
        
        # Chamar o método
        result = self.processor.convert_date_columns(df, date_cols=['Data'])
        
        # Verificar se retornou None
        self.assertIsNone(result)
        
        # Verificar se o log de erro foi feito
        self.error_logger.error.assert_called_once()
    
    def test_convert_numeric_columns(self):
        """Testa a conversão de colunas numéricas."""
        # Criar um DataFrame com valores numéricos como strings
        df = pd.DataFrame({
            'Coluna_Int': ['1', '2', '3'],
            'Coluna_Float': ['1,5', '2,5', '3,5'],
            'Coluna_Texto': ['A', 'B', 'C']
        })
        
        # Chamar o método
        result = self.processor.convert_numeric_columns(
            df, 
            int_cols=['Coluna_Int'], 
            float_cols=['Coluna_Float']
        )
        
        # Verificar se as colunas foram convertidas corretamente
        self.assertTrue(pd.api.types.is_integer_dtype(result['Coluna_Int']))
        self.assertTrue(pd.api.types.is_float_dtype(result['Coluna_Float']))
        self.assertEqual(result['Coluna_Float'].iloc[0], 1.5)
        
        # Verificar logs
        self.execution_logger.info.assert_called_once()
    
    def test_convert_numeric_columns_error(self):
        """Testa o tratamento de erros na conversão numérica."""
        # Criar um DataFrame com valores não-numéricos
        df = pd.DataFrame({
            'Coluna_Int': ['1', 'dois', '3'],
            'Coluna_Float': ['1,5', '2,5', '3,5']
        })
        
        # Chamar o método
        result = self.processor.convert_numeric_columns(
            df, 
            int_cols=['Coluna_Int'], 
            float_cols=['Coluna_Float']
        )
        
        # Verificar se retornou None
        self.assertIsNone(result)
        
        # Verificar se o log de erro foi feito
        self.error_logger.error.assert_called_once()
    
    def test_process_data(self):
        """Testa o processamento completo dos dados."""
        # Usar um DataFrame com dados que precisam de processamento
        df = MIXED_TYPES_DATAFRAME.copy()
        
        # Mock para os métodos individuais
        with patch.object(self.processor, 'remove_duplicados', return_value=df) as mock_remove:
            with patch.object(self.processor, 'convert_date_columns', return_value=df) as mock_convert_date:
                with patch.object(self.processor, 'convert_numeric_columns', return_value=df) as mock_convert_numeric:
                    
                    # Chamar o método
                    result = self.processor.process_data(
                        df,
                        duplicate_keys=['CNPJ', 'Data'],
                        date_cols=['Data'],
                        int_cols=['Valor_Int'],
                        float_cols=['Valor_Float']
                    )
                    
                    # Verificar se todos os métodos foram chamados
                    mock_remove.assert_called_once_with(df, ['CNPJ', 'Data'], 'last')
                    mock_convert_date.assert_called_once_with(df, ['Data'], '%d/%m/%Y')
                    mock_convert_numeric.assert_called_once_with(df, ['Valor_Int'], ['Valor_Float'])
                    
                    # Verificar se o resultado é o DataFrame esperado
                    self.assertEqual(result, df)
    
    def test_process_data_partial_error(self):
        """Testa o processo quando um dos passos falha."""
        # Usar um DataFrame com dados que precisam de processamento
        df = MIXED_TYPES_DATAFRAME.copy()
        
        # Mock para o método remove_duplicados retornar None (erro)
        with patch.object(self.processor, 'remove_duplicados', return_value=None) as mock_remove:
            
            # Chamar o método
            result = self.processor.process_data(
                df,
                duplicate_keys=['CNPJ', 'Data'],
                date_cols=['Data'],
                int_cols=['Valor_Int'],
                float_cols=['Valor_Float']
            )
            
            # Verificar se o método removeDuplicados foi chamado
            mock_remove.assert_called_once()
            
            # Verificar se retornou None devido ao erro
            self.assertIsNone(result)
            
            # Verificar se o log de erro foi feito
            self.error_logger.error.assert_called_once()
    
    def test_process_data_normal(self):
        """Testa processamento de dados sem duplicatas."""
        # Dados de teste sem duplicatas
        test_data = pd.DataFrame({
            'CNPJ': ['123', '456', '789'],
            'Data': ['2023-01-01', '2023-01-01', '2023-01-01'],
            'TP_FUNDO_CLASSE': ['A', 'B', 'C'],
            'Valor': [100, 200, 300]
        })
        
        # Mockando o método _check_duplicatas para isolar o teste
        with patch.object(self.processor, '_check_duplicatas', return_value=test_data):
            result = self.processor.process_data(test_data)
            
            # Verifica se o resultado está correto
            self.assertIsNotNone(result)
            self.assertEqual(len(result), 3)
            # Verifica se os logs foram chamados corretamente
            self.execution_logger.info.assert_called()
            self.data_logger.info.assert_called()
    
    def test_process_data_with_duplicates(self):
        """Testa processamento de dados com duplicatas."""
        # Dados de teste com duplicatas
        test_data_with_duplicates = pd.DataFrame({
            'CNPJ': ['123', '123', '789'],
            'Data': ['2023-01-01', '2023-01-01', '2023-01-01'],
            'TP_FUNDO_CLASSE': ['A', '', 'C'],
            'Valor': [100, 200, 300]
        })
        
        # Cria um DataFrame resultante já tratado (2 registros, sem a duplicata)
        expected_result = pd.DataFrame({
            'CNPJ': ['123', '789'],
            'Data': ['2023-01-01', '2023-01-01'],
            'TP_FUNDO_CLASSE': ['A', 'C'],
            'Valor': [100, 300]
        })
        
        # Mockando o método _check_duplicatas
        with patch.object(self.processor, '_check_duplicatas', return_value=expected_result):
            result = self.processor.process_data(test_data_with_duplicates)
            
            # Verifica se a duplicata foi removida
            self.assertEqual(len(result), 2)
            # Verifica se os logs foram chamados corretamente
            self.execution_logger.info.assert_called()
    
    def test_process_data_empty_result(self):
        """Testa comportamento quando o processamento resulta em DataFrame vazio."""
        test_data = pd.DataFrame({
            'CNPJ': ['123'],
            'Data': ['2023-01-01'],
            'TP_FUNDO_CLASSE': ['A'],
            'Valor': [100]
        })
        
        # Mockando _check_duplicatas para retornar um DataFrame vazio
        with patch.object(self.processor, '_check_duplicatas', return_value=pd.DataFrame()):
            result = self.processor.process_data(test_data)
            
            # Verifica que o resultado é None quando o processamento retorna vazio
            self.assertIsNone(result)
            # Verifica se o log de aviso foi chamado
            self.data_logger.warning.assert_called()
    
    def test_process_data_error(self):
        """Testa tratamento de erros durante o processamento."""
        test_data = pd.DataFrame({
            'CNPJ': ['123'],
            'Data': ['2023-01-01'],
            'TP_FUNDO_CLASSE': ['A'],
            'Valor': [100]
        })
        
        # Mockando _check_duplicatas para lançar uma exceção
        with patch.object(self.processor, '_check_duplicatas', side_effect=Exception("Erro de teste")):
            result = self.processor.process_data(test_data)
            
            # Verifica que o resultado é None quando ocorre um erro
            self.assertIsNone(result)
            # Verifica se o log de erro foi chamado
            self.error_logger.error.assert_called()
    
    def test_create_backup(self):
        """Testa criação de backup dos dados processados."""
        test_data = pd.DataFrame({
            'CNPJ': ['123'],
            'Data': ['2023-01-01'],
            'TP_FUNDO_CLASSE': ['A'],
            'Valor': [100]
        })
        
        # Mockando pd.DataFrame.to_csv para não realmente salvar arquivo
        with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
            success = self.processor.create_backup(test_data)
            
            # Verifica se o backup foi criado com sucesso
            self.assertTrue(success)
            # Verifica se to_csv foi chamado
            mock_to_csv.assert_called_once()
            # Verifica se os logs foram chamados corretamente
            self.execution_logger.info.assert_called()
    
    def test_create_backup_error(self):
        """Testa tratamento de erros durante criação de backup."""
        test_data = pd.DataFrame({
            'CNPJ': ['123'],
            'Data': ['2023-01-01'],
            'TP_FUNDO_CLASSE': ['A'],
            'Valor': [100]
        })
        
        # Mockando pd.DataFrame.to_csv para lançar exceção
        with patch.object(pd.DataFrame, 'to_csv', side_effect=Exception("Erro ao salvar")):
            success = self.processor.create_backup(test_data)
            
            # Verifica que o resultado é False quando ocorre um erro
            self.assertFalse(success)
            # Verifica se o log de erro foi chamado
            self.error_logger.error.assert_called()
    
    def test_check_duplicatas_basic(self):
        """Testa o fluxo básico do método _check_duplicatas."""
        # Um DataFrame simples sem duplicatas
        test_data = pd.DataFrame({
            'CNPJ': ['123', '456'],
            'Data': ['2023-01-01', '2023-01-01'],
            'TP_FUNDO_CLASSE': ['A', 'B'],
            'Valor': [100, 200]
        })
        
        # Chama o método diretamente
        result = self.processor._check_duplicatas(test_data)
        
        # Verifica se os dados foram processados corretamente
        self.assertEqual(len(result), 2)
        # Verifica se a coluna Data foi convertida para formato YYYY-MM
        self.assertEqual(result['Data'][0], '2023-01')
    
    def test_check_duplicatas_empty(self):
        """Testa comportamento com DataFrame vazio."""
        # DataFrame vazio
        empty_df = pd.DataFrame()
        
        # Chama o método
        result = self.processor._check_duplicatas(empty_df)
        
        # Verifica que o resultado é None para DataFrame vazio
        self.assertIsNone(result)
        # Verifica se o log apropriado foi chamado
        self.data_logger.warning.assert_called()

if __name__ == '__main__':
    unittest.main() 