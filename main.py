"""
Ponto de entrada principal para a aplicação de coleta e processamento de FIDCs.
"""
from config.tables import TABLES
from src.core.pipeline import FidcPipeline
<<<<<<< HEAD
import shutil
=======
>>>>>>> 24e81b5cb8f77a7693080e3f5a65d60a51c455f8

def main():
    """
    Função principal que inicia o pipeline de coleta e processamento de FIDCs.
    """
    # Inicializar o pipeline com as configurações das tabelas
    pipeline = FidcPipeline(TABLES)
    
    # Executar o pipeline
    pipeline.run(data_inicio='2022-01-01')

<<<<<<< HEAD
    # Limpar o cache
    shutil.rmtree('cache', ignore_errors=True)

=======
>>>>>>> 24e81b5cb8f77a7693080e3f5a65d60a51c455f8
if __name__ == "__main__":
    main()