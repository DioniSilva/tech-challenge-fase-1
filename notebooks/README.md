# Notebooks

## Trilha Canonica Das Etapas 1 E 2

Execute e avalie os notebooks abaixo nesta ordem:

1. `Etapa_01-EDA.ipynb`
2. `Etapa_02-Modelagem_com_Redes_Neurais.ipynb`

## Etapa 1

`Etapa_01-EDA.ipynb` concentra a exploracao do dataset Telco Customer Churn, definicao inicial de metricas, tratamento de dados, baselines com `DummyClassifier` e `LogisticRegression`, persistencia do baseline e registros no MLflow.

Artefatos esperados:

- `data/raw/Telco_customer_churn_preprocessed.csv`
- `models/baseline_model.joblib`
- runs de baseline em `data/mlflow_tracking/mlflow.db`

## Etapa 2

`Etapa_02-Modelagem_com_Redes_Neurais.ipynb` concentra a comparacao entre modelos sklearn e MLP PyTorch, calculo de metricas tecnicas, analise de custo-beneficio e artefatos comparativos.

Artefatos esperados:

- `reports/figures/etapa02_grafico_comparativo_metricas_modelos.png`
- `reports/figures/etapa02_tabela_comparativa_metricas_modelos.png`
- `reports/figures/etapa02_tabela_comparativa_custo_beneficio_modelos.png`
- runs dos modelos candidatos em `data/mlflow_tracking/mlflow.db`

## Notebooks De Suporte Ou Legado

- `Etapa_01-Treina_e_compara_modelos.ipynb`: exploracao adicional de treino e comparacao; nao e a trilha principal.
- `Etapa_01-model_card.ipynb`: suporte para geracao do Model Card inicial; nao substitui a documentacao final.
- `Etapa_02-NN_model_WIP.ipynb`: rascunho/WIP; nao usar como evidencia principal da Etapa 2.

## MLflow

Use `data/mlflow_tracking/mlflow.db` como backend oficial do MLflow e `data/mlflow_tracking/artifacts/` como artifact store. Os experimentos canonicos sao `Tech Challenge - Etapa 1` e `Tech Challenge - Etapa 2`. `data/mlflow_tracking/mlruns`, `notebooks/mlruns` e `notebooks/mlflow.db` sao considerados legado local e nao devem ser usados como fonte canonica.
