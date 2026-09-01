# 🔧 PLANO DE REFACTOR E MELHORIA - FUSAO_EXTREMA

**Objetivo**: Elevar de **7/10 para 8.5/10**

**Timeline**: 2-3 semanas de desenvolvimento

---

## 📊 ANÁLISE ATUAL

### O que FUNCIONA ✅
- Motor de fusão inteligente (intelligence_fusion.py)
- Classificação automática de tarefas
- Sistema de logging básico
- Demonstrações funcionais

### O que NÃO FUNCIONA ❌
- Caminhos hardcoded (`C:\Users\Usuário\FUSAO_EXTREMA`)
- Sem testes unitários
- Sem API REST
- Sem tratamento robusto de erros
- Estrutura desordenada
- Sem documentação técnica
- Sem versionamento de config
- Sem suporte a múltiplos modelos

### Problemas Críticos 🚨
1. **Hardcoded paths** - Quebra em qualquer outro PC
2. **No tests** - Impossível fazer refactor seguro
3. **Missing arsenal/** - Módulos não existem (vazio)
4. **No config management** - Tudo em código
5. **No error handling** - Vai falhar silenciosamente

---

## 🎯 FASES DE REFACTOR

### FASE 1: Setup Profissional (Semana 1)

#### 1.1 - Estrutura de Diretórios
```
FUSAO_EXTREMA/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── intelligence_fusion.py          [REFACTOR]
│   │   ├── logger_system.py                [REFACTOR]
│   │   └── orchestrator.py                 [REFACTOR de main_fusion_orchestrator.py]
│   ├── models/
│   │   ├── __init__.py
│   │   └── model_manager.py                [NOVO]
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py                       [NOVO - Config Management]
│   │   └── validators.py                   [NOVO - Input Validation]
│   └── api/
│       ├── __init__.py
│       └── server.py                       [NOVO - FastAPI]
├── tests/
│   ├── __init__.py
│   ├── test_core.py                        [NOVO]
│   ├── test_fusion.py                      [NOVO]
│   ├── test_orchestrator.py                [NOVO]
│   └── conftest.py                         [NOVO]
├── config/
│   ├── base_config.yaml                    [NOVO]
│   ├── development.yaml                    [NOVO]
│   ├── production.yaml                     [NOVO]
│   └── .env.example                        [NOVO]
├── docs/
│   ├── ARCHITECTURE.md                     [NOVO]
│   ├── API.md                              [NOVO]
│   └── CONTRIBUTING.md                     [NOVO]
├── requirements.txt                         [NOVO]
├── requirements-dev.txt                     [NOVO]
├── pytest.ini                              [NOVO]
├── setup.py                                [NOVO]
├── README.md                               [ATUALIZAR]
└── .gitignore                              [NOVO]
```

#### 1.2 - Criar requirements.txt
```bash
# Core
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0

# AI/ML
anthropic==0.7.0
google-generativeai==0.3.0

# Utilities
pyyaml==6.0.1
python-json-logger==2.0.7

# Development & Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
black==23.12.0
flake8==6.1.0
mypy==1.7.0
```

#### 1.3 - Criar Config Management
```python
# src/utils/config.py
import os
from pathlib import Path
from typing import Dict, Any
import yaml
from dotenv import load_dotenv

class Config:
    """Gerenciador centralizado de configurações"""
    
    def __init__(self, env: str = "development"):
        self.env = env
        self.base_path = Path(__file__).parent.parent.parent
        self.config_path = self.base_path / "config"
        
        # Carregar .env
        load_dotenv(self.config_path / ".env")
        
        # Carregar YAML config
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Carrega configuração de arquivo YAML"""
        base_config = yaml.safe_load(
            open(self.config_path / "base_config.yaml")
        )
        env_config = yaml.safe_load(
            open(self.config_path / f"{self.env}.yaml")
        )
        return {**base_config, **env_config}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtém valor de config com fallback para env vars"""
        # 1. Tenta env var
        env_key = f"FUSION_{key.upper()}"
        if env_key in os.environ:
            return os.environ[env_key]
        
        # 2. Tenta arquivo YAML
        if key in self.config:
            return self.config[key]
        
        # 3. Retorna default
        return default

# Uso:
# config = Config()
# api_key = config.get("anthropic_api_key")
```

---

### FASE 2: Refactor Core (Semana 1.5)

#### 2.1 - Refactor intelligence_fusion.py
```python
# PROBLEMAS ATUAIS:
# ❌ Hardcoded paths
# ❌ Sem tipagem
# ❌ Sem docstrings
# ❌ Sem error handling
# ❌ Classe única sem modularização

# SOLUÇÃO:
# ✅ Usar Config management
# ✅ Type hints completo
# ✅ Docstrings em Google style
# ✅ Raise exceptions específicas
# ✅ Estratégias de fusão modulares
```

#### 2.2 - Criar Custom Exceptions
```python
# src/core/exceptions.py
class FusionException(Exception):
    """Base exception for fusion system"""
    pass

class ModelNotAvailableError(FusionException):
    """Model is not available"""
    pass

class ConfigurationError(FusionException):
    """Invalid configuration"""
    pass

class FusionProcessError(FusionException):
    """Error during fusion process"""
    pass

class APIError(FusionException):
    """Error calling external API"""
    pass
```

#### 2.3 - Criar Model Manager
```python
# src/models/model_manager.py
from typing import Dict, List, Callable
from enum import Enum

class ModelProvider(Enum):
    CLAUDE = "claude"
    GEMINI = "gemini"
    LLAMA = "llama"
    MISTRAL = "mistral"

class ModelManager:
    """Gerencia múltiplos modelos de IA"""
    
    def __init__(self, config):
        self.config = config
        self.providers: Dict[ModelProvider, Callable] = {}
        self._register_providers()
    
    def _register_providers(self):
        """Registra provedores de modelo"""
        # Será preenchido com integrações reais
        pass
    
    def call_model(self, provider: ModelProvider, prompt: str) -> str:
        """Chama modelo específico"""
        if provider not in self.providers:
            raise ModelNotAvailableError(f"{provider} not available")
        
        return self.providers[provider](prompt)
    
    def list_available_models(self) -> List[str]:
        """Lista modelos disponíveis"""
        return [p.value for p in ModelProvider]
```

---

### FASE 3: Testes (Semana 2)

#### 3.1 - Unit Tests
```python
# tests/test_fusion.py
import pytest
from src.core.intelligence_fusion import IntelligenceFusion
from src.core.exceptions import FusionProcessError

@pytest.fixture
def fusion_engine():
    return IntelligenceFusion()

def test_synergy_score(fusion_engine):
    """Testa cálculo de sinergia"""
    score = fusion_engine.calculate_synergy_score(
        "Claude response",
        "Gemini response"
    )
    assert 0 <= score <= 1

def test_task_classification(fusion_engine):
    """Testa classificação de tarefa"""
    task_type = fusion_engine.determine_task_type(
        "How to optimize a Python algorithm?"
    )
    assert task_type in ["technical", "creative", "analytical", "problem_solving", "general"]

def test_invalid_input_raises_error(fusion_engine):
    """Testa validação de entrada"""
    with pytest.raises(ValueError):
        fusion_engine.calculate_synergy_score("", "")

# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = --cov=src --cov-report=html --strict-markers
markers =
    slow: marks tests as slow
    integration: marks tests as integration
```

#### 3.2 - Integration Tests
```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from src.api.server import app

@pytest.fixture
def client():
    return TestClient(app)

def test_fuse_endpoint(client):
    """Testa endpoint /api/v1/fuse"""
    response = client.post("/api/v1/fuse", json={
        "prompt": "Test prompt",
        "models": ["claude", "gemini"],
        "strategy": "weighted"
    })
    assert response.status_code == 200
    assert "result" in response.json()
```

---

### FASE 4: API REST (Semana 2)

#### 4.1 - FastAPI Server
```python
# src/api/server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Fusion AI API",
    version="1.0.0",
    docs_url="/api/docs"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)

class FuseRequest(BaseModel):
    prompt: str
    models: List[str] = ["claude", "gemini"]
    strategy: str = "weighted"
    task_type: str = "auto"
    return_details: bool = False

class FuseResponse(BaseModel):
    result: str
    synergy_score: float
    task_type: str
    models_used: List[str]

@app.post("/api/v1/fuse", response_model=FuseResponse)
async def fuse(request: FuseRequest):
    """Executa fusão de modelos"""
    try:
        result = orchestrator.fuse(
            prompt=request.prompt,
            models=request.models,
            strategy=request.strategy,
            task_type=request.task_type
        )
        return FuseResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/models")
async def get_models():
    """Lista modelos disponíveis"""
    return {"models": model_manager.list_available_models()}

@app.get("/api/v1/health")
async def health():
    """Health check"""
    return {"status": "ok", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### 4.2 - Executar servidor
```bash
# Terminal
python -m uvicorn src.api.server:app --reload

# Acessar:
# http://localhost:8000/api/docs (Swagger UI)
# http://localhost:8000/api/v1/health (Health check)
```

---

### FASE 5: Melhorias & Expansões (Semana 3)

#### 5.1 - Multi-Model Support
```python
# Adicionar suporte para mais modelos

class LlamaProvider:
    """Integração com Llama via Ollama"""
    def __call__(self, prompt: str) -> str:
        # Implementar

class MistralProvider:
    """Integração com Mistral AI"""
    def __call__(self, prompt: str) -> str:
        # Implementar

class GPT4Provider:
    """Integração com GPT-4 (OpenAI)"""
    def __call__(self, prompt: str) -> str:
        # Implementar
```

#### 5.2 - Estratégias de Fusão Avançadas
```python
class FusionStrategy:
    """Base class para estratégias"""
    def fuse(self, responses: List[str]) -> str:
        pass

class DebateStrategy(FusionStrategy):
    """Modelos debatem e chegam a conclusão"""
    def fuse(self, responses: List[str]) -> str:
        # Implementar lógica de debate

class TournamentStrategy(FusionStrategy):
    """Maioria vence"""
    def fuse(self, responses: List[str]) -> str:
        # Implementar votação

class SequentialRefinementStrategy(FusionStrategy):
    """Modelo 1 → Modelo 2 refina"""
    def fuse(self, responses: List[str]) -> str:
        # Implementar refinamento sequencial
```

#### 5.3 - Caching & Performance
```python
# src/utils/cache.py
import redis
from functools import wraps

redis_client = redis.Redis()

def cache_response(ttl=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Hash dos args como chave
            key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Tenta recuperar do cache
            cached = redis_client.get(key)
            if cached:
                return json.loads(cached)
            
            # Executa função e cacheia resultado
            result = func(*args, **kwargs)
            redis_client.setex(key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_response(ttl=3600)
def fuse_with_cache(prompt, models):
    # Implementação
    pass
```

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### Semana 1
- [ ] Criar estrutura de diretórios
- [ ] Criar requirements.txt
- [ ] Implementar Config management
- [ ] Refactor intelligence_fusion.py
- [ ] Remover hardcoded paths
- [ ] Criar Custom exceptions

### Semana 2
- [ ] Criar 20+ unit tests
- [ ] Criar Model manager
- [ ] Implementar FastAPI server
- [ ] Integrar 4 endpoints básicos
- [ ] Setup CI/CD (GitHub Actions)

### Semana 3
- [ ] Multi-model support (Llama, Mistral)
- [ ] Estratégias avançadas (Debate, Tournament)
- [ ] Caching com Redis
- [ ] Dashboard web (React)
- [ ] Documentação técnica completa

---

## 🚀 RESULTADO FINAL

```
ANTES (7/10):
✅ Funciona
❌ Hardcoded paths
❌ Sem testes
❌ Sem API
❌ Sem docs

DEPOIS (8.5/10):
✅ Funciona
✅ Config management
✅ 80%+ test coverage
✅ REST API completa
✅ Docs técnicas
✅ Multi-model
✅ Caching
✅ Production-ready
```

---

## 📞 Como Executar

```bash
# 1. Clone
git clone https://github.com/guimilgraubr/FUSAO_EXTREMA
cd FUSAO_EXTREMA

# 2. Setup virtual env
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Install deps
pip install -r requirements-dev.txt

# 4. Run tests
pytest --cov=src

# 5. Run API
python -m uvicorn src.api.server:app --reload

# 6. Access
# Swagger UI: http://localhost:8000/api/docs
```

---

**Status**: 🔴 Planejado
**Próximo Passo**: Iniciar implementação Fase 1
