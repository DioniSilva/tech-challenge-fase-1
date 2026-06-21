# Experimentos Das Etapas 1 E 2

Esta pagina consolida a trilha oficial de experimentos antes da refatoracao para API.

## Trilha Oficial

Notebooks canonicos:

1. `notebooks/Etapa_01-EDA.ipynb`
2. `notebooks/Etapa_02-Modelagem_com_Redes_Neurais.ipynb`

Arquivos de apoio:

- `docs/docs/ml-canvas.md`
- `docs/docs/dataset.md`
- `docs/docs/mlflow.md`
- `reports/plano-consolidacao-etapas-1-2.md`

## Etapa 1: Entendimento E Preparacao

Status atual: parcialmente fechado.

Implementado:

- EDA do dataset Telco Customer Churn IBM.
- ML Canvas gerado a partir de `src/ml_pipeline/ml_canvas.py`.
- Definicao inicial de metricas tecnicas como precision, recall, F1 e ROC-AUC.
- Discussao de metrica de negocio relacionada ao custo de churn evitado.
- Baselines com `DummyClassifier` e `LogisticRegression`.
- Registro de experimentos no MLflow.
- Persistencia de baseline em `models/baseline_model.joblib`.

Pendencias de consolidacao:

- Explicitar conclusoes finais da EDA em formato executivo.
- Padronizar o uso de MLflow apenas em `data/mlflow_tracking/mlflow.db`, com artefatos em `data/mlflow_tracking/artifacts/`.
- Garantir split estratificado no fluxo canonico da Etapa 1.
- Formalizar a metrica de negocio usada na comparacao final.

## Etapa 2: Modelagem Com Redes Neurais

Status atual: implementado com pendencias de consolidacao.

Implementado:

- MLP em PyTorch com `nn.Sequential`.
- Loss `BCEWithLogitsLoss`.
- Batching com `DataLoader` e `TensorDataset`.
- Early stopping com conjunto de validacao estratificado.
- Comparacao com `LogisticRegression`, `DecisionTreeClassifier`, `RandomForestClassifier` e `GradientBoostingClassifier`.
- Metricas de avaliacao: accuracy, precision, recall, F1, ROC-AUC e PR-AUC.
- Analise de custo-beneficio considerando custo de retencao, CLTV e taxa de conversao.
- Figuras comparativas em `reports/figures/`.

Pendencias de consolidacao:

- Reexecutar o notebook apos a inclusao de `StratifiedKFold` explicito para atualizar os outputs.
- Consolidar runs finais do MLflow com nomes e tags padronizados.
- Criar uma tabela final unica em formato tabular versionavel.
- Declarar o modelo escolhido para a API.

## Politica Canonica De Features

As seguintes features devem ser removidas antes do treino por identificacao, redundancia, baixa utilidade operacional ou vazamento de informacao:

| Feature normalizada | Motivo |
|---|---|
| `customerid` | Identificador unico sem poder generalizavel |
| `count` | Coluna auxiliar de contagem |
| `country` | Baixa variabilidade no dataset |
| `state` | Baixa variabilidade no dataset |
| `city` | Alta cardinalidade e dependencia geografica local |
| `lat_long` | Redundante com latitude/longitude e pouco adequada para API inicial |
| `latitude` | Feature geografica removida para reduzir dependencia local |
| `longitude` | Feature geografica removida para reduzir dependencia local |
| `churn_label` | Duplicata textual do target |
| `churn_score` | Vazamento/fonte futura gerada por outro modelo |
| `cltv` | Variavel derivada potencialmente futura para decisao de churn |
| `churn_reason` | Vazamento: so existe para clientes que cancelaram |

`total_charges` deve ser convertido para numerico e valores ausentes devem ser tratados. A feature derivada `average_monthly_spend` nao faz parte do fluxo canonico ate haver evidencia comparativa de ganho.

## MLflow Canonico

Backend oficial:

```text
data/mlflow_tracking/mlflow.db
```

Artifact store oficial:

```text
data/mlflow_tracking/artifacts/
```

Experimentos canonicos:

- `Tech Challenge - Etapa 1`
- `Tech Challenge - Etapa 2`

Runs finais devem usar nomes consistentes:

- `baseline_dummy_classifier`
- `baseline_logistic_regression`
- `decision_tree_classifier`
- `random_forest_classifier`
- `gradient_boosting_classifier`
- `mlp_pytorch`

Tags recomendadas:

- `stage`: `baseline`, `candidate` ou `final`
- `model_family`: `dummy`, `linear`, `tree`, `ensemble` ou `neural_network`
- `dataset`: `telco_customer_churn_ibm`
- `target`: `churn_value`
- `phase`: `etapa_1` ou `etapa_2`

O notebook canonico da Etapa 2 registra metricas de validacao cruzada para modelos sklearn com prefixos `cv_test_*_mean` e `cv_test_*_std`.

File stores antigos em `data/mlflow_tracking/mlruns`, `notebooks/mlruns` e `notebooks/mlflow.db` sao legado e nao devem ser usados como fonte canonica.

Experimentos antigos como `churn_model_classification`, `TechChallenge - Etapa 02`, `ML Experiments`, `Modelagem de Rede Neural` e `Telco Churn Customer Analysis` foram consolidados/arquivados para manter a UI focada nos dois experimentos canonicos.

## Criterio Para Fechar Etapas 1 E 2

As Etapas 1 e 2 ficam prontas para refatoracao em API quando:

- A validacao cruzada estratificada estiver explicita e os outputs do notebook estiverem atualizados.
- A tabela comparativa final existir em formato versionavel.
- Os runs finais do MLflow estiverem identificaveis.
- O modelo escolhido para API estiver declarado.
- Notebooks WIP nao fizerem parte da trilha oficial.
- A politica de features estiver refletida no notebook canonico e no futuro pipeline.
