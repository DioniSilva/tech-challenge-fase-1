# Tech Challenge Fase 1

Projeto Final Fase 1 MLET10

## Como executar

### Requisitos

- Python 3.12
- `uv` instalado

### Setup (ambiente + dependencias)

```bash
make setup
```

O target `make setup` instala o ambiente completo de desenvolvimento:
runtime da API, treino, notebooks, documentacao e testes.

Se voce quiser apenas subir a API localmente sem o stack de treino/notebook:

```bash
make setup-runtime
```

### Qualidade e testes

```bash
make lint
make format
make test
```

### Documentacao

```bash
make docs
make docs-build
```

### MLflow (UI)

```bash
make run-mlflow
```

## Docker

### Fluxo recomendado

O artefato `models/mlp.joblib` e gerado localmente e nao deve ser versionado.
Como a pasta `data/` fica fora do contexto do Docker, o build da imagem nao treina o modelo.
Neste repositorio, a origem oficial do modelo para a imagem Docker passa a ser local: `make train`.
O fluxo esperado e:

```bash
make setup
make train
make docker-build
```

### Build da imagem

```bash
make docker-build
```

### Execucao local

```bash
docker run --rm -p 8000:8000 tech-challenge-fase-1:local
```

A imagem embarca o codigo da API e o artefato `models/mlp.joblib`.
Se o arquivo nao existir, o build falha cedo com a instrucao para executar `make train` antes.
CI e registry de modelos continuam como evolucoes futuras; ainda nao sao a origem adotada neste projeto.
Por padrao, o container sobe a API FastAPI em `http://localhost:8000`.

## Kustomize

Os manifests Kubernetes ficam em `k8s/`.

### Renderizar manifests

```bash
kubectl kustomize k8s/overlays/local
```

### Aplicar no cluster

```bash
kubectl apply -k k8s/overlays/local
```

## Estrutura do Projeto

```
├── LICENSE            <- Licenca do projeto
├── Makefile           <- Atalhos (setup, lint, testes, docs)
├── README.md          <- README principal do projeto
├── data
│   ├── external       <- Dados de terceiros
│   ├── interim        <- Dados intermediarios transformados
│   ├── processed      <- Dados finais para modelagem
│   └── raw            <- Dados brutos (imutaveis)
│
├── docs               <- Documentacao (MkDocs)
│
├── models             <- Modelos treinados e artefatos
│
├── notebooks          <- Notebooks Jupyter. Convencao: numero (ordem),
│                         iniciais do autor e descricao curta, ex.:
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Config do projeto e ferramentas (ruff/pytest/mkdocs)
├── uv.lock            <- Lockfile do uv para reproducibilidade
│
├── references         <- Dicionarios de dados, manuais e materiais de apoio
│
├── reports            <- Relatorios gerados (HTML, PDF, etc.)
│   └── figures        <- Figuras/plots gerados para relatorios
│
└── src                       <- Codigo-fonte do projeto
    │
    ├── ml_pipeline            <- Modulos do pipeline de ML
    ├── utils                  <- Scripts utilitarios (ex.: build de docs)
    └── ...                    <- Modulos do projeto (a evoluir)
```

--------
