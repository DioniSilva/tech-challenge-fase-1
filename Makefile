#################################################################################
# GLOBAIS                                                                       #
#################################################################################

PROJECT_NAME = tech-challenge-fase-1
PYTHON_VERSION = 3.12
UV_RUN = uv run
PYTHON_INTERPRETER = $(UV_RUN) python
HELP_PYTHON ?= python3
DOCKER_PYTHON ?= python
DATA_FILE = data/raw/Telco_customer_churn.xlsx

#################################################################################
# COMANDOS                                                                      #
#################################################################################


## Cria o ambiente uv e instala as dependencias
.PHONY: setup
setup:
	uv venv --python $(PYTHON_VERSION)
	@printf '%s\n' ">>> New uv virtual environment created. Activate with:"
	@printf '%s\n' ">>> Windows: .\.venv\Scripts\activate"
	@printf '%s\n' ">>> Unix/macOS: source ./.venv/bin/activate"
	uv sync --extra train --extra docs --extra notebook --extra dev --extra ui


## Cria ambiente enxuto para servir a API localmente
.PHONY: setup-runtime
setup-runtime:
	uv venv --python $(PYTHON_VERSION)
	@printf '%s\n' ">>> New uv virtual environment created. Activate with:"
	@printf '%s\n' ">>> Windows: .\.venv\Scripts\activate"
	@printf '%s\n' ">>> Unix/macOS: source ./.venv/bin/activate"
	uv sync


## Instalar dependencias do projeto em um interpretador alvo (uso no Docker)
.PHONY: install-runtime
install-runtime:
	uv pip install --python $(DOCKER_PYTHON) .


## Validar existencia do modelo treinado localmente
.PHONY: check-model
check-model:
	@if [ ! -f models/mlp.joblib ]; then \
		echo "models/mlp.joblib ausente. Rode 'make train' antes de compilar a imagem."; \
		exit 1; \
	fi


## Validar existencia do dataset de treino local
.PHONY: check-data
check-data:
	@if [ ! -f $(DATA_FILE) ]; then \
		echo "$(DATA_FILE) ausente. Verifique se o dataset oficial esta versionado em data/raw/."; \
		exit 1; \
	fi

## Compilar a imagem Docker usando o modelo treinado localmente
.PHONY: docker-build
docker-build: check-model
	docker build -t $(PROJECT_NAME):local .


## Lint com ruff (`make format` para formatar)
.PHONY: lint
lint:
	$(UV_RUN) ruff format --check
	$(UV_RUN) ruff check

## Formatar codigo-fonte com ruff (`make lint` para checar)
.PHONY: format
format:
	$(UV_RUN) ruff check --fix
	$(UV_RUN) ruff format

## Executar testes
.PHONY: test
test:
	$(UV_RUN) pytest tests --ignore=src/ml_pipeline --ignore=tests/test_api_endpoints.py -q

.PHONY: smoke
smoke:
	$(UV_RUN) pytest tests/test_smoke_pipeline.py tests/test_mlp.py --ignore=src/ml_pipeline -q

.PHONY: test-all
test-all:
	$(UV_RUN) pytest tests --ignore=src/ml_pipeline -q


## Servir a documentacao localmente (mkdocs)

## (Re)gerar pagina do ML Canvas (MkDocs)
.PHONY: docs-canvas
docs-canvas:
	$(UV_RUN) python src/utils/build_ml_canvas.py --out docs/docs/ml-canvas.md


.PHONY: docs docs-serve
docs: docs-canvas
	$(UV_RUN) mkdocs serve -f docs/mkdocs.yml

docs-serve: docs

## Gerar o site da documentacao (mkdocs)
.PHONY: docs-build
docs-build: docs-canvas
	$(UV_RUN) mkdocs build -f docs/mkdocs.yml


## Subir a UI do MLflow (historico local)
.PHONY: run-mlflow
run-mlflow:
	cd data/mlflow_tracking && \
		$(UV_RUN) mlflow ui


## Executar o projeto e a API, conforme existencia do modelo
## Se models/mlp.joblib não existir, roda src/train_mlp.py para treinar o modelo
## Inicia a API FastAPI em src/api_main.py
.PHONY: serve
serve:
	@if [ -n "$(WITH_UI)" ] && [ "$(WITH_UI)" != "true" ]; then \
		echo "Uso: make serve [WITH_UI=true]"; \
		exit 2; \
	fi
	@if [ ! -f models/mlp.joblib ]; then \
		$(MAKE) check-data || exit $$?; \
		$(PYTHON_INTERPRETER) src/train_mlp.py; \
	fi
	@if [ "$(WITH_UI)" = "true" ]; then \
		$(UV_RUN) uvicorn src.api_main:app --host 0.0.0.0 --port 8000 --reload & api_pid=$$!; \
		cleanup() { kill $$api_pid 2>/dev/null || true; wait $$api_pid 2>/dev/null || true; }; \
		trap cleanup EXIT INT TERM; \
		PYTHONPATH=src $(UV_RUN) streamlit run src/ui/app.py; \
	else \
		$(UV_RUN) uvicorn src.api_main:app --host 0.0.0.0 --port 8000 --reload; \
	fi

## Gerar o modelo MLP rodando o treinamento completo
.PHONY: train
train: check-data
	$(PYTHON_INTERPRETER) src/train_mlp.py

## Validar a API (verificar imports e estrutura)
.PHONY: api-validate
api-validate:
	$(PYTHON_INTERPRETER) scripts/validate_api.py


## Apagar arquivos Python compilados
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


#################################################################################
# REGRAS DO PROJETO                                                             #
#################################################################################



#################################################################################
# Comandos auto-documentados                                                    #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('\n'); \
print('Comandos disponíveis:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches])); \
print('\n')
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(HELP_PYTHON) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
