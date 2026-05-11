# MLflow

Este projeto usa o MLflow em modo local (file store) para registrar experimentos.

## Onde fica o historico

O historico de experimentos fica em `data/mlflow_tracking/mlruns/`.

Para manter o repositorio leve, artefatos pesados (modelos, figuras, etc.) nao foram versionados.

## Como abrir a UI

Na raiz do repositorio:

```bash
make run-mlflow
```

Isso sobe o servidor local em `http://127.0.0.1:5000`.

Obs: o target `make run-mlflow` executa o comando dentro de `data/mlflow_tracking/`,
entao o MLflow usa o `./mlruns` desse diretorio automaticamente.

## Padrao de uso nos notebooks

Nos notebooks, configurar o tracking para usar o file store do projeto:

```python
import mlflow

mlflow.set_tracking_uri("file:../data/mlflow_tracking/mlruns")
mlflow.set_experiment("churn_model_classification")
```