#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pytest configuration and fixtures.
"""

import pytest
from src.utils.config import Config


@pytest.fixture
def config():
    """Fixture para Config object com environment de teste."""
    return Config(env="development")


@pytest.fixture
def sample_prompt():
    """Fixture para prompt de teste."""
    return "How to optimize a Python algorithm for better performance?"


@pytest.fixture
def sample_models():
    """Fixture para lista de modelos de teste."""
    return ["claude", "gemini"]


@pytest.fixture
def sample_strategy():
    """Fixture para estratégia de teste."""
    return "weighted"
