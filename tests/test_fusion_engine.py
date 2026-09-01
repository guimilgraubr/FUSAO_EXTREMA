#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Testes para FusionEngine.
"""

import pytest
from src.core.fusion_engine import (
    FusionEngine,
    TaskType,
    FusionStrategy,
)
from src.utils.config import Config
from src.utils.exceptions import FusionProcessError


class TestFusionEngine:
    """Testes para FusionEngine."""

    @pytest.fixture
    def engine(self):
        """Fixture para FusionEngine."""
        config = Config(env="development")
        return FusionEngine(config)

    def test_engine_initialization(self, engine):
        """Testa inicialização do engine."""
        assert engine is not None
        assert engine.config is not None

    def test_detect_task_type_technical(self, engine):
        """Testa detecção de tarefa técnica."""
        prompt = "How to optimize a Python algorithm?"
        task_type = engine.detect_task_type(prompt)
        assert task_type in [TaskType.TECHNICAL.value, TaskType.GENERAL.value]

    def test_detect_task_type_creative(self, engine):
        """Testa detecção de tarefa criativa."""
        prompt = "Create a story about artificial intelligence"
        task_type = engine.detect_task_type(prompt)
        assert task_type in [TaskType.CREATIVE.value, TaskType.GENERAL.value]

    def test_detect_task_type_analytical(self, engine):
        """Testa detecção de tarefa analítica."""
        prompt = "Analyze the pros and cons of this approach"
        task_type = engine.detect_task_type(prompt)
        assert task_type in [TaskType.ANALYTICAL.value, TaskType.GENERAL.value]

    def test_synergy_score_identical(self, engine):
        """Testa score de sinergia para respostas idênticas."""
        response = "This is a test response"
        score = engine.calculate_synergy_score(response, response)
        assert score == 1.0

    def test_synergy_score_empty(self, engine):
        """Testa score de sinergia para respostas vazias."""
        score = engine.calculate_synergy_score("", "")
        assert score == 0.0

    def test_synergy_score_different(self, engine):
        """Testa score de sinergia para respostas diferentes."""
        response_a = "This is response A"
        response_b = "This is response B"
        score = engine.calculate_synergy_score(response_a, response_b)
        assert 0 <= score <= 1

    def test_fuse_basic(self, engine):
        """Testa fusão básica."""
        prompt = "What is machine learning?"
        result = engine.fuse(
            prompt=prompt,
            models=["claude", "gemini"],
            strategy="weighted",
        )
        assert result is not None
        assert result.fused_response is not None
        assert 0 <= result.synergy_score <= 1
        assert result.task_type is not None
        assert len(result.models_used) > 0

    def test_fuse_invalid_prompt(self, engine):
        """Testa fusão com prompt inválido."""
        with pytest.raises(Exception):
            engine.fuse(prompt="hi")  # Muito curto

    def test_fuse_invalid_models(self, engine):
        """Testa fusão com modelos inválidos."""
        with pytest.raises(Exception):
            engine.fuse(
                prompt="What is machine learning?",
                models=["invalid_model"],
            )

    def test_fuse_with_strategy_ensemble(self, engine):
        """Testa fusão com estratégia ensemble."""
        prompt = "Explain deep learning"
        result = engine.fuse(
            prompt=prompt,
            models=["claude", "gemini"],
            strategy="ensemble",
        )
        assert result.strategy_used == "ensemble"
        assert "ENSEMBLE" in result.fused_response

    def test_fuse_with_strategy_debate(self, engine):
        """Testa fusão com estratégia debate."""
        prompt = "Is AI dangerous?"
        result = engine.fuse(
            prompt=prompt,
            models=["claude", "gemini"],
            strategy="debate",
        )
        assert result.strategy_used == "debate"
        assert "DEBATE" in result.fused_response

    def test_fuse_return_individual(self, engine):
        """Testa fusão retornando respostas individuais."""
        prompt = "What is neural networks?"
        result = engine.fuse(
            prompt=prompt,
            models=["claude", "gemini"],
            return_individual=True,
        )
        assert result.individual_responses is not None
        assert len(result.individual_responses) > 0

    def test_result_to_dict(self):
        """Testa conversão de resultado para dicionário."""
        from src.core.fusion_engine import FusionResult

        result = FusionResult(
            fused_response="Test response",
            synergy_score=0.85,
            task_type="technical",
            strategy_used="weighted",
            models_used=["claude", "gemini"],
        )
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert result_dict["synergy_score"] == 0.85
        assert len(result_dict["models_used"]) == 2
