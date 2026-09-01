#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Orquestrador Principal da Fusão de IA

Coordenador de alto nível que gerencia o pipeline completo de fusão.
"""

from typing import Dict, List, Any, Optional
import logging

from src.utils.config import Config
from src.core.fusion_engine import FusionEngine, FusionResult
from src.utils.exceptions import FusionProcessError


logger = logging.getLogger(__name__)


class FusionOrchestrator:
    """
    Orquestrador principal para fusão de respostas de múltiplos modelos.
    
    Gerencia:
    - Inicialização de engines
    - Execução de pipelines
    - Logging e monitoramento
    - Cache de resultados (opcional)
    """

    def __init__(self, config: Optional[Config] = None):
        """
        Inicializa o orquestrador.
        
        Args:
            config: Objeto Config
        """
        self.config = config or Config()
        self.fusion_engine = FusionEngine(self.config)
        self.logger = logger
        self._log("Orchestrator initialized")

    def execute(
        self,
        prompt: str,
        models: List[str] = None,
        strategy: str = "weighted",
        task_type: str = "auto",
        return_individual: bool = False,
    ) -> Dict[str, Any]:
        """
        Executa pipeline completo de fusão.
        
        Args:
            prompt: Prompt a processar
            models: Modelos a usar
            strategy: Estratégia de fusão
            task_type: Tipo de tarefa
            return_individual: Retornar respostas individuais
        
        Returns:
            Dicionário com resultado
        
        Raises:
            FusionProcessError: Se algo der errado
        """
        try:
            self._log(
                "Pipeline execution started",
                context={"prompt_length": len(prompt), "models": models}
            )

            # Executa fusão
            result: FusionResult = self.fusion_engine.fuse(
                prompt=prompt,
                models=models,
                strategy=strategy,
                task_type=task_type,
                return_individual=return_individual,
            )

            self._log(
                "Pipeline execution completed",
                context={"synergy_score": result.synergy_score}
            )

            return result.to_dict()

        except Exception as e:
            self._log(f"Pipeline error: {str(e)}", level="error")
            raise

    def list_available_models(self) -> Dict[str, Any]:
        """
        Lista modelos disponíveis.
        
        Returns:
            Dicionário com modelos
        """
        return {
            "models": [
                "claude",
                "gemini",
                "llama",
                "mistral",
                "gpt4",
            ],
            "default": "claude",
            "description": "Available AI models for fusion",
        }

    def list_strategies(self) -> Dict[str, Any]:
        """
        Lista estratégias de fusão disponíveis.
        
        Returns:
            Dicionário com estratégias
        """
        return {
            "strategies": [
                {
                    "name": "weighted",
                    "description": "Adaptive weighted fusion based on task type",
                },
                {
                    "name": "debate",
                    "description": "Models debate and reach consensus",
                },
                {
                    "name": "tournament",
                    "description": "Majority voting - best response wins",
                },
                {
                    "name": "sequential_refinement",
                    "description": "Model 1 -> Model 2 refines",
                },
                {
                    "name": "ensemble",
                    "description": "Simple combination of all responses",
                },
            ]
        }

    def get_health(self) -> Dict[str, Any]:
        """
        Retorna status de saúde do sistema.
        
        Returns:
            Status do sistema
        """
        return {
            "status": "healthy",
            "version": "2.0.0",
            "engine": "fusion",
            "models_ready": len(self.list_available_models()["models"]),
            "strategies_available": len(self.list_strategies()["strategies"]),
        }

    def _log(
        self,
        message: str,
        level: str = "info",
        context: Dict[str, Any] = None,
    ) -> None:
        """
        Log estruturado.
        
        Args:
            message: Mensagem
            level: Nível (info, debug, warning, error)
            context: Contexto adicional
        """
        log_data = {"message": message, "component": "orchestrator"}
        if context:
            log_data.update(context)

        if level == "debug":
            self.logger.debug(log_data)
        elif level == "warning":
            self.logger.warning(log_data)
        elif level == "error":
            self.logger.error(log_data)
        else:
            self.logger.info(log_data)
