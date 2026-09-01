#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CORE do Sistema de Fusão de IA

Motor inteligente que combina respostas de múltiplos modelos de IA.

Exemplo:
    from src.core.fusion_engine import FusionEngine
    
    engine = FusionEngine(config)
    result = engine.fuse(
        prompt="Explique machine learning",
        models=["claude", "gemini"],
        strategy="weighted"
    )
    print(result["fused_response"])
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

from src.utils.config import Config
from src.utils.exceptions import (
    FusionProcessError,
    ModelNotAvailableError,
)
from src.utils.validators import (
    PromptValidator,
    ModelListValidator,
    StrategyValidator,
)


logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Tipos de tarefas suportadas."""
    TECHNICAL = "technical"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    PROBLEM_SOLVING = "problem_solving"
    GENERAL = "general"


class FusionStrategy(Enum):
    """Estratégias de fusão disponíveis."""
    WEIGHTED = "weighted"
    DEBATE = "debate"
    TOURNAMENT = "tournament"
    SEQUENTIAL_REFINEMENT = "sequential_refinement"
    ENSEMBLE = "ensemble"


@dataclass
class FusionResult:
    """
    Resultado de uma operação de fusão.
    
    Attributes:
        fused_response: Resposta fundida
        synergy_score: Score de sinergia (0-1)
        task_type: Tipo de tarefa detectado
        strategy_used: Estratégia usada
        models_used: Modelos que contribuíram
        individual_responses: Respostas individuais dos modelos
    """
    fused_response: str
    synergy_score: float
    task_type: str
    strategy_used: str
    models_used: List[str]
    individual_responses: Dict[str, str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte resultado para dicionário."""
        return {
            "fused_response": self.fused_response,
            "synergy_score": self.synergy_score,
            "task_type": self.task_type,
            "strategy_used": self.strategy_used,
            "models_used": self.models_used,
            "individual_responses": self.individual_responses,
        }


