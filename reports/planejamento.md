<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Plano de Projeto - Etapas</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
    h1 { color: #2c3e50; }
    h2 { color: #34495e; margin-top: 30px; }
    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
    th { background-color: #f4f4f4; }
    .entregavel { margin-top: 10px; font-weight: bold; }
  </style>
</head>
<body>

<h1>Plano de Projeto sugerido</h1>
Cada integrante deve por favor identificar com quais atividades estão mais familiarizados, escrever seu nome na coluna "Responsável" e confirmar a data sugerida. Uma vez que a atividade é entregue e revisada, preencher com "Feito".

<!-- Etapas 1 a 4 já existentes -->

<h2>Etapa 1 — Entendimento e Preparação (Disciplinas 01 e 02)</h2>
<p><strong>Foco:</strong> formulação do problema, exploração de dados e construção de baselines.</p>
<table>
  <tr><th>Tarefa</th><th>Referência</th><th>Responsável</th><th>Data limite</th></tr>
  <tr><td>Preencher ML Canvas (stakeholders, métricas de negócio, SLOs)</td><td>Ciclo de Vida, Aula 01 / Tech Challenge 4</td><td>Feito</td><td>Feito</td></tr>
  <tr><td>EDA completa: volume, qualidade, distribuição, data readiness</td><td>Ciclo de Vida, Aula 01</td><td>Feito</td><td>Feito</td></tr>
  <tr><td>Definir métrica técnica (AUC-ROC, PR-AUC, F1) e métrica de negócio (custo de churn evitado)</td><td>Fundamentos, Aula 05</td><td>Feito</td><td>Feito</td></tr>
  <tr><td>Treinar baseline com DummyClassifier e Regressão Logística (Scikit-Learn)</td><td>Fundamentos, Aulas 01–02</td><td>Feito</td><td>Feito</td></tr>
  <tr><td>Registrar experimentos no MLflow (parâmetros, métricas, dataset version)</td><td>Ciclo de Vida, Aula 02</td><td>Rodrigo</td><td>20/05/2026</td></tr>
</table>
<p class="entregavel">Entregável: notebook de EDA + baselines registrados no MLflow.</p>

<h2>Etapa 2 — Modelagem com Redes Neurais (Disciplina 02)</h2>
<p><strong>Foco:</strong> Construção, treinamento e avaliação de MLP com PyTorch.</p>
<table>
  <tr><th>Tarefa</th><th>Referência</th><th>Responsável</th><th>Data limite</th></tr>
  <tr><td>Construir MLP em PyTorch: definir arquitetura, função de ativação, loss function</td><td>Fundamentos, Aula 04</td><td></td><td>22/05/2026</td></tr>
  <tr><td>Implementar loop de treinamento com early stopping e batching</td><td>Fundamentos, Aula 04</td><td></td><td>24/05/2026</td></tr>
  <tr><td>Comparar MLP vs. baselines (lineares + árvores) usando ≥ 4 métricas</td><td>Fundamentos, Aula 05</td><td></td><td>26/05/2026</td></tr>
  <tr><td>Analisar trade-off de custo (falso positivo vs. negativo)</td><td>Fundamentos, Aula 05</td><td></td><td>27/05/2026</td></tr>
  <tr><td>Registrar todos os experimentos (MLP e ensembles) no MLflow</td><td>Ciclo de Vida, Aula 02</td><td></td><td>29/05/2026</td></tr>
</table>
<p class="entregavel">Entregável: tabela comparativa de modelos + MLP treinado + artefatos no MLflow.</p>

<h2>Etapa 3 — Engenharia e API (Disciplinas 03, 04 e 05)</h2>
<p><strong>Foco:</strong> refatoração profissional, API de inferência e pacote reutilizável.</p>
<table>
  <tr><th>Tarefa</th><th>Referência</th><th>Responsável</th><th>Data limite</th></tr>
  <tr><td>Refatorar código em módulos (src/) com estrutura limpa</td><td>Eng. Software, Aula 01</td><td></td><td>31/05/2026</td></tr>
  <tr><td>Criar pipeline reprodutível (sklearn + transformadores custom)</td><td>Eng. Software, Aula 01; Bibliotecas, Aula 02</td><td></td><td>31/05/2026</td></tr>
  <tr><td>Escrever testes (pytest): unitários, schema (pandera), smoke test</td><td>Eng. Software, Aula 03</td><td></td><td>03/06/2026</td></tr>
  <tr><td>Construir API FastAPI: /predict, /health, validação Pydantic</td><td>APIs, Aulas 01–03</td><td></td><td>05/06/2026</td></tr>
  <tr><td>Adicionar logging estruturado e middleware de latência</td><td>APIs, Aula 04</td><td></td><td>07/06/2026</td></tr>
  <tr><td>Configurar pyproject.toml, ruff, Makefile (lint, test, run)</td><td>Eng. Software, Aulas 04–05</td><td></td><td>10/06/2026</td></tr>
</table>
<p class="entregavel">Entregável: repositório refatorado + API funcional + testes passando.</p>

<h2>Etapa 4 — Documentação e Entrega Final (Todas as disciplinas)</h2>
<p><strong>Foco:</strong> consolidação, documentação e vídeo de apresentação.</p>
<table>
  <tr><th>Tarefa</th><th>Referência</th><th>Responsável</th><th>Data limite</th></tr>
  <tr><td>Gerar Model Card completo (performance, limitações, vieses, cenários de falha)</td><td>Ciclo de Vida, Aula 11</td><td></td><td>30/06/2026</td></tr>
  <tr><td>Documentar arquitetura de deploy escolhida (batch vs. real-time) + justificativa</td><td>Ciclo de Vida, Aula 04</td><td></td><td>13/06/2026</td></tr>
  <tr><td>Criar plano de monitoramento (métricas, alertas, playbook de resposta)</td><td>Ciclo de Vida, Aula 05</td><td></td><td>14/06/2026</td></tr>
  <tr><td>Finalizar README com instruções de setup + execução + arquitetura</td><td>Eng. Software / APIs</td><td></td><td>15/06/2026</td></tr>
  <tr><td>Gravar vídeo de 5 min (método STAR) demonstrando o projeto</td><td>—</td><td></td><td>20/06/2026</td></tr>
  <tr><td>(Opcional) Deploy da API em nuvem (AWS/Azure/GCP) com endpoint público</td><td>—</td><td></td><td>30/06/2026</td></tr>
</table>
<p class="entregavel">Entregável: repositório final + vídeo STAR + (opcional) URL do deploy em nuvem.</p>

<!-- Nova seção de Critérios de Avaliação -->

<h2>Critérios de Avaliação</h2>
<table>
  <tr><th>Critério</th><th>Peso</th><th>Descrição</th></tr>
  <tr><td>Qualidade do código e estrutura</td><td>25%</td><td>Organização, modularidade, SOLID, linting sem erros</td></tr>
  <tr><td>Rede neural (PyTorch)</td><td>25%</td><td>MLP funcional, treinamento com early stopping, comparação com baselines</td></tr>
  <tr><td>Pipeline e reprodutibilidade</td><td>15%</td><td>Pipeline sklearn, seeds, pyproject.toml, instala do zero</td></tr>
  <tr><td>API de inferência</td><td>15%</td><td>FastAPI funcional, Pydantic, logging, testes passando</td></tr>
  <tr><td>Documentação e Model Card</td><td>10%</td><td>Model Card completa, README claro, plano de monitoramento</td></tr>
  <tr><td>Vídeo STAR</td><td>10%</td><td>Clareza, cobertura dos quatro elementos STAR, dentro de cinco minutos</td></tr>
  <tr><td>Bônus: deploy em nuvem</td><td>+5%</td><td>API acessível via URL pública</td></tr>