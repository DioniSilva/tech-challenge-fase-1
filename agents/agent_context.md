# Contexto Do Tech Challenge Fase 01

O Tech Challenge pede construir um projeto completo de Machine Learning para previsao de churn de clientes de telecom, com foco em uma rede neural MLP em PyTorch, comparada com modelos baseline em Scikit-Learn, rastreada com MLflow e servida via API FastAPI.

## Entrega Obrigatoria

- Repositorio GitHub organizado.
- Video de ate 5 minutos usando metodo STAR.
- Projeto funcional do notebook ate a API.
- Deploy em nuvem e opcional e vale bonus.

## Tema

Criar um modelo que classifique clientes com risco de cancelamento/churn para apoiar uma operadora de telecom.

## Dataset

Pode usar o dataset sugerido Telco Customer Churn - IBM ou outro dataset de classificacao binaria com:

- Pelo menos 5.000 registros.
- Pelo menos 10 features.

## Estrutura Esperada Do Repositorio

- `src/`
- `data/`
- `models/`
- `tests/`
- `notebooks/`
- `docs/`
- `README.md`
- `pyproject.toml`
- `.gitignore`
- `Makefile`

## Bibliotecas Obrigatorias

- `PyTorch`: modelo MLP.
- `Scikit-Learn`: preprocessing, pipelines e baselines.
- `MLflow`: tracking de experimentos.
- `FastAPI`: API de inferencia.

## Boas Praticas Obrigatorias

- Seeds fixados para reprodutibilidade.
- Validacao cruzada estratificada.
- Model Card com limitacoes, vieses e cenarios de falha.
- Pelo menos 3 testes automatizados: smoke test, schema e API.
- Logging estruturado, sem `print()`.
- Linting com `ruff` sem erros.

## Etapa 1: Entendimento E Preparacao

Entregavel: notebook de EDA + baselines registrados no MLflow.

Deve conter:

- ML Canvas: stakeholders, metricas de negocio, SLOs.
- EDA completa: volume, qualidade, distribuicao, prontidao dos dados.
- Definicao de metricas tecnicas: AUC-ROC, PR-AUC, F1 etc.
- Definicao de metrica de negocio: custo de churn evitado.
- Baselines com `DummyClassifier` e `Regressao Logistica`.
- Registro dos experimentos no MLflow.

## Etapa 2: Modelagem Com Redes Neurais

Entregavel: tabela comparativa de modelos + MLP treinado + artefatos no MLflow.

Deve conter:

- MLP em PyTorch.
- Definicao de arquitetura, ativacoes e loss function.
- Loop de treinamento com batching.
- Early stopping.
- Comparacao contra baselines lineares e arvores.
- Pelo menos 4 metricas.
- Analise de custo entre falso positivo e falso negativo.
- Registro de todos os experimentos no MLflow.

## Etapa 3: Engenharia E API

Entregavel: repositorio refatorado + API funcional + testes passando.

Deve conter:

- Codigo modular em `src/`.
- Pipeline reprodutivel com Scikit-Learn e, se necessario, transformadores customizados.
- Testes com `pytest`.
- Validacao de schema, preferencialmente com `pandera`.
- API FastAPI com endpoints `/health` e `/predict`.
- Validacao com Pydantic.
- Logging estruturado.
- Middleware de latencia.
- `pyproject.toml`, `ruff` e `Makefile` com comandos de lint, test e run.

## Etapa 4: Documentacao E Entrega Final

Entregavel: repositorio final + video STAR + opcionalmente URL de deploy.

Deve conter:

- Model Card completo.
- Documentacao da arquitetura de deploy escolhida: batch ou real-time.
- Justificativa da escolha.
- Plano de monitoramento: metricas, alertas e playbook.
- README final com setup, execucao e arquitetura.
- Video de 5 minutos usando STAR:
- Situation: problema de negocio e dataset.
- Task: tarefa do grupo e objetivos tecnicos.
- Action: decisoes tecnicas, features, modelo e metricas.
- Result: resultados e aprendizados.

## Criterios De Avaliacao

- 25%: rede neural PyTorch.
- 20%: qualidade do codigo e estrutura.
- 15%: pipeline e reprodutibilidade.
- 15%: API de inferencia.
- 10%: documentacao e Model Card.
- 10%: video STAR.
- 5% bonus: deploy em nuvem.

## Resumo Operacional

O projeto precisa demonstrar um pipeline profissional end-to-end de Machine Learning, desde analise exploratoria e baselines ate MLP em PyTorch, rastreamento com MLflow, API FastAPI, testes, documentacao e apresentacao final.
