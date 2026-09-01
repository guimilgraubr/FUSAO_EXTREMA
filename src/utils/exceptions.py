#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Custom Exceptions for Fusion System

Define exceções específicas para melhor tratamento de erros.
"""


class FusionException(Exception):
    """
    Base exception para o sistema de fusão.
    
    Todas as exceções customizadas herdam desta classe.
    """
    
    def __init__(self, message: str, code: str = "FUSION_ERROR"):
        """
        Inicializa exceção.
        
        Args:
            message: Mensagem de erro
            code: Código de erro (para logging e debugging)
        """
        self.message = message
        self.code = code
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


class ModelNotAvailableError(FusionException):
    """
    Exceção levantada quando um modelo não está disponível.
    """
    
    def __init__(self, model: str):
        super().__init__(
            f"Model '{model}' is not available",
            code="MODEL_NOT_AVAILABLE"
        )
        self.model = model


class ConfigurationError(FusionException):
    """
    Exceção levantada quando há erro de configuração.
    """
    
    def __init__(self, message: str, config_key: str = None):
        super().__init__(
            f"Configuration error: {message}" + (f" (key: {config_key})" if config_key else ""),
            code="CONFIG_ERROR"
        )
        self.config_key = config_key


class FusionProcessError(FusionException):
    """
    Exceção levantada durante o processo de fusão.
    """
    
    def __init__(self, message: str, step: str = None):
        super().__init__(
            f"Fusion process error: {message}" + (f" (step: {step})" if step else ""),
            code="FUSION_PROCESS_ERROR"
        )
        self.step = step


class APIError(FusionException):
    """
    Exceção levantada quando há erro ao chamar API externa.
    """
    
    def __init__(self, provider: str, message: str, status_code: int = None):
        super().__init__(
            f"API error from {provider}: {message}" + (f" (status: {status_code})" if status_code else ""),
            code="API_ERROR"
        )
        self.provider = provider
        self.status_code = status_code


class ValidationError(FusionException):
    """
    Exceção levantada quando há erro de validação de entrada.
    """
    
    def __init__(self, field: str, message: str):
        super().__init__(
            f"Validation error on field '{field}': {message}",
            code="VALIDATION_ERROR"
        )
        self.field = field
