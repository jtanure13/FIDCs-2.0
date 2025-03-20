"""
Módulo para scraping de dados da CVM.
"""
import pandas as pd
import requests
import zipfile
from io import BytesIO
from typing import Optional, List
from datetime import datetime

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

class CvmScraper:
    """
    Classe responsável pelo scraping de dados da CVM.
    """
    
    @staticmethod
    def baixar_extrair_csv(url: str, nome_arquivo: str) -> pd.DataFrame:
        """
        Baixa e extrai um CSV de dentro de um arquivo ZIP.
        
        Args:
            url: URL do arquivo ZIP a ser baixado
            nome_arquivo: Nome do arquivo CSV dentro do ZIP
            
        Returns:
            DataFrame contendo os dados do CSV
        """
        response = requests.get(url)
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            with zip_ref.open(nome_arquivo) as file:
                df = pd.read_csv(file, sep=';', encoding='latin1', low_memory=False)
        return df
    
    @staticmethod
    def importa_dados(nome_arquivo_fonte: str, data_inicio: str = '2022-01-01') -> Optional[pd.DataFrame]:
        """
        Importa dados de FIDCs da CVM para um período específico.
        
        Args:
            nome_arquivo_fonte: Prefixo do nome do arquivo a ser baixado
            data_inicio: Data de início para baixar os dados (formato: 'YYYY-MM-DD')
            
        Returns:
            DataFrame contendo os dados importados ou None se não houver dados
        """
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