class FusionEngine:
    """
    Motor principal de fusão de respostas de múltiplos modelos de IA.
    
    Implementa várias estratégias de fusão e detecção automática de tipos de tarefa.
    """

    # Keywords para classificação de tarefa
    TECHNICAL_KEYWORDS = [
        "algorithm", "code", "program", "function", "technical",
        "debug", "implement", "optimize", "performance", "architecture"
    ]
    CREATIVE_KEYWORDS = [
        "create", "design", "imagine", "innovate", "art", "story",
        "write", "brainstorm", "idea", "novel"
    ]
    ANALYTICAL_KEYWORDS = [
        "analyze", "evaluate", "compare", "assess", "examine",
        "review", "critical", "study", "investigate", "research"
    ]
    PROBLEM_SOLVING_KEYWORDS = [
        "solve", "resolve", "fix", "address", "tackle", "overcome",
        "challenge", "issue", "problem", "solution"
    ]

    def __init__(self, config: Optional[Config] = None):
        """
        Inicializa o motor de fusão.
        
        Args:
            config: Objeto Config. Se None, cria um novo.
        """
        self.config = config or Config()
        self.logger = logger
        self._log("Fusion Engine initialized", level="info")

    def fuse(
        self,
        prompt: str,
        models: List[str] = None,
        strategy: str = "weighted",
        task_type: str = "auto",
        return_individual: bool = False,
    ) -> FusionResult:
        """
        Executa fusão de respostas de múltiplos modelos.
        
        Args:
            prompt: Prompt a processar
            models: Lista de modelos a usar. Default: ["claude", "gemini"]
            strategy: Estratégia de fusão. Default: "weighted"
            task_type: Tipo de tarefa (auto-detect se "auto")
            return_individual: Se True, retorna respostas individuais
        
        Returns:
            FusionResult com resposta fundida e metadados
        
        Raises:
            FusionProcessError: Se algo der errado no processo
        """
        try:
            # Validações
            PromptValidator.validate(prompt)
            models = models or ["claude", "gemini"]
            ModelListValidator.validate(models)
            StrategyValidator.validate(strategy)

            # Detecta tipo de tarefa se "auto"
            if task_type == "auto":
                task_type = self.detect_task_type(prompt)

            self._log(
                f"Fusing with {len(models)} models using {strategy} strategy",
                context={"task_type": task_type},
            )

            # Simula obtenção de respostas (será implementado com APIs reais)
            individual_responses = self._get_model_responses(prompt, models)

            # Calcula score de sinergia
            synergy_score = self._calculate_synergy(
                individual_responses, task_type
            )

            # Executa fusão baseada na estratégia
            fused_response = self._apply_strategy(
                individual_responses, strategy, task_type
            )

            return FusionResult(
                fused_response=fused_response,
                synergy_score=synergy_score,
                task_type=task_type,
                strategy_used=strategy,
                models_used=models,
                individual_responses=individual_responses if return_individual else None,
            )

        except Exception as e:
            self._log(f"Fusion error: {str(e)}", level="error")
            raise FusionProcessError(str(e), step="fuse")

    def detect_task_type(self, prompt: str) -> str:
        """
        Detecta tipo de tarefa automaticamente baseado em keywords.
        
        Args:
            prompt: Prompt a analisar
        
        Returns:
            Tipo de tarefa detectado
        """
        prompt_lower = prompt.lower()

        scores = {
            TaskType.TECHNICAL.value: sum(
                1 for kw in self.TECHNICAL_KEYWORDS if kw in prompt_lower
            ),
            TaskType.CREATIVE.value: sum(
                1 for kw in self.CREATIVE_KEYWORDS if kw in prompt_lower
            ),
            TaskType.ANALYTICAL.value: sum(
                1 for kw in self.ANALYTICAL_KEYWORDS if kw in prompt_lower
            ),
            TaskType.PROBLEM_SOLVING.value: sum(
                1 for kw in self.PROBLEM_SOLVING_KEYWORDS if kw in prompt_lower
            ),
        }

        detected_type = max(scores, key=scores.get)
        confidence = scores[detected_type] / sum(scores.values()) if sum(scores.values()) > 0 else 0

        # Se confiança baixa, retorna "general"
        if confidence < 0.2:
            return TaskType.GENERAL.value

        return detected_type

    def calculate_synergy_score(
        self, response_a: str, response_b: str
    ) -> float:
        """
        Calcula score de sinergia entre duas respostas.
        
        Args:
            response_a: Primeira resposta
            response_b: Segunda resposta
        
        Returns:
            Score entre 0 e 1
        """
        if not response_a or not response_b:
            return 0.0

        # Métrica simples: similaridade de comprimento + sobreposição de palavras
        len_a = len(response_a.split())
        len_b = len(response_b.split())
        len_ratio = min(len_a, len_b) / max(len_a, len_b) if max(len_a, len_b) > 0 else 0

        words_a = set(response_a.lower().split())
        words_b = set(response_b.lower().split())
        if words_a or words_b:
            word_overlap = len(words_a & words_b) / len(words_a | words_b)
        else:
            word_overlap = 0

        # Score final (média ponderada)
        synergy_score = (len_ratio * 0.3) + (word_overlap * 0.7)
        return min(1.0, max(0.0, synergy_score))

    def _get_model_responses(
        self, prompt: str, models: List[str]
    ) -> Dict[str, str]:
        """
        Obtém respostas de múltiplos modelos.
        
        TODO: Integrar com APIs reais (Anthropic, Google, etc)
        Por enquanto, retorna respostas simuladas.
        
        Args:
            prompt: Prompt
            models: Lista de modelos
        
        Returns:
            Dicionário {modelo: resposta}
        """
        responses = {}
        for model in models:
            # Simulação - será substituído por chamadas reais à API
            responses[model] = f"[{model.upper()}] Response to: {prompt[:50]}..."
        return responses

    def _calculate_synergy(
        self,
        responses: Dict[str, str],
        task_type: str,
    ) -> float:
        """
        Calcula score de sinergia geral entre respostas.
        
        Args:
            responses: Dicionário de respostas
            task_type: Tipo de tarefa (afeta pesos)
        
        Returns:
            Score de sinergia (0-1)
        """
        if len(responses) < 2:
            return 1.0

        # Calcula sinergia pairwise
        response_list = list(responses.values())
        total_synergy = 0.0
        pairs = 0

        for i in range(len(response_list)):
            for j in range(i + 1, len(response_list)):
                synergy = self.calculate_synergy_score(
                    response_list[i], response_list[j]
                )
                total_synergy += synergy
                pairs += 1

        if pairs == 0:
            return 1.0

        avg_synergy = total_synergy / pairs

        # Ajusta score baseado no tipo de tarefa
        task_boost = {
            TaskType.TECHNICAL.value: 0.1,
            TaskType.CREATIVE.value: 0.05,
            TaskType.ANALYTICAL.value: 0.15,
            TaskType.PROBLEM_SOLVING.value: 0.1,
            TaskType.GENERAL.value: 0.0,
        }

        adjusted_score = min(1.0, avg_synergy + task_boost.get(task_type, 0))
        return adjusted_score

    def _apply_strategy(
        self,
        responses: Dict[str, str],
        strategy: str,
        task_type: str,
    ) -> str:
        """
        Aplica estratégia de fusão às respostas.
        
        Args:
            responses: Dicionário de respostas
            strategy: Estratégia a usar
            task_type: Tipo de tarefa
        
        Returns:
            Resposta fundida
        """
        if strategy == FusionStrategy.WEIGHTED.value:
            return self._weighted_fusion(responses, task_type)
        elif strategy == FusionStrategy.ENSEMBLE.value:
            return self._ensemble_fusion(responses)
        elif strategy == FusionStrategy.DEBATE.value:
            return self._debate_fusion(responses)
        elif strategy == FusionStrategy.TOURNAMENT.value:
            return self._tournament_fusion(responses)
        elif strategy == FusionStrategy.SEQUENTIAL_REFINEMENT.value:
            return self._sequential_refinement(responses)
        else:
            return self._weighted_fusion(responses, task_type)

    def _weighted_fusion(
        self,
        responses: Dict[str, str],
        task_type: str,
    ) -> str:
        """
        Fusão com pesos adaptativos por tipo de tarefa.
        
        Args:
            responses: Respostas dos modelos
            task_type: Tipo de tarefa
        
        Returns:
            Resposta fundida
        """
        # Pesos adaptativos
        weights = {
            "claude": 0.6 if task_type == TaskType.TECHNICAL.value else 0.5,
            "gemini": 0.4 if task_type == TaskType.TECHNICAL.value else 0.5,
        }

        result = "[WEIGHTED FUSION]\n"
        for model, response in responses.items():
            weight = weights.get(model, 1.0 / len(responses))
            result += f"\n[{model.upper()} - {weight:.0%}]\n{response}"

        return result

    def _ensemble_fusion(self, responses: Dict[str, str]) -> str:
        """
        Fusão por ensemble (combinação simples).
        
        Args:
            responses: Respostas dos modelos
        
        Returns:
            Resposta fundida
        """
        result = "[ENSEMBLE FUSION]\n"
        for model, response in responses.items():
            result += f"\n## {model.upper()}\n{response}\n"
        return result

    def _debate_fusion(self, responses: Dict[str, str]) -> str:
        """
        Fusão por debate (simula discussão entre modelos).
        
        Args:
            responses: Respostas dos modelos
        
        Returns:
            Resposta fundida
        """
        result = "[DEBATE FUSION]\n\n"
        for i, (model, response) in enumerate(responses.items(), 1):
            result += f"Position {i} ({model}): {response}\n\n"
        result += "\n[SYNTHESIS]\nConsidações complementares das múltiplas perspectivas acima."
        return result

    def _tournament_fusion(self, responses: Dict[str, str]) -> str:
        """
        Fusão por tournament (melhor resposta vence).
        
        Args:
            responses: Respostas dos modelos
        
        Returns:
            Resposta fundida
        """
        # TODO: Implementar scoring real
        best_model = list(responses.keys())[0]
        return f"[TOURNAMENT WINNER: {best_model.upper()}]\n\n{responses[best_model]}"

    def _sequential_refinement(self, responses: Dict[str, str]) -> str:
        """
        Fusão por refinamento sequencial.
        
        Args:
            responses: Respostas dos modelos
        
        Returns:
            Resposta fundida
        """
        result = "[SEQUENTIAL REFINEMENT]\n"
        for i, (model, response) in enumerate(responses.items()):
            if i == 0:
                result += f"\nBase ({model}):\n{response}"
            else:
                result += f"\n\nRefinement by {model}:\n{response}"
        return result

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
            level: Nível de log (info, debug, warning, error)
            context: Contexto adicional
        """
        log_data = {"message": message}
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
