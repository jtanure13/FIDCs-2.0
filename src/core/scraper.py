"""
<<<<<<< HEAD
Módulo para scraping de dados da CVM com otimizações de performance e tratamento de erros.
=======
Módulo para scraping de dados da CVM.
>>>>>>> 24e81b5cb8f77a7693080e3f5a65d60a51c455f8
"""
import pandas as pd
import requests
import zipfile
<<<<<<< HEAD
import gc
from io import BytesIO
from typing import Optional, List, Dict, Tuple, Set
from datetime import datetime
import logging
from pathlib import Path
import hashlib
from tenacity import retry, stop_after_attempt, wait_exponential
import requests_cache
from functools import lru_cache
import os
import numpy as np
import time
from contextlib import contextmanager

# Configuração de logging
logger = logging.getLogger(__name__)

# Configuração do cache de requisições
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)
requests_cache.install_cache(
    str(CACHE_DIR / "cvm_cache"),
    backend="sqlite",
    expire_after=86400  # Cache expira após 24 horas
)

# Dicionário para armazenar métricas de tempo
METRICAS_TEMPO = {
    'download': [],
    'processamento': [],
    'otimizacao': [],
    'cache_save': [],
    'cache_load': [],
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
        METRICAS_TEMPO[operacao].append(elapsed_time)
        logger.info(f"Tempo de {operacao}: {elapsed_time:.2f} segundos")

def get_metricas_tempo() -> Dict[str, Dict[str, float]]:
    """
    Retorna estatísticas das métricas de tempo.
    
    Returns:
        Dicionário com estatísticas de tempo para cada operação
    """
    stats = {}
    for operacao, tempos in METRICAS_TEMPO.items():
        if tempos:
            stats[operacao] = {
                'media': np.mean(tempos),
                'min': np.min(tempos),
                'max': np.max(tempos),
                'total': np.sum(tempos),
                'contagem': len(tempos)
            }
    return stats
=======
from io import BytesIO
from typing import Optional, List
from datetime import datetime
>>>>>>> 24e81b5cb8f77a7693080e3f5a65d60a51c455f8

# Dicionário que mapeia cada arquivo CSV ao seu nome de tabela
ARQUIVOS_FONTE_PROCESSADO = {
    "inf_mensal_fidc_tab_I_": "Características Fundo",
    "inf_mensal_fidc_tab_II_": "Carteira Ativos",
    "inf_mensal_fidc_tab_III_": "Passivos e Derivativos",
    "inf_mensal_fidc_tab_IV_": "Patrimônio Líquido",
    "inf_mensal_fidc_tab_V_": "Prazos Créditos",
    "inf_mensal_fidc_tab_VI_": "Inadimplência",
    "inf_mensal_fidc_tab_VII_": "Cedentes e Tomadores",
    "inf_mensal_fidc_tab_IX_": "Preços Mercado",
    "inf_mensal_fidc_tab_X_": "Risco Crédito",
    "inf_mensal_fidc_tab_X_1_": "Classes e Cotistas",
    "inf_mensal_fidc_tab_X_1_1_": "Distribuição Cotistas",
    "inf_mensal_fidc_tab_X_2_": "Cotas e Valores",
    "inf_mensal_fidc_tab_X_3_": "Rentabilidade",
    "inf_mensal_fidc_tab_X_4_": "Operações Estruturadas",
    "inf_mensal_fidc_tab_X_5_": "Liquidez Ativos",
    "inf_mensal_fidc_tab_X_6_": "Performance Fundo",
    "inf_mensal_fidc_tab_X_7_": "Garantias e Seguros"
}

<<<<<<< HEAD
# Colunas que não devem ser convertidas para categoria
COLUNAS_NAO_CATEGORIA = {
    'CNPJ', 'CNPJ_ADMIN', 'CNPJ_GESTOR', 'CPF_CNPJ_COTISTA',
    'Data', 'DT_COMPTC', 'DT_INI_EXERC', 'DT_FIM_EXERC', 'TP_FUNDO_CLASSE'
}

class CvmScraper:
    """
    Classe responsável pelo scraping de dados da CVM com otimizações de performance.
    """
    
    CHUNK_SIZE = 10000  # Tamanho do chunk para processamento de arquivos grandes
    MAX_RETRIES = 3    # Número máximo de tentativas para download
    
    @staticmethod
    def _get_cache_path(url: str, nome_arquivo: str) -> Path:
        """
        Gera o caminho do arquivo de cache baseado na URL e nome do arquivo.
        """
        hash_str = hashlib.md5(f"{url}_{nome_arquivo}".encode()).hexdigest()
        return CACHE_DIR / f"data_{hash_str}.parquet"
    
    @staticmethod
    def _validate_zip_file(content: bytes) -> bool:
        """
        Valida se o conteúdo do arquivo ZIP é válido.
        """
        try:
            with zipfile.ZipFile(BytesIO(content)) as zf:
                return zf.testzip() is None
        except zipfile.BadZipFile:
            return False
    
    @staticmethod
    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        reraise=True
    )
    def _download_file(url: str) -> bytes:
        """
        Baixa um arquivo com retry em caso de falha.
        """
        with timer('download'):
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                return response.content
            except requests.exceptions.RequestException as e:
                logger.error(f"Erro ao baixar arquivo de {url}: {str(e)}")
                raise
    
    @staticmethod
    def _should_convert_to_category(series: pd.Series, col_name: str) -> bool:
        """
        Determina se uma coluna deve ser convertida para categoria.
        """
        # Não converter colunas específicas
        if col_name in COLUNAS_NAO_CATEGORIA:
            return False
            
        # Não converter se a coluna já é categoria
        if isinstance(series.dtype, pd.CategoricalDtype):
            return False
            
        # Não converter se a coluna tem muitos valores únicos
        if series.nunique() / len(series) >= 0.5:
            return False
            
        # Não converter se a coluna tem valores numéricos
        if pd.api.types.is_numeric_dtype(series):
            return False
            
        return True
    
    @staticmethod
    def _optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        Otimiza o uso de memória do DataFrame com tratamento seguro para categorias.
        """
        for col in df.columns:
            try:
                # Não otimiza colunas específicas
                if col in COLUNAS_NAO_CATEGORIA:
                    continue
                
                # Trata valores ausentes antes de qualquer conversão
                if df[col].isna().any():
                    if pd.api.types.is_numeric_dtype(df[col]):
                        df[col] = df[col].fillna(0)
                    elif pd.api.types.is_string_dtype(df[col]):
                        df[col] = df[col].fillna('Não Informado')
                
                # Converte tipos numéricos para versões mais eficientes
                if pd.api.types.is_float_dtype(df[col]):
                    if df[col].min() > -1e6 and df[col].max() < 1e6:
                        df[col] = df[col].astype('float32')
                elif pd.api.types.is_integer_dtype(df[col]):
                    if df[col].min() > -2e9 and df[col].max() < 2e9:
                        df[col] = df[col].astype('int32')
                
                # Converte strings para categoria quando apropriado
                elif CvmScraper._should_convert_to_category(df[col], col):
                    # Primeiro, garante que não há valores nulos
                    df[col] = df[col].fillna('Não Informado')
                    
                    # Obtém todos os valores únicos e adiciona valores padrão
                    unique_values = df[col].unique().tolist()
                    for valor in ['Não Informado', 'Sem Classificação']:
                        if valor not in unique_values:
                            unique_values.append(valor)
                    
                    # Converte para categoria com todos os valores possíveis
                    df[col] = pd.Categorical(df[col], categories=unique_values)
                        
            except Exception as e:
                logger.warning(f"Erro ao otimizar coluna {col}: {str(e)}")
                continue
        
        return df
    
    @staticmethod
    def baixar_extrair_csv(url: str, nome_arquivo: str) -> Optional[pd.DataFrame]:
        """
        Baixa e extrai um CSV de dentro de um arquivo ZIP com cache e otimizações.
