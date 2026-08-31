#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de teste simplificado para verificar o funcionamento básico
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.append(str(Path(__file__).parent))

try:
    print("Tentando importar o logger...")
    from arsenal.logger_system import get_fusion_logger

    print("Logger importado com sucesso!")

    logger = get_fusion_logger()
    print("Logger criado com sucesso!")

    logger.log_fusion_event("teste", {"mensagem": "Funcionando"})
    print("Log gravado com sucesso!")

except Exception as e:
    print(f"Erro ao trabalhar com o logger: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nTentando importar o motor de fusão...")
    from arsenal.intelligence_fusion import create_fusion_engine

    print("Motor de fusão importado com sucesso!")

    engine = create_fusion_engine()
    print("Motor de fusão criado com sucesso!")

    # Testa uma operação simples
    result = engine.calculate_synergy_score("Teste de Claude", "Teste de Gemini")
    print(f"Score de sinergia calculado: {result}")

except Exception as e:
    print(f"Erro ao trabalhar com o motor de fusão: {e}")
    import traceback
    traceback.print_exc()

print("\nTeste básico concluído!")