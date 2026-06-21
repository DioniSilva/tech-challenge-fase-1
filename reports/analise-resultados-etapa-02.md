# Analise Dos Resultados Da Etapa 2

Notebook analisado: `notebooks/Etapa_02-Modelagem_com_Redes_Neurais.ipynb`.

Data da execucao analisada: 2026-06-13.

## Estado Da Execucao

- O notebook foi reexecutado sem erros registrados nos outputs.
- Foram executadas 41 celulas.
- As figuras finais foram regeneradas em `reports/figures/`.
- A validacao cruzada estratificada foi executada para os modelos sklearn.
- O MLP foi avaliado por holdout estratificado com conjunto de validacao e early stopping.

## Validacao Cruzada Estratificada

Resultados em treino via `StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)`.

| Modelo | Accuracy media | Accuracy desvio | Precision media | Recall media | F1 media | ROC-AUC media |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.7602 | 0.0146 | 0.5333 | 0.7967 | 0.6383 | 0.8549 |
| Decision Tree Classifier | 0.7508 | 0.0201 | 0.5254 | 0.7130 | 0.6030 | 0.8213 |
| Random Forest Classifier | 0.7680 | 0.0139 | 0.5450 | 0.7819 | 0.6416 | 0.8528 |
| Gradient Boosting Classifier | 0.7941 | 0.0163 | 0.6073 | 0.6455 | 0.6248 | 0.8517 |

Leitura:

- `Gradient Boosting Classifier` lidera em accuracy media e precision media na CV.
- `Logistic Regression` lidera em recall medio e ROC-AUC medio na CV.
- `Random Forest Classifier` lidera em F1 medio na CV, com resultado muito proximo da regressao logistica.
- `Decision Tree Classifier` e o modelo mais fraco na CV, especialmente em F1 e ROC-AUC.

## Metricas No Conjunto De Teste

| Modelo | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC | Overfitting |
|---|---:|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.7729 | 0.5500 | 0.7941 | 0.6499 | 0.8635 | 0.6778 | -0.0102 |
| Decision Tree Classifier | 0.7850 | 0.5720 | 0.7540 | 0.6505 | 0.8442 | 0.6901 | -0.0118 |
| Random Forest Classifier | 0.7729 | 0.5506 | 0.7861 | 0.6476 | 0.8636 | 0.6717 | 0.0076 |
| Gradient Boosting Classifier | 0.8133 | 0.6377 | 0.6872 | 0.6615 | 0.8730 | 0.6881 | 0.0484 |
| MLP (PyTorch) | 0.7793 | 0.5602 | 0.7834 | 0.6533 | 0.8664 | 0.6810 | -0.0042 |

Leitura:

- `Gradient Boosting Classifier` teve melhor accuracy, precision, F1 e ROC-AUC no teste.
- `Decision Tree Classifier` teve o maior PR-AUC no teste, mas pior ROC-AUC e CV mais fraca; nao parece bom candidato final.
- `Logistic Regression` teve maior recall no teste, importante para churn quando falso negativo e caro.
- `MLP (PyTorch)` ficou competitivo: segundo melhor ROC-AUC, segundo melhor F1 e baixo overfitting.
- `Gradient Boosting Classifier` tem maior overfitting observado, mas ainda moderado.

## Custo-Beneficio

Melhor threshold por modelo conforme a simulacao de custo-beneficio.

| Modelo | Threshold | Clientes acionados | Clientes salvos estimados | Economia liquida |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.45 | 591 | 62.4 | 34593.00 |
| Decision Tree Classifier | 0.50 | 493 | 56.4 | 33943.00 |
| Random Forest Classifier | 0.45 | 611 | 63.6 | 34697.00 |
| Gradient Boosting Classifier | 0.35 | 535 | 60.6 | 36127.00 |
| MLP (PyTorch) | 0.45 | 572 | 61.4 | 34658.00 |

Leitura:

- `Gradient Boosting Classifier` teve maior economia liquida estimada.
- `Random Forest Classifier`, `MLP (PyTorch)` e `Logistic Regression` ficaram muito proximos em valor salvo.
- `MLP (PyTorch)` e competitivo no criterio de negocio, mas nao lidera.

## MLflow

Experimento criado na reexecucao:

```text
Tech Challenge - Etapa 2
```

Runs finais observadas:

| Modelo | Run ID |
|---|---|
| Logistic Regression | `d608c8672a1742f5a86e24e03fb16d7f` |
| Decision Tree Classifier | `89540df58b9d4c4b9bd94aad0c89043b` |
| Random Forest Classifier | `b7886e2bfb0344d68455fb9b7c00b57e` |
| Gradient Boosting Classifier | `b27fdd2872c44fb0bb5047069a87f766` |
| MLP (PyTorch) | `67d21372bf2d4c74a6a954e8919495df` |

Ponto de atencao:

- Estes runs foram gerados antes da padronizacao para SQLite.
- A fonte canonica definida para proximas execucoes e `data/mlflow_tracking/mlflow.db`, com artefatos em `data/mlflow_tracking/artifacts/`.
- Os resultados canônicos da Etapa 2 foram consolidados no experimento `Tech Challenge - Etapa 2`.
- File stores antigos em `data/mlflow_tracking`, `data/mlflow_tracking/mlruns` e `notebooks/mlruns` devem ser tratados como legado.

## Recomendacao De Modelo

Para a narrativa da Etapa 2:

- Melhor modelo tecnico no teste: `Gradient Boosting Classifier`.
- Melhor modelo de negocio na simulacao: `Gradient Boosting Classifier`.
- Modelo neural central do desafio: `MLP (PyTorch)`.

Recomendacao pratica:

- Declarar `Gradient Boosting Classifier` como melhor benchmark tabular nesta rodada.
- Declarar `MLP (PyTorch)` como modelo central exigido, competitivo e candidato preferencial para demonstracao da API se o objetivo for maximizar aderencia ao enunciado.
- Se a API servir apenas um modelo, escolher explicitamente entre melhor performance (`Gradient Boosting Classifier`) e aderencia ao requisito central (`MLP PyTorch`).

## Pendencias Antes Da API

- Reexecutar os notebooks canonicos usando o backend SQLite oficial do MLflow.
- Salvar tabela comparativa final em formato tabular versionavel, por exemplo `reports/model_comparison.csv`.
- Registrar tags consistentes nos runs finais.
- Decidir e documentar o modelo final que sera servido.
- Atualizar a documentacao das Etapas 1 e 2 com estes resultados consolidados.
