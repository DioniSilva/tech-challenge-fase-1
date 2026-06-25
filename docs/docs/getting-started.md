# Primeiros passos

Este guia descreve o caminho mínimo para preparar o ambiente, treinar o modelo e subir a API localmente.

## Requisitos

- Python 3.12
- `uv`
- `make`

## Configurar ambiente

Use o ambiente completo de desenvolvimento:

```bash
make setup
```

Esse comando instala dependências de runtime, treino, notebooks, documentação, testes e UI.

Para instalar apenas o runtime da API:

```bash
make setup-runtime
```

## Preparar dados

O dataset oficial é versionado no repositório em:

```text
data/raw/Telco_customer_churn.xlsx
```

Sem esse arquivo, `make train` e o primeiro `make serve` falham porque o modelo ainda não pode ser gerado.

## Treinar o modelo

```bash
make train
```

O treinamento gera o artefato `models/mlp.joblib`, usado pelo serviço de predição.

> [!NOTE]
> Se `models/mlp.joblib` não existir, `make serve` executa o treinamento antes de iniciar a API.

## Subir a API

```bash
make serve
```

A API FastAPI fica disponível em:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/v1/health`

## Subir API e UI

```bash
make serve WITH_UI=true
```

A UI Streamlit fica disponível em `http://localhost:8501`.

## Rodar testes e qualidade

```bash
make lint
make test
```

Para aplicar formatação automática:

```bash
make format
```

## Abrir MLflow

```bash
make run-mlflow
```

A UI do MLflow fica disponível em `http://127.0.0.1:5000`.

## Documentação

Subir a documentação localmente:

```bash
make docs
```

Gerar o site estático em `docs/site/`:

```bash
make docs-build
```

A página do ML Canvas é gerada automaticamente pelo target `docs-canvas`, chamado por `make docs` e `make docs-build`.

## Docker

```bash
make setup
make train
make docker-build
docker run --rm -p 8000:8000 tech-challenge-fase-1:local
```
