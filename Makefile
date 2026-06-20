#################################################################################
# GLOBAIS                                                                       #
#################################################################################

PROJECT_NAME = tech-challenge-fase-1
PYTHON_VERSION = 3.12
UV_RUN = uv run
PYTHON_INTERPRETER = $(UV_RUN) python

#################################################################################
# COMANDOS                                                                      #
#################################################################################


## Cria o ambiente uv e instala as dependências
.PHONY: setup
setup:
	uv venv --python $(PYTHON_VERSION)
	@echo ">>> New uv virtual environment created. Activate with:"
	@echo ">>> Windows: .\\.venv\\Scripts\\activate"
	@echo ">>> Unix/macOS: source ./.venv/bin/activate"
	uv sync


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
	$(UV_RUN) pytest tests --ignore=src/ml_pipeline

.PHONY: smoke
smoke:
	$(UV_RUN) pytest tests/test_smoke_pipeline.py tests/test_mlp.py --ignore=src/ml_pipeline -q


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


## Executar a API FastAPI (desenvolvimento com reload)
.PHONY: api-run
api-run:
	$(UV_RUN) uvicorn src.api_main:app --host 0.0.0.0 --port 8000 --reload


## Validar a API (verificar imports e estrutura)
.PHONY: api-validate
api-validate:
	$(PYTHON_INTERPRETER) validate_api.py


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
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
