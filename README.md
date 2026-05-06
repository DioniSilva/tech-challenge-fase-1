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
└── tech_challenge_fase_1   <- Codigo-fonte do projeto
    │
    ├── __init__.py             <- Torna `tech_challenge_fase_1` um modulo Python
    │
    └── ...                     <- Modulos do projeto (a evoluir)
```

--------
