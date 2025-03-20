"""
Módulo para coleta de dados de FIDCs da CVM.
"""
import os
import pandas as pd
from typing import Dict, Optional, Any, List
import logging
from datetime import datetime
from tqdm import tqdm
from src.core.scraper import CvmScraper

class CvmDataCollector:
    """
    Classe responsável pela coleta de dados de FIDCs da CVM.
    """
    
    def __init__(self, 
                 table_config: Dict[str, Any], 
                 execution_logger: logging.Logger, 
                 error_logger: logging.Logger, 
                 data_logger: logging.Logger):
        """
        Inicializa o coletor de dados.
        
        Args:
            table_config: Configuração da tabela a ser coletada
            execution_logger: Logger para o fluxo de execução
            error_logger: Logger para erros
            data_logger: Logger para operações de dados
        """
        self.table_config = table_config
        self.table_name = table_config['name']
        self.file_prefix = table_config['prefix']
        self.execution_logger = execution_logger
        self.error_logger = error_logger
        self.data_logger = data_logger
        self.url_base = 'https://dados.cvm.gov.br/dados/FIDC/DOC/INF_MENSAL/DADOS/'
    
    def collect_data(self, data_inicio: str = '2020-01-01') -> Optional[pd.DataFrame]:
        """
        Coleta dados da CVM para uma tabela específica.
        
        Args:
            data_inicio: Data de início para coleta dos dados (formato: 'YYYY-MM-DD')
            
        Returns:
            DataFrame contendo os dados coletados ou None em caso de erro
        """
        try:
            self.execution_logger.info(f"Iniciando coleta de dados para {self.table_name}")
            
            # Garantir que o diretório de dados brutos exista
            os.makedirs('data/raw', exist_ok=True)
            
            # Baixando arquivos da CVM
            df = self._importa_dados(data_inicio=data_inicio)
            
            if df is None or df.empty:
                self.data_logger.warning(f"Nenhum dado disponível para {self.table_name}")
                return None
                
            # Salvando dados brutos
            raw_file_path = f'data/raw/{self.table_name}_raw.csv'
            df.to_csv(raw_file_path, index=False)
            
            self.data_logger.info(f"Dados brutos coletados para {self.table_name}: {len(df)} registros")
            self.execution_logger.info(f"Coleta de dados para {self.table_name} finalizada com sucesso")
            
            return df
            
        except Exception as e:
            self.error_logger.error(f"Erro na coleta de dados para {self.table_name}", exc_info=True)
            return None
    
    def _importa_dados(self, data_inicio: str) -> Optional[pd.DataFrame]:
        """
        Importa dados de FIDCs da CVM para um período específico, com barra de progresso.
        
        Args:
            data_inicio: Data de início para baixar os dados (formato: 'YYYY-MM-DD')
            
        Returns:
            DataFrame contendo os dados importados ou None se não houver dados
        """
        # Formatando data input para ser usada
        data_inicio_dt = pd.to_datetime(data_inicio)

        # Datas a baixar
        data_atual = pd.to_datetime("today").replace(day=1) - pd.DateOffset(days=1)
        datas_a_baixar = pd.date_range(start=data_inicio_dt, end=data_atual, freq='M')

        # Loop para baixar arquivo de cada mês com barra de progresso
        dfs_novos = []
        
        # Configuração da barra de progresso
        total_meses = len(datas_a_baixar)
        if total_meses == 0:
            self.data_logger.warning("Nenhum período para baixar.")
            return None
            
        with tqdm(total=total_meses, desc=f"Baixando {self.table_name}", unit="mês", leave=True) as pbar:
            for data in datas_a_baixar:
                ano, mes = data.year, data.month
                try:
                    df_novo = CvmScraper.baixar_extrair_csv(
                        f"{self.url_base}inf_mensal_fidc_{ano}{mes:02d}.zip",
                        f"{self.file_prefix}_{ano}{mes:02d}.csv"
                    )
                    if df_novo is not None:
                        cnpj_col = 'CNPJ_FUNDO' if 'CNPJ_FUNDO' in df_novo.columns else 'CNPJ_FUNDO_CLASSE'
                        df_novo.rename(columns={"DT_COMPTC": "Data", cnpj_col: 'CNPJ'}, inplace=True)
                        dfs_novos.append(df_novo)
                        # Atualiza a barra de progresso com informações
                        pbar.set_postfix({"Status": "OK", "Registros": len(df_novo)})
                    else:
                        pbar.set_postfix({"Status": "VAZIO"})
                except Exception as e:
                    # Atualiza a barra de progresso com o erro
                    pbar.set_postfix({"Status": "ERRO", "Mensagem": str(e)[:50]})
                    self.error_logger.error(f"Erro ao baixar dados de {ano}/{mes:02d}: {str(e)}")
                finally:
                    pbar.update(1)

        if not dfs_novos:
            self.data_logger.warning("Nenhum dado novo encontrado.")
            return None
        
        df_novos = pd.concat(dfs_novos, ignore_index=True)
        self.data_logger.info(f"Total de {len(df_novos)} registros baixados em {len(dfs_novos)}/{total_meses} meses.")
        return df_novos 