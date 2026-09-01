#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Testes para Orchestrator.
"""

import pytest
from src.core.orchestrator import FusionOrchestrator
from src.utils.config import Config


class TestFusionOrchestrator:
    """Testes para FusionOrchestrator."""

    @pytest.fixture
    def orchestrator(self):
        """Fixture para Orchestrator."""
        config = Config(env="development")
        return FusionOrchestrator(config)

    def test_orchestrator_initialization(self, orchestrator):
        """Testa inicialização do orquestrador."""
        assert orchestrator is not None
        assert orchestrator.fusion_engine is not None

    def test_execute_basic(self, orchestrator):
        """Testa execução básica."""
        result = orchestrator.execute(
            prompt="What is machine learning?",
            models=["claude", "gemini"],
        )
        assert isinstance(result, dict)
        assert "fused_response" in result
        assert "synergy_score" in result

    def test_list_available_models(self, orchestrator):
        """Testa listagem de modelos."""
        models = orchestrator.list_available_models()
        assert "models" in models
        assert len(models["models"]) > 0
        assert "claude" in models["models"]
        assert "gemini" in models["models"]

    def test_list_strategies(self, orchestrator):
        """Testa listagem de estratégias."""
        strategies = orchestrator.list_strategies()
        assert "strategies" in strategies
        assert len(strategies["strategies"]) > 0
        strategy_names = [s["name"] for s in strategies["strategies"]]
        assert "weighted" in strategy_names
        assert "debate" in strategy_names

    def test_get_health(self, orchestrator):
        """Testa health check."""
        health = orchestrator.get_health()
        assert health["status"] == "healthy"
        assert "version" in health
        assert health["engine"] == "fusion"
