# Comandos

Os comandos abaixo estão definidos no `Makefile` e rodam ferramentas dentro do ambiente gerenciado pelo `uv`.

## Ajuda

```bash
make help
```

Lista os comandos documentados no `Makefile`.

## Setup

```bash
make setup
```

Cria a virtualenv com `uv` e instala dependências de runtime, treino, notebooks, documentação, testes e UI.

```bash
make setup-runtime
```

Cria um ambiente enxuto apenas com as dependências necessárias para servir a API.

## Treinamento

```bash
make train
```

Executa `src/train_mlp.py` e gera `models/mlp.joblib`.

Requer o arquivo versionado `data/raw/Telco_customer_churn.xlsx`.

```bash
make check-data
```

Valida se `data/raw/Telco_customer_churn.xlsx` existe antes do treino.

```bash
make check-model
```

Valida se `models/mlp.joblib` existe antes do build Docker.

## API e UI

```bash
make serve
```

Sobe a API FastAPI em `http://localhost:8000`. Se o modelo ainda não existir, treina antes de iniciar o servidor.

```bash
make serve WITH_UI=true
```

Sobe a API e a interface Streamlit. A UI fica disponível em `http://localhost:8501`.

```bash
make api-validate
```

Valida imports e estrutura da API.

Também avisa quando `data/raw/Telco_customer_churn.xlsx` ou `models/mlp.joblib` ainda não existem.

## Lint e formatação

```bash
make lint
```

Valida formatação e regras de lint com `ruff`.

```bash
make format
```

Aplica correções automáticas e formata o código.

## Testes

```bash
make test
```

Roda a suíte principal de testes.

```bash
make smoke
```

Roda testes rápidos de smoke do pipeline e da MLP.

```bash
make test-all
```

Roda a suíte ampliada, mantendo apenas o ignore de `src/ml_pipeline`.

## Documentação

```bash
make docs
```

Gera o ML Canvas e sobe o servidor local do MkDocs.

```bash
make docs-build
```

Gera o site estático em `docs/site/`.

```bash
make docs-canvas
```

Regenera a página `docs/docs/ml-canvas.md`.

## MLflow

```bash
make run-mlflow
```

Sobe a UI do MLflow usando o file store em `data/mlflow_tracking/mlruns/`.

## Docker

```bash
make docker-build
```

Compila a imagem `tech-challenge-fase-1:local`. Esse target depende de `check-model`, portanto exige que `make train` já tenha sido executado.

## Limpeza

```bash
make clean
```

Remove caches e bytecode Python (`__pycache__`, `*.pyc`, `*.pyo`).
