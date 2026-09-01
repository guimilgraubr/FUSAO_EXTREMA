#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Testes para validadores.
"""

import pytest
from src.utils.validators import (
    PromptValidator,
    ModelListValidator,
    StrategyValidator
)
from src.utils.exceptions import ValidationError


class TestPromptValidator:
    """Testes para PromptValidator."""
    
    def test_valid_prompt(self):
        """Testa prompt válido."""
        prompt = "This is a valid prompt with enough characters"
        PromptValidator.validate(prompt)  # Não deve lançar exceção
    
    def test_prompt_too_short(self):
        """Testa prompt muito curto."""
        with pytest.raises(ValidationError):
            PromptValidator.validate("hi")
    
    def test_prompt_not_string(self):
        """Testa prompt não é string."""
        with pytest.raises(ValidationError):
            PromptValidator.validate(123)
    
    def test_prompt_too_long(self):
        """Testa prompt muito longo."""
        long_prompt = "a" * 15000
        with pytest.raises(ValidationError):
            PromptValidator.validate(long_prompt)


class TestModelListValidator:
    """Testes para ModelListValidator."""
    
    def test_valid_models(self):
        """Testa lista válida de modelos."""
        models = ["claude", "gemini"]
        ModelListValidator.validate(models)  # Não deve lançar exceção
    
    def test_invalid_model(self):
        """Testa modelo inválido."""
        with pytest.raises(ValidationError):
            ModelListValidator.validate(["invalid_model"])
    
    def test_empty_list(self):
        """Testa lista vazia."""
        with pytest.raises(ValidationError):
            ModelListValidator.validate([])
    
    def test_too_many_models(self):
        """Testa muitos modelos."""
        models = ["claude", "gemini", "llama", "mistral", "gpt4", "extra"]
        with pytest.raises(ValidationError):
            ModelListValidator.validate(models)


class TestStrategyValidator:
    """Testes para StrategyValidator."""
    
    def test_valid_strategy(self):
        """Testa estratégia válida."""
        for strategy in ["weighted", "debate", "tournament"]:
            StrategyValidator.validate(strategy)  # Não deve lançar exceção
    
    def test_invalid_strategy(self):
        """Testa estratégia inválida."""
        with pytest.raises(ValidationError):
            StrategyValidator.validate("invalid_strategy")
