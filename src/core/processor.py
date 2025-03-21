"""
Módulo para processamento de dados de FIDCs.
"""
import os
import pandas as pd
from typing import Dict, List, Optional, Any
import logging
<<<<<<< HEAD
import time
from contextlib import contextmanager

# Dicionário para armazenar métricas de tempo do processador
METRICAS_TEMPO_PROCESSOR = {
    'verificacao_duplicatas': [],
    'tratamento_dados': [],
    'backup': [],
    'total': []
}

@contextmanager
def timer(operacao: str):
    """
    Context manager para medir o tempo de execução de operações.
    
    Args:
        operacao: Nome da operação sendo medida
    """
    start_time = time.time()
    try:
        yield
    finally:
        elapsed_time = time.time() - start_time
        METRICAS_TEMPO_PROCESSOR[operacao].append(elapsed_time)

def get_metricas_tempo_processor() -> Dict[str, Dict[str, float]]:
    """
    Retorna estatísticas das métricas de tempo do processador.
    """
    stats = {}
    for operacao, tempos in METRICAS_TEMPO_PROCESSOR.items():
        if tempos:
            stats[operacao] = {
                'media': sum(tempos) / len(tempos),
                'min': min(tempos),
                'max': max(tempos),
                'total': sum(tempos),
                'contagem': len(tempos)
            }
    return stats
=======
>>>>>>> 24e81b5cb8f77a7693080e3f5a65d60a51c455f8

