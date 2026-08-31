import logging
print("Logging importado")

from pathlib import Path
print("Path importado")

# Teste de criação de diretório
log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)
print("Diretório de logs criado")

# Teste de configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('TestLogger')
logger.info("Logger configurado")
print("Logger configurado com sucesso")