=======
class CvmScraper:
    """
    Classe responsável pelo scraping de dados da CVM.
    """
    
    @staticmethod
    def baixar_extrair_csv(url: str, nome_arquivo: str) -> pd.DataFrame:
        """
        Baixa e extrai um CSV de dentro de um arquivo ZIP.
>>>>>>> 24e81b5cb8f77a7693080e3f5a65d60a51c455f8
        
        Args:
            url: URL do arquivo ZIP a ser baixado
            nome_arquivo: Nome do arquivo CSV dentro do ZIP
            
        Returns:
<<<<<<< HEAD
            DataFrame com os dados ou None se não houver dados ou ocorrer erro
        """
        cache_path = CvmScraper._get_cache_path(url, nome_arquivo)
        
        # Verifica se existe cache válido
        if cache_path.exists():
            try:
                with timer('cache_load'):
                    logger.info(f"Carregando dados do cache: {cache_path}")
                    return pd.read_parquet(cache_path)
            except Exception as e:
                logger.warning(f"Erro ao ler cache, baixando novamente: {str(e)}")
                cache_path.unlink(missing_ok=True)
        
        try:
            # Download do arquivo
            logger.info(f"Baixando arquivo: {url}")
            content = CvmScraper._download_file(url)
            
            # Valida o arquivo ZIP
            if not CvmScraper._validate_zip_file(content):
                logger.error(f"Arquivo ZIP inválido: {url}")
                return None
            
            # Processa o arquivo em chunks para economia de memória
            dfs = []
            with timer('processamento'):
                with zipfile.ZipFile(BytesIO(content)) as zf:
                    if nome_arquivo not in zf.namelist():
                        logger.error(f"Arquivo {nome_arquivo} não encontrado no ZIP")
                        return None
                        
                    with zf.open(nome_arquivo) as csv_file:
                        chunks = pd.read_csv(
                            csv_file,
                            encoding='latin1',
                            sep=';',
                            decimal=',',
                            chunksize=CvmScraper.CHUNK_SIZE,
                            low_memory=False
                        )
                        
                        for chunk in chunks:
                            # Otimiza cada chunk
                            with timer('otimizacao'):
                                chunk_otimizado = CvmScraper._optimize_dataframe(chunk)
                                dfs.append(chunk_otimizado)
                                
                            # Libera memória
                            gc.collect()
            
            # Concatena todos os chunks
            df_final = pd.concat(dfs, ignore_index=True)
            
            # Salva no cache
            with timer('cache_save'):
                logger.info(f"Salvando dados no cache: {cache_path}")
                df_final.to_parquet(cache_path, index=False)
            
            return df_final
            
        except Exception as e:
            logger.error(f"Erro ao processar arquivo {url}: {str(e)}")
            return None
