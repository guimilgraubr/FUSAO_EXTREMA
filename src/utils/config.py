#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Config Management System

Gerencia configurações de forma centralizada, suportando:
- Arquivo YAML
- Variáveis de ambiente (.env)
- Environment variables do sistema

Exemplo:
    config = Config(env="development")
    api_key = config.get("anthropic_api_key")
    debug = config.get("debug", default=False)
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from dotenv import load_dotenv


class Config:
    """
    Gerenciador centralizado de configurações.
    
    Carrega configurações em ordem de precedência:
    1. Variáveis de ambiente do sistema
    2. Arquivo .env
    3. Arquivo YAML (base + environment-specific)
    4. Valores default
    """
    
    def __init__(self, env: Optional[str] = None):
        """
        Inicializa o gerenciador de configurações.
        
        Args:
            env: Environment (development, staging, production)
                Se None, tenta ler de ENVIRONMENT env var, default é 'development'
        """
        # Determina ambiente
        self.env = env or os.getenv("ENVIRONMENT", "development")
        
        # Caminho base (raiz do projeto)
        self.base_path = Path(__file__).parent.parent.parent
        self.config_path = self.base_path / "config"
        
        # Carrega configurações
        self._load_env_file()
        self.config = self._load_config()
    
    def _load_env_file(self) -> None:
        """
        Carrega arquivo .env.
        
        Tenta em ordem:
        1. .env.{environment}.local
        2. .env.{environment}
        3. .env.local
        4. .env
        """
        env_files = [
            self.config_path.parent / f".env.{self.env}.local",
            self.config_path.parent / f".env.{self.env}",
            self.config_path.parent / ".env.local",
            self.config_path.parent / ".env",
        ]
        
        for env_file in env_files:
            if env_file.exists():
                load_dotenv(env_file, override=True)
                break
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Carrega configurações de arquivos YAML.
        
        Returns:
            Dict com configurações mergeadas (base + environment-specific)
        """
        config = {}
        
        # Carrega config base
        base_config_file = self.config_path / "base_config.yaml"
        if base_config_file.exists():
            with open(base_config_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
        
        # Carrega config específica do environment
        env_config_file = self.config_path / f"{self.env}.yaml"
        if env_config_file.exists():
            with open(env_config_file, "r", encoding="utf-8") as f:
                env_config = yaml.safe_load(f) or {}
                config.update(env_config)
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém valor de configuração.
        
        Tenta em ordem:
        1. Variável de ambiente (FUSION_{KEY})
        2. Arquivo YAML
        3. Valor default
        
        Args:
            key: Chave de configuração
            default: Valor padrão se não encontrado
        
        Returns:
            Valor da configuração
        """
        # 1. Tenta env var com prefixo FUSION_
        env_key = f"FUSION_{key.upper()}"
        if env_key in os.environ:
            return os.environ[env_key]
        
        # 2. Tenta env var sem prefixo
        if key.upper() in os.environ:
            return os.environ[key.upper()]
        
        # 3. Tenta arquivo YAML
        if key in self.config:
            return self.config[key]
        
        # 4. Retorna default
        return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        Obtém valor booleano de configuração.
        
        Args:
            key: Chave de configuração
            default: Valor padrão
        
        Returns:
            Valor booleano
        """
        value = self.get(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes", "on")
        return bool(value)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """
        Obtém valor inteiro de configuração.
        
        Args:
            key: Chave de configuração
            default: Valor padrão
        
        Returns:
            Valor inteiro
        """
        value = self.get(key, default)
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Retorna todas as configurações como dicionário.
        
        Returns:
            Dicionário com todas as configurações
        """
        return self.config.copy()
    
    def __repr__(self) -> str:
        return f"Config(env={self.env})"
