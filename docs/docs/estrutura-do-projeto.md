# Estrutura do projeto

Esta página descreve a organização de pastas e arquivos principais do repositório.

```text
.
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── scripts/
│   └── validate_api.py
├── pyproject.toml
├── uv.lock
├── data/
│   ├── external/
│   ├── interim/
│   ├── mlflow_tracking/
│   ├── processed/
│   └── raw/
├── docs/
│   ├── mkdocs.yml
│   ├── docs/
│   └── site/
├── k8s/
│   ├── base/
│   └── overlays/
├── models/
├── notebooks/
├── reports/
│   └── figures/
├── src/
│   ├── api/
│   ├── core/
│   ├── data/
│   ├── ml_pipeline/
│   ├── modeling/
│   ├── schemas/
│   ├── services/
│   ├── ui/
│   └── utils/
└── tests/
```

## Raiz do repositório

| Caminho | Descrição |
|---|---|
| `README.md` | Porta de entrada do projeto no GitHub |
| `Makefile` | Atalhos para setup, treino, API, testes, docs, MLflow e Docker |
| `pyproject.toml` | Configuração do pacote, dependências e ferramentas |
| `Dockerfile` | Build da imagem da API |
| `scripts/validate_api.py` | Smoke check de imports, estrutura da API e configurações |
| `LICENSE` | Licença do projeto |

## Dados e artefatos

| Caminho | Descrição |
|---|---|
| `data/raw/` | Dados brutos, incluindo o dataset oficial versionado |
| `data/interim/` | Dados intermediários |
| `data/processed/` | Dados prontos para modelagem |
| `data/external/` | Dados externos |
| `data/mlflow_tracking/` | File store local do MLflow |
| `models/` | Modelos treinados, incluindo `models/mlp.joblib` |
| `reports/figures/` | Figuras usadas na documentação e relatórios |

## Código-fonte

| Caminho | Descrição |
|---|---|
| `src/api_main.py` | Ponto de entrada da aplicação FastAPI |
| `src/api/` | Roteadores e endpoints versionados |
| `src/core/` | Configurações centrais da aplicação |
| `src/data/` | Transformadores, configurações e modelos de dados auxiliares |
| `src/modeling/` | Componentes de modelagem, treino, avaliação e seleção |
| `src/schemas/` | Contratos Pydantic da API |
| `src/services/` | Camada de serviço para predição |
| `src/ui/` | Interface Streamlit e cliente HTTP da API |
| `src/utils/` | Utilitários de logging, MLflow, canvas e seleção de champion |
| `src/train_mlp.py` | Script de treinamento do modelo final MLP |

## Documentação

| Caminho | Descrição |
|---|---|
| `docs/mkdocs.yml` | Configuração do MkDocs |
| `docs/docs/` | Fontes Markdown da documentação |
| `docs/site/` | Site gerado pelo MkDocs |

## Deploy

| Caminho | Descrição |
|---|---|
| `k8s/base/` | Manifests base de Kubernetes |
| `k8s/overlays/local/` | Overlay local com namespace e kustomization |

## Notas de manutenção

- `docs/site/` é artefato gerado pelo MkDocs.
- `models/mlp.joblib` é gerado por `make train` e não deve ser versionado.
- Sempre que novos comandos forem adicionados ao `Makefile`, atualize também a página [Comandos](comandos.md).
- Sempre que novos módulos públicos forem adicionados em `src/`, atualize esta página.