=======
            DataFrame contendo os dados do CSV
        """
        response = requests.get(url)
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            with zip_ref.open(nome_arquivo) as file:
                df = pd.read_csv(file, sep=';', encoding='latin1', low_memory=False)
        return df
>>>>>>> 24e81b5cb8f77a7693080e3f5a65d60a51c455f8
    
    @staticmethod
    def importa_dados(nome_arquivo_fonte: str, data_inicio: str = '2022-01-01') -> Optional[pd.DataFrame]:
        """
<<<<<<< HEAD
        Importa dados de FIDCs da CVM para um período específico com otimizações.
=======
        Importa dados de FIDCs da CVM para um período específico.
>>>>>>> 24e81b5cb8f77a7693080e3f5a65d60a51c455f8
        
        Args:
            nome_arquivo_fonte: Prefixo do nome do arquivo a ser baixado
            data_inicio: Data de início para baixar os dados (formato: 'YYYY-MM-DD')
            
        Returns:
            DataFrame contendo os dados importados ou None se não houver dados
        """
<<<<<<< HEAD
        start_time = time.time()
        registros_por_mes = {}
        total_registros = 0
        
        try:
            # URL base
            url_base = 'https://dados.cvm.gov.br/dados/FIDC/DOC/INF_MENSAL/DADOS/'

            # Formatando data input para ser usada
            data_inicio = pd.to_datetime(data_inicio)

            # Datas a baixar
            data_atual = pd.to_datetime("today").replace(day=1) - pd.DateOffset(days=1)
            datas_a_baixar = pd.date_range(start=data_inicio, end=data_atual, freq='M')

            # Loop para baixar arquivo de cada mês
            dfs_novos = []
            erros = []
            
            for data in datas_a_baixar:
                ano, mes = data.year, data.month
                url = f"{url_base}inf_mensal_fidc_{ano}{mes:02d}.zip"
                nome_arquivo = f"{nome_arquivo_fonte}_{ano}{mes:02d}.csv"
                
                try:
                    df_novo = CvmScraper.baixar_extrair_csv(url, nome_arquivo)
                    
                    if df_novo is not None:
                        # Padronização das colunas
                        cnpj_col = 'CNPJ_FUNDO' if 'CNPJ_FUNDO' in df_novo.columns else 'CNPJ_FUNDO_CLASSE'
                        df_novo.rename(columns={"DT_COMPTC": "Data", cnpj_col: 'CNPJ'}, inplace=True)
                        
                        registros_por_mes[f"{mes:02d}/{ano}"] = len(df_novo)
                        total_registros += len(df_novo)
                        dfs_novos.append(df_novo)
                        
                        # Libera memória após processar cada arquivo
                        del df_novo
                        gc.collect()
                        
                except Exception as e:
                    erro_msg = f"Erro ao processar {mes:02d}/{ano}: {str(e)}"
                    logger.error(erro_msg)
                    erros.append(erro_msg)

            if not dfs_novos:
                if erros:
                    logger.error("Erros encontrados durante a importação:\n" + "\n".join(erros))
                return None
            
            try:
                # Log detalhado dos registros por mês
                logger.info("\nRegistros por mês:")
                for periodo, num_registros in sorted(registros_por_mes.items()):
                    logger.info(f"  {periodo}: {num_registros:,} registros")
                logger.info(f"Total acumulado: {total_registros:,} registros\n")
                
                # Concatena todos os DataFrames
                logger.info(f"Concatenando {len(dfs_novos)} DataFrames...")
                df_novos = pd.concat(dfs_novos, ignore_index=True)
                
                # Ordena por data para otimizar consultas futuras
                df_novos.sort_values('Data', inplace=True)
                
                registros_final = len(df_novos)
                if registros_final != total_registros:
                    logger.warning(f"Diferença no número de registros após concatenação!")
                    logger.warning(f"  Registros antes: {total_registros:,}")
                    logger.warning(f"  Registros depois: {registros_final:,}")
                    logger.warning(f"  Diferença: {abs(registros_final - total_registros):,}")
                
                return df_novos
                
            except Exception as e:
                logger.error(f"Erro ao concatenar DataFrames: {str(e)}")
                raise
            finally:
                # Limpa a lista de DataFrames e força liberação de memória
                dfs_novos.clear()
                gc.collect()
                
        finally:
            # Log do tempo total de importação
            total_time = time.time() - start_time
            logger.info(f"\nEstatísticas finais:")
            logger.info(f"  Tempo total de importação: {total_time:.2f} segundos")
            logger.info(f"  Total de registros processados: {total_registros:,}")
            logger.info("\nMétricas de tempo por operação:")
            for operacao, stats in get_metricas_tempo().items():
                logger.info(f"  {operacao}:")
                for metrica, valor in stats.items():
                    if metrica in ['media', 'min', 'max', 'total']:
                        logger.info(f"    {metrica}: {valor:.2f} segundos")
                    else:
                        logger.info(f"    {metrica}: {valor}") 
=======
        # URL base
        url_base = 'https://dados.cvm.gov.br/dados/FIDC/DOC/INF_MENSAL/DADOS/'

        # Formatando data input para ser usada
        data_inicio = pd.to_datetime(data_inicio)

        # Datas a baixar
        data_atual = pd.to_datetime("today").replace(day=1) - pd.DateOffset(days=1)
        datas_a_baixar = pd.date_range(start=data_inicio, end=data_atual, freq='M')

        # Loop para baixar arquivo de cada mês
        dfs_novos = []
        for data in datas_a_baixar:
            ano, mes = data.year, data.month
            try:
                df_novo = CvmScraper.baixar_extrair_csv(
                    f"{url_base}inf_mensal_fidc_{ano}{mes:02d}.zip",
                    f"{nome_arquivo_fonte}_{ano}{mes:02d}.csv"
                )
                cnpj_col = 'CNPJ_FUNDO' if 'CNPJ_FUNDO' in df_novo.columns else 'CNPJ_FUNDO_CLASSE'
                df_novo.rename(columns={"DT_COMPTC": "Data", cnpj_col: 'CNPJ'}, inplace=True)
                dfs_novos.append(df_novo)
            except Exception as e:
                # Erro ao baixar será tratado pelo chamador
                pass

        if not dfs_novos:
            return None
        
        df_novos = pd.concat(dfs_novos, ignore_index=True)
        return df_novos 
>>>>>>> 24e81b5cb8f77a7693080e3f5a65d60a51c455f8
