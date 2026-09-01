#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Testes para Config management system.
"""

import os
import pytest
from src.utils.config import Config
from src.utils.exceptions import ConfigurationError


class TestConfig:
    """Testes para classe Config."""
    
    def test_config_initialization(self):
        """Testa inicialização do Config."""
        config = Config(env="development")
        assert config.env == "development"
        assert config.base_path is not None
    
    def test_config_get_default(self):
        """Testa obtenção com valor default."""
        config = Config()
        value = config.get("nonexistent_key", default="default_value")
        assert value == "default_value"
    
    def test_config_get_bool(self):
        """Testa obtenção de valor booleano."""
        config = Config()
        
        # Testa conversão de string
        os.environ["FUSION_TEST_BOOL"] = "true"
        assert config.get_bool("test_bool") is True
        
        os.environ["FUSION_TEST_BOOL"] = "false"
        assert config.get_bool("test_bool") is False
    
    def test_config_get_int(self):
        """Testa obtenção de valor inteiro."""
        config = Config()
        
        os.environ["FUSION_TEST_INT"] = "42"
        assert config.get_int("test_int") == 42
        
        # Testa valor inválido
        os.environ["FUSION_TEST_INT"] = "invalid"
        assert config.get_int("test_int", default=0) == 0
    
    def test_config_env_precedence(self):
        """Testa precedência de env vars."""
        config = Config()
        
        # Seta env var
        os.environ["FUSION_TEST_KEY"] = "from_env"
        
        # Env var deve ter precedência
        assert config.get("test_key") == "from_env"
    
    def test_config_repr(self):
        """Testa representação string."""
        config = Config(env="development")
        assert "development" in repr(config)
