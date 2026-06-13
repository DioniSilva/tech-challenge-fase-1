# MLflow

Este projeto usa MLflow local com backend SQLite para registrar experimentos.

## Fonte Oficial

Backend store oficial:

```text
data/mlflow_tracking/mlflow.db
```

Artifact store oficial:

```text
data/mlflow_tracking/artifacts/
```

File stores antigos em `data/mlflow_tracking/mlruns`, `notebooks/mlruns` e `notebooks/mlflow.db` sao legado e nao devem ser usados como fonte canonica.

## Como Abrir A UI

Na raiz do repositorio:

```bash
make run-mlflow
```

Isso sobe o servidor local em `http://127.0.0.1:5000` usando:

```bash
uv run mlflow ui \
  --backend-store-uri sqlite:///data/mlflow_tracking/mlflow.db \
  --default-artifact-root file:<repo>/data/mlflow_tracking/artifacts
```

## Padrao De Uso Nos Notebooks

Nos notebooks, configurar o tracking para usar o SQLite do projeto:

```python
from pathlib import Path
import mlflow

tracking_dir = Path("../data/mlflow_tracking").resolve()
tracking_dir.mkdir(parents=True, exist_ok=True)
(tracking_dir / "artifacts").mkdir(parents=True, exist_ok=True)

mlflow.set_tracking_uri(f"sqlite:///{tracking_dir / 'mlflow.db'}")

experiment_name = "Tech Challenge - Etapa 1"
artifact_location = (tracking_dir / "artifacts" / experiment_name).as_uri()

experiment = mlflow.get_experiment_by_name(experiment_name)
if experiment is None:
    mlflow.create_experiment(experiment_name, artifact_location=artifact_location)

mlflow.set_experiment(experiment_name)
```

## Experimentos Recomendados

- `Tech Challenge - Etapa 1`: EDA, baselines e experimentos iniciais.
- `Tech Challenge - Etapa 2`: comparacao entre modelos sklearn e MLP PyTorch.

## O Que Cada Run Deve Registrar

Parametros:

- hiperparametros do modelo;
- `random_state`;
- configuracao de balanceamento;
- threshold quando aplicavel.

Metricas:

- accuracy;
- precision;
- recall;
- F1;
- ROC-AUC;
- PR-AUC;
- overfitting gap;
- custo-beneficio quando aplicavel;
- metricas de validacao cruzada com prefixos `cv_test_*_mean` e `cv_test_*_std`.

Artefatos:

- classification report;
- matriz de confusao;
- curva ROC;
- importancia de features quando disponivel;
- modelo treinado;
- tabelas comparativas finais.

Tags recomendadas:

- `stage`: `baseline`, `candidate` ou `final`;
- `model_family`: `dummy`, `linear`, `tree`, `ensemble` ou `neural_network`;
- `dataset`: `telco_customer_churn_ibm`;
- `target`: `churn_value`;
- `phase`: `etapa_1` ou `etapa_2`.

## Carregar Um Modelo

```python
from pathlib import Path
import mlflow

tracking_dir = Path("data/mlflow_tracking").resolve()
mlflow.set_tracking_uri(f"sqlite:///{tracking_dir / 'mlflow.db'}")

model_uri = "runs:/<RUN_ID>/model"
model = mlflow.pyfunc.load_model(model_uri)
```

## Estrutura Local Esperada

```text
data/mlflow_tracking/
├── mlflow.db
└── artifacts/
    ├── Tech Challenge - Etapa 1/
    └── Tech Challenge - Etapa 2/
```

## Migracao Dos Runs Antigos

O repositorio inclui um script para copiar runs legados para o backend SQLite canonico:

```bash
uv run python src/utils/migrate_mlflow_runs.py --dry-run --skip-artifacts
uv run python src/utils/migrate_mlflow_runs.py
```

O script:

- le `data/mlflow_tracking/mlruns`, `data/mlflow_tracking`, `notebooks/mlruns` e `notebooks/mlflow.db` por padrao;
- cria/reutiliza experimentos no `data/mlflow_tracking/mlflow.db`;
- copia params, metricas, tags e artefatos;
- adiciona tags `legacy.*` para rastrear a origem;
- e idempotente, entao uma segunda execucao pula runs ja migradas.

Relatorio gerado:

```text
reports/mlflow_migration_report.md
```

A estrategia recomendada depois da migracao e:

1. manter file stores antigos como legado local;
2. usar somente `mlflow.db` para novas execucoes;
3. considerar os runs migrados e novos no `mlflow.db` como fonte oficial.

Essa abordagem preserva reprodutibilidade e evita carregar para a entrega runs duplicados ou inconsistentes.

## Consolidacao Em Experimentos Canonicos

Para manter a UI focada na entrega, os runs relevantes foram consolidados em apenas dois experimentos ativos:

- `Tech Challenge - Etapa 1`
- `Tech Challenge - Etapa 2`

Script usado:

```bash
uv run python src/utils/consolidate_mlflow_experiments.py --dry-run --archive-old --skip-artifacts
uv run python src/utils/consolidate_mlflow_experiments.py --archive-old
```

O script copia runs canônicas, adiciona tags `canonical.*` e `legacy.*`, e pode arquivar experimentos antigos para que apenas os dois experimentos oficiais fiquem ativos.

Relatorio gerado:

```text
reports/mlflow_experiment_consolidation_report.md
```
