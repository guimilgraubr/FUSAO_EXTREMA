#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de Logging para o Projeto de Fusão Claude-Gemini
Local: FUSAO_EXTREMA/arsenal/logger_system.py
"""

import logging
import os
from datetime import datetime
from pathlib import Path

class FusionLogger:
    """
    Sistema avançado de logging para registrar atividades de fusão de IA
    """

    def __init__(self, log_directory="FUSAO_EXTREMA/logs"):
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(parents=True, exist_ok=True)

        # Configuração do logger principal
        self.logger = logging.getLogger('FusionLogger')
        self.logger.setLevel(logging.DEBUG)

        # Formato de log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Handler para arquivo
        file_handler = logging.FileHandler(
            self.log_directory / f"fusion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log_fusion_event(self, event_type: str, details: dict):
        """
        Registra um evento de fusão
        """
        message = f"{event_type.upper()}: {details}"
        self.logger.info(message)

    def log_error(self, error_message: str):
        """
        Registra um erro
        """
        self.logger.error(error_message)

    def log_performance_metrics(self, metrics: dict):
        """
        Registra métricas de performance
        """
        self.logger.info(f"PERFORMANCE_METRICS: {metrics}")

    def log_synergy_analysis(self, analysis: dict):
        """
        Registra análise de sinergia
        """
        self.logger.info(f"SYNERGY_ANALYSIS: {analysis}")

# Função auxiliar para facilitar o uso
def get_fusion_logger():
    """
    Retorna uma instância do logger de fusão
    """
    return FusionLogger()

if __name__ == "__main__":
    print("Sistema de logging para fusão de IA inicializado!")
    print("Use get_fusion_logger() para obter uma instância do logger.")