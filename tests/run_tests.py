#!/usr/bin/env python
"""
Script para executar todos os testes do projeto.
Pode ser executado como: python -m tests.run_tests
"""
import pytest
import os
import sys

def main():
    """Função principal que executa os testes e gera relatórios."""
    # Adicionar a pasta raiz do projeto ao path para imports
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    # Argumentos para o pytest
    args = [
        # Pasta de testes
        os.path.dirname(__file__),
        # Verbose para mostrar detalhes dos testes
        '-v',
        # Gerar relatório de cobertura
        '--cov=src',
        # Formato do relatório de cobertura
        '--cov-report=term',
        '--cov-report=html:tests/coverage_html',
        # Exibir barra de progresso
        '--progress',
        # Cores nos relatórios
        '--color=yes'
    ]
    
    # Executar os testes
    resultado = pytest.main(args)
    
    return resultado

if __name__ == "__main__":
    sys.exit(main()) 