class DataProcessor:
    """
    Classe responsável pelo processamento e limpeza dos dados coletados da CVM.
    """
    
    def __init__(self, 
                 table_config: Dict[str, Any], 
                 execution_logger: logging.Logger, 
                 error_logger: logging.Logger, 
                 data_logger: logging.Logger):
        """
        Inicializa o processador de dados.
        
        Args:
            table_config: Configuração da tabela a ser processada
            execution_logger: Logger para o fluxo de execução
            error_logger: Logger para erros
            data_logger: Logger para operações de dados
        """
        self.table_config = table_config
        self.table_name = table_config['name']
        self.p_keys = table_config['P_Keys']
        self.execution_logger = execution_logger
        self.error_logger = error_logger
        self.data_logger = data_logger
    
    def process_data(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """
        Processa e limpa os dados coletados.
        
        Args:
            df: DataFrame contendo os dados brutos
            
        Returns:
            DataFrame processado ou None em caso de erro
        """
        try:
<<<<<<< HEAD
            with timer('total'):
                self.execution_logger.info(f"Iniciando processamento de dados para {self.table_name}")
                
                # Verificando e tratando duplicatas
                with timer('verificacao_duplicatas'):
                    df_processado = self._check_duplicatas(df)
                
                if df_processado is None or df_processado.empty:
                    self.data_logger.warning(f"Problemas no processamento de dados para {self.table_name}")
                    return None
                
                # Tratamento adicional dos dados
                with timer('tratamento_dados'):
                    # Converte data para datetime e formata
                    df_processado['Data'] = pd.to_datetime(df_processado['Data'])
                    df_processado['Data'] = df_processado['Data'].dt.strftime('%Y-%m')
                
                self.data_logger.info(f"Dados processados para {self.table_name}: {len(df_processado)} registros")
                
                # Log das métricas de tempo
                stats = get_metricas_tempo_processor()
                self.execution_logger.info(f"Métricas de tempo para {self.table_name}:")
                for operacao, metricas in stats.items():
                    self.execution_logger.info(f"  {operacao}:")
                    for metrica, valor in metricas.items():
                        if isinstance(valor, (int, float)):
                            self.execution_logger.info(f"    {metrica}: {valor:.2f} segundos")
                        else:
                            self.execution_logger.info(f"    {metrica}: {valor}")
                
                return df_processado
=======
            self.execution_logger.info(f"Iniciando processamento de dados para {self.table_name}")
            
            # Verificando e tratando duplicatas
            df_processado = self._check_duplicatas(df)
            
            if df_processado is None or df_processado.empty:
                self.data_logger.warning(f"Problemas no processamento de dados para {self.table_name}")
                return None
            
            self.data_logger.info(f"Dados processados para {self.table_name}: {len(df_processado)} registros")
            self.execution_logger.info(f"Processamento de dados para {self.table_name} finalizado com sucesso")
            
            return df_processado
>>>>>>> 24e81b5cb8f77a7693080e3f5a65d60a51c455f8
            
        except Exception as e:
            self.error_logger.error(f"Erro no processamento de dados para {self.table_name}", exc_info=True)
            return None
    
    def create_backup(self, df: pd.DataFrame) -> bool:
        """
        Cria um backup dos dados processados.
        
        Args:
            df: DataFrame contendo os dados processados
            
        Returns:
            True se o backup foi criado com sucesso, False caso contrário
        """
        try:
<<<<<<< HEAD
            with timer('backup'):
                self.execution_logger.info(f"Criando backup para {self.table_name}")
                
                # Garantir que o diretório de backup exista
                os.makedirs('backup', exist_ok=True)
                
                # Salvando backup
                backup_file_path = f'backup/{self.table_name}.csv'
                df.to_csv(backup_file_path, index=False)
                
                self.execution_logger.info(f"Backup para {self.table_name} criado com sucesso")
                return True
=======
            self.execution_logger.info(f"Criando backup para {self.table_name}")
            
            # Garantir que o diretório de backup exista
            os.makedirs('backup', exist_ok=True)
            
            # Salvando backup
            backup_file_path = f'backup/{self.table_name}.csv'
            df.to_csv(backup_file_path, index=False)
            
            self.execution_logger.info(f"Backup para {self.table_name} criado com sucesso")
            return True
>>>>>>> 24e81b5cb8f77a7693080e3f5a65d60a51c455f8
            
        except Exception as e:
            self.error_logger.error(f"Erro ao criar backup para {self.table_name}", exc_info=True)
            return False
    
    def _check_duplicatas(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """
        Verifica e trata duplicatas nos dados importados.
        
        Args:
            df: DataFrame a ser verificado
            
        Returns:
            DataFrame tratado sem duplicatas problemáticas ou None em caso de erro
        """
        # Cria diretório para duplicatas se não existir
        os.makedirs('duplicatas', exist_ok=True)
        
        self.execution_logger.info(f"Verificando duplicatas para {self.table_name}")
        
<<<<<<< HEAD
        # Trata a coluna TP_FUNDO_CLASSE antes de qualquer outra operação
        if 'TP_FUNDO_CLASSE' in df.columns:
            # Converte para string e trata valores ausentes
            df['TP_FUNDO_CLASSE'] = df['TP_FUNDO_CLASSE'].astype(str)
            df['TP_FUNDO_CLASSE'] = df['TP_FUNDO_CLASSE'].replace({'nan': 'Sem Classificação', '': 'Sem Classificação'})
        
=======
>>>>>>> 24e81b5cb8f77a7693080e3f5a65d60a51c455f8
        # Cria uma cópia da lista para não modificar a original
        p_keys_check = self.p_keys.copy()
        if 'TP_FUNDO_CLASSE' in p_keys_check:
            p_keys_check.remove('TP_FUNDO_CLASSE')
        
        if not df.empty:
            # Duplicatas nas chaves CNPJ e Data
            duplicados_chave = df[df.duplicated(subset=p_keys_check, keep=False)]
            if not duplicados_chave.empty:
                self.data_logger.warning(f"Duplicatas detectadas nas chaves primárias para {self.table_name}")
            
                # Duplicatas sem TP_CLASSE_FUNDO
                duplicados_sem_classe = duplicados_chave[
<<<<<<< HEAD
                    duplicados_chave['TP_FUNDO_CLASSE'] == 'Sem Classificação'
=======
                    duplicados_chave['TP_FUNDO_CLASSE'].isnull() | (duplicados_chave['TP_FUNDO_CLASSE'] == "")
>>>>>>> 24e81b5cb8f77a7693080e3f5a65d60a51c455f8
                ]
                
                # Remove duplicatas SEM TP_FUNDO_CLASSE do DataFrame original
                if not duplicados_sem_classe.empty:
                    self.data_logger.warning(f"{len(duplicados_sem_classe)} duplicatas SEM TP_FUNDO_CLASSE detectadas para {self.table_name}")
                    duplicados_sem_classe.to_csv(f'duplicatas/dupli_sem_tp_fundo_classe_{self.table_name}.csv', index=False)
                    df = df.drop(duplicados_sem_classe.index)
                    self.execution_logger.info(f"Duplicatas SEM TP_FUNDO_CLASSE removidas para {self.table_name}")

                # Duplicatas com TP_FUNDO_CLASSE preenchido
                duplicados_com_classe = duplicados_chave[
<<<<<<< HEAD
                    duplicados_chave['TP_FUNDO_CLASSE'] != 'Sem Classificação'
=======
                    ~(duplicados_chave['TP_FUNDO_CLASSE'].isnull() | (duplicados_chave['TP_FUNDO_CLASSE'] == ""))
>>>>>>> 24e81b5cb8f77a7693080e3f5a65d60a51c455f8
                ]

                # Avalia se duplicatas com TP_FUNDO_CLASSE preenchido realmente diferem nesse campo
                problemas_classe_preenchida = duplicados_com_classe[
                    duplicados_com_classe.duplicated(subset=['CNPJ', 'Data', 'TP_FUNDO_CLASSE'], keep=False)
                ]

                if not problemas_classe_preenchida.empty:
                    cnpjs_unicos = problemas_classe_preenchida['CNPJ'].nunique()
                    if cnpjs_unicos > 250:
                        self.error_logger.error(f"{cnpjs_unicos} CNPJs com duplicatas COM TP_FUNDO_CLASSE iguais detectadas para {self.table_name}")
                        problemas_classe_preenchida.to_csv(f'duplicatas/dupli_classe_repetida_{self.table_name}.csv', index=False)
                        return None
                    else:
                        df = df.drop(problemas_classe_preenchida.index)
                        self.data_logger.warning(f"{cnpjs_unicos} CNPJs com duplicatas para {self.table_name}. Dentro do limite - seguimos.")

                self.execution_logger.info(f"Tratamento das duplicatas finalizado com sucesso para {self.table_name}")
            else:
                self.execution_logger.info(f"Nenhuma duplicata detectada nas chaves primárias para {self.table_name}")
<<<<<<< HEAD
            
=======

            # Insere valor para termos Chaves Primárias não nulas
            df['TP_FUNDO_CLASSE'] = df['TP_FUNDO_CLASSE'].fillna('Sem Classificação')
            # Converte data para datetime
            df['Data'] = pd.to_datetime(df['Data'])
            # Data para yyyy-mm
            df['Data'] = df['Data'].dt.strftime('%Y-%m')
>>>>>>> 24e81b5cb8f77a7693080e3f5a65d60a51c455f8
            return df
        else:
            self.data_logger.warning(f"DataFrame vazio para {self.table_name}")
            return None 