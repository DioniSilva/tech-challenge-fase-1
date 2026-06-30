# Roteiro do vídeo STAR

Roteiro do vídeo de avaliação - Tech Challenge Fase 1. O texto está estruturado
para slides narrados seguindo o método STAR, com tom técnico executivo e duração estimada de 5min.

## Visão geral dos slides

| Slide | Bloco STAR | Tempo alvo | Foco |
|---|---|---:|---|
| 1 | Situation | 0:00-0:35 | Problema de negócio e dataset |
| 2 | Task | 0:35-1:10 | Objetivos técnicos da entrega |
| 3 | Action | 1:10-2:05 | Arquitetura end-to-end |
| 4 | Action | 2:05-3:05 | Modelagem, avaliação e trade-offs |
| 5 | Action | 3:05-3:55 | API, contrato, testes e documentação |
| 6 | Result | 3:55-4:45 | Resultados, limitações e lições |
| 7 | Result | 4:45-4:55 | Fechamento |

## Slide 1 - Situation: problema e contexto

**Visual sugerido:** título do projeto, logo/ícone de telecom, e três blocos:
problema, dados e decisão de negócio.

**Narração:**

Olá, somos o grupo MLEks e vamos apresentar a entrega do Tech Challenge Fase 1. 
O problema de negócio que estamos lidando é churn em telecomunicações. 
Onde uma operadora que perde clientes precisa agir antes do
cancelamento. Em termos práticos, nossa equipe deve identificar clientes em risco antes que a empresa perca receita. 
Para isso, usamos o dataset Telco Customer Churn, com 7.043 registros e informações
demográficas, contratuais, de serviços e de cobrança como base de treino e teste para os modelos de machine learning apresentados. A pergunta central que nos propusemos a responder é: quais clientes têm maior risco de cancelar e devem receber retenção proativa?

## Slide 2 - Task: objetivo da entrega

**Visual sugerido:** lista curta com os principais requisitos: MLP, baselines,
MLflow, API, testes e documentação.

**Narração:**

Nossa tarefa foi transformar essa base histórica em uma solução de Machine
Learning de ponta a ponta. O objetivo não era entregar apenas um notebook, mas
um fluxo reprodutível: exploração dos dados, comparação de modelos, treinamento
e serviço de inferência. Para isso, desponibilizamos um MLP em
PyTorch como modelo central, baselines em scikit-learn, rastreabilidade com
MLflow e disponibilização por FastAPI estruterada em um projeto com Makefile,
testes automatizados, README, MkDocs e Model Card, registrando performance,
limitações e riscos de uso seguindo as melhores práticas de engenharia de software e de ML.


## Slide 3 - Action: arquitetura end-to-end

**Visual sugerido:** diagrama simples:
dataset -> EDA -> preprocessamento -> MLP -> MLflow -> `models/mlp.joblib` ->
FastAPI -> Streamlit/MkDocs.

**Narração:**

Nas ações, o primeiro passo foi organizar a arquitetura do projeto como um
pipeline profissional. O dataset base ficou versionado em
`data/raw/Telco_customer_churn.xlsx` visando a reprodutibilidade. As features selecionadas cobrem perfil demográfico,
contrato, serviços, cobrança, etc; no pré-processamento removemos campos de
identificação ou vazamento e preparamos os dados para o pipeline. O código de
produção foi separado em `src/`, com módulos para dados, modelagem, treino,
schemas, serviços e API. O treinamento gera `models/mlp.joblib`, carregado pela
API. Para reprodução, o Makefile concentra `make setup`, `make train`,
`make serve` e `make test`.

## Slide 4 - Action: modelagem e avaliação

**Visual sugerido:** tabela de modelos comparados e um bloco com escolhas da
MLP: batching, early stopping, dropout e seeds.

**Narração:**

Na modelagem, a entrega central foi uma MLP em PyTorch, implementada com
interface compatível com scikit-learn para funcionar dentro do pipeline. O
treinamento usa batches, validação interna, early stopping, dropout,
regularização e seeds fixas, além de suporte a validação cruzada estratificada.
Também comparamos a MLP com Logistic Regression, Decision Tree, Random Forest e
Gradient Boosting. Essa comparação foi importante porque churn é um problema
desbalanceado: nem sempre maior acurácia significa melhor decisão de retenção.
Por isso, avaliamos precisão, recall, F1, ROC-AUC, PR-AUC e custo-benefício. A
MLP é o artefato final servido pela API; os baselines explicam o trade-off e
apontam caminhos de evolução.

## Slide 5 - Action: engenharia e serving

**Visual sugerido:** endpoints da API, exemplo de payload validado e lista de
práticas de engenharia.

**Narração:**

Na engenharia, transformamos o modelo em um serviço de inferência. A API FastAPI
expõe dois endpoints principais: `/api/v1/health`, para verificar se o serviço e
o modelo estão disponíveis, e `/api/v1/predict`, para retornar a predição. O
contrato público usa Pydantic de forma estrita, com 20 variáveis, rejeição de
campos extras e validação de combinações incoerentes. Isso reduz o risco de uso em produção,
porque o experimento passa a ter contrato, validação e observabilidade. A
aplicação inclui logging estruturado, middleware de latência e testes
automatizados para API, schemas, pipeline, treinamento, UI e logging. Para
consumo, criamos uma interface Streamlit; para manutenção, o MkDocs centraliza
arquitetura, comandos, dataset, MLflow, Model Card e comparação de modelos.

## Slide 6 - Result: resultados e aprendizados

**Visual sugerido:** tabela de métricas do Model Card e bloco de limitações.

**Narração:**

Como resultado, o modelo final documentado no Model Card alcançou acurácia de
69,98 %, precisão de 45,94 %, sensibilidade de 89,86 %, F1 de 60,80 % e
ROC-AUC de 85,97 %. A sensibilidade é a métrica mais importante nesta leitura,
porque indica que o modelo captura 89,86 % dos clientes churners no conjunto
avaliado. Em churn, o maior risco de negócio é o falso negativo: o cliente que
cancelaria, mas não entra no radar de retenção. A alta sensibilidade traz um
custo: mais falsos positivos e ações para clientes que talvez não cancelassem.
Esse trade-off deve ser calibrado com custo de campanha e valor do cliente. As
limitações principais são desbalanceamento,
possível viés histórico, mudanças de mercado e drift. Por isso, recomendamos
monitorar performance, fairness e distribuição dos dados, além de reavaliar o
modelo periodicamente.

## Slide 7 - Fechamento

**Visual sugerido:** frase final com os quatro pilares: rastreável, testável,
documentado e pronto para inferência.

**Narração:**

Em resumo, a entrega conecta ciência de dados, engenharia e decisão de negócio.
Saímos de uma base histórica de churn, comparamos modelos, treinamos uma MLP em
PyTorch, registramos experimentos com MLflow e disponibilizamos a solução por
FastAPI. O resultado é uma solução rastreável, testável com pytest, documentada
com MkDocs e preparada para apoiar retenção em tempo real. Obrigado.

## Checklist de gravação

- Manter a fala em ritmo natural, sem ultrapassar 5 minutos.
- Mostrar pouco texto por slide; usar o roteiro como apoio de narração.
- Enfatizar os quatro blocos STAR verbalmente: situação, tarefa, ação e
  resultado.
- Não esconder o trade-off: a MLP é a entrega central, mas os baselines ajudam a
  avaliar custo-benefício e melhorias futuras.
- Encerrar com a mensagem de engenharia: solução reprodutível, servida por API,
  testada e documentada.
