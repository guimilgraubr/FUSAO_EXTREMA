#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Validadores de entrada para o sistema de fusão.
"""

from typing import List, Optional
from src.utils.exceptions import ValidationError


class PromptValidator:
    """
    Validador para prompts.
    """
    
    MIN_LENGTH = 5
    MAX_LENGTH = 10000
    
    @classmethod
    def validate(cls, prompt: str) -> None:
        """
        Valida um prompt.
        
        Args:
            prompt: Prompt a validar
        
        Raises:
            ValidationError: Se inválido
        """
        if not isinstance(prompt, str):
            raise ValidationError("prompt", "Must be a string")
        
        if len(prompt.strip()) < cls.MIN_LENGTH:
            raise ValidationError(
                "prompt",
                f"Must be at least {cls.MIN_LENGTH} characters"
            )
        
        if len(prompt) > cls.MAX_LENGTH:
            raise ValidationError(
                "prompt",
                f"Must be at most {cls.MAX_LENGTH} characters"
            )


class ModelListValidator:
    """
    Validador para lista de modelos.
    """
    
    VALID_MODELS = ["claude", "gemini", "llama", "mistral", "gpt4"]
    
    @classmethod
    def validate(cls, models: List[str]) -> None:
        """
        Valida lista de modelos.
        
        Args:
            models: Lista de modelos
        
        Raises:
            ValidationError: Se inválido
        """
        if not isinstance(models, list):
            raise ValidationError("models", "Must be a list")
        
        if len(models) == 0:
            raise ValidationError("models", "List cannot be empty")
        
        if len(models) > 5:
            raise ValidationError("models", "Maximum 5 models allowed")
        
        for model in models:
            if model not in cls.VALID_MODELS:
                raise ValidationError(
                    "models",
                    f"Invalid model '{model}'. Valid: {cls.VALID_MODELS}"
                )


class StrategyValidator:
    """
    Validador para estratégia de fusão.
    """
    
    VALID_STRATEGIES = [
        "weighted",
        "debate",
        "tournament",
        "sequential_refinement",
        "ensemble"
    ]
    
    @classmethod
    def validate(cls, strategy: str) -> None:
        """
        Valida estratégia de fusão.
        
        Args:
            strategy: Estratégia
        
        Raises:
            ValidationError: Se inválido
        """
        if not isinstance(strategy, str):
            raise ValidationError("strategy", "Must be a string")
        
        if strategy not in cls.VALID_STRATEGIES:
            raise ValidationError(
                "strategy",
                f"Invalid strategy. Valid: {cls.VALID_STRATEGIES}"
            )
