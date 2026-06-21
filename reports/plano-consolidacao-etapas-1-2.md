# Plano De Consolidacao Das Etapas 1 E 2

Este plano organiza as alteracoes necessarias para fechar as Etapas 1 e 2 antes da refatoracao para API.

## Objetivo

Transformar os experimentos atuais em uma base coerente, rastreavel e pronta para virar pipeline de inferencia.

## Escopo

- Etapa 1: EDA, ML Canvas, metricas, baselines e MLflow.
- Etapa 2: MLP PyTorch, comparacao com modelos sklearn, custo-beneficio e MLflow.
- Fora de escopo neste momento: API FastAPI, testes de API, deploy e Model Card final da Etapa 4.

## Decisoes Iniciais

- Notebooks canonicos:
  - `notebooks/Etapa_01-EDA.ipynb`
  - `notebooks/Etapa_02-Modelagem_com_Redes_Neurais.ipynb`
- MLflow oficial: `data/mlflow_tracking/mlflow.db` com artefatos em `data/mlflow_tracking/artifacts/`.
- Notebooks/artefatos WIP ou legados devem ficar fora da trilha de avaliacao.
- `total_charges` permanece como feature original corrigida; `average_monthly_spend` nao deve entrar no fluxo canonico sem evidencia comparativa.
- Validacao cruzada estratificada deve ser explicita para modelos sklearn; MLP pode usar holdout estratificado de validacao com early stopping, desde que documentado.

## Bloco 1: Trilha Canonica

Status: iniciado.

Tarefas:

- Documentar notebooks oficiais e ordem de execucao.
- Marcar notebooks WIP/legados como fora da trilha principal.
- Apontar artefatos esperados de cada notebook.

Aceite:

- Um avaliador sabe quais notebooks abrir e em que ordem.
- Nao ha ambiguidade entre notebook final e rascunho.

## Bloco 2: Politica De Features

Status: iniciado.

Tarefas:

- Consolidar features removidas por vazamento, identificacao ou baixa utilidade.
- Documentar tratamento de `total_charges`.
- Garantir que a politica seja a mesma da Etapa 2 e da futura API.

Aceite:

- A lista de features removidas esta documentada.
- O risco de vazamento por `churn_label`, `churn_score`, `cltv` e `churn_reason` esta explicitamente tratado.

## Bloco 3: Validacao Cruzada Estratificada

Status: iniciado.

Tarefas:

- Usar `StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)` no notebook canonico da Etapa 2. Status: feito.
- Executar a validacao cruzada no fluxo principal para modelos sklearn. Status: feito.
- Registrar media e desvio das metricas. Status: feito no MLflow para chaves `cv_test_*_mean` e `cv_test_*_std`.

Aceite:

- A validacao cruzada estratificada aparece explicitamente no notebook.
- Os resultados de CV sao comparaveis entre modelos sklearn.

## Bloco 4: MLflow Canonico

Status: pendente.

Tarefas:

- Padronizar nomes de runs finais.
- Padronizar tags de experimento.
- Registrar metricas e artefatos finais de forma consistente.
- Evitar uso de file stores legados como `data/mlflow_tracking/mlruns` e `notebooks/mlruns` como tracking oficial.

Aceite:

- Cada modelo final tem run identificavel no backend SQLite oficial do MLflow.
- A tabela final consegue apontar `run_id` ou nome da run de cada modelo.

## Bloco 5: Tabela Comparativa Final

Status: pendente.

Tarefas:

- Consolidar tabela final com metricas tecnicas, custo-beneficio, threshold e referencia MLflow.
- Salvar versao tabular em `reports/` alem das figuras ja existentes.
- Explicitar melhor modelo tecnico, melhor modelo financeiro e candidato para API.

Aceite:

- Existe uma fonte unica de verdade para a comparacao final.

## Bloco 6: Escolha Do Modelo Para API

Status: pendente.

Tarefas:

- Definir o modelo que sera servido na Etapa 3.
- Registrar justificativa considerando metricas, custo-beneficio, overfitting e aderencia ao desafio.

Aceite:

- A futura API tem um artefato-alvo claro.

## Bloco 7: Documentacao Das Etapas 1 E 2

Status: iniciado.

Tarefas:

- Criar pagina de documentacao com resumo de experimentos, features, validacao e lacunas. Status: feito em `docs/docs/experimentos-etapas-1-2.md`.
- Linkar a pagina no MkDocs. Status: feito.

Aceite:

- As decisoes principais podem ser entendidas sem abrir todos os notebooks.

## Bloco 8: Higiene De Artefatos

Status: pendente.

Tarefas:

- Revisar arquivos nao relacionados a churn em `data/`.
- Confirmar se devem ser removidos, arquivados ou apenas ignorados.
- Garantir que WIP e legados nao sejam apresentados como entrega principal.

Aceite:

- O repositorio comunica foco claro em churn prediction.

## Bloco 9: Verificacao Final

Status: pendente.

Tarefas:

- Reexecutar notebooks canonicos do zero.
- Conferir geracao dos artefatos esperados.
- Validar ausencia de vazamento de target.
- Confirmar que Etapas 1 e 2 estao prontas para refatoracao em API.

Aceite:

- Etapas 1 e 2 sao consideradas fechadas para iniciar Etapa 3.
