# TELCO Customer Churn Prediction

Documentacao das definicoes do ML Canvas para o projeto de churn prediction.

> Data Readiness Score: 100%
>
> Projeto viavel: Sim



Para atualizar esta pagina, rode: `make docs-canvas`

<div class="ml-canvas-grid">

<section class="ml-canvas-card">
  <header class="ml-canvas-card__header">Problema de negocio</header>
  <div class="ml-canvas-card__body"><p>Reduzir o Churn através da identificação de clientes com perfis de alto risco de saída e alto LTV.</p></div>
</section>

<section class="ml-canvas-card">
  <header class="ml-canvas-card__header">Tarefa ML</header>
  <div class="ml-canvas-card__body"><p>Rede Neural para classificação binária (Churn: 0/1)</p></div>
</section>

<section class="ml-canvas-card">
  <header class="ml-canvas-card__header">Variavel alvo</header>
  <div class="ml-canvas-card__body"><p>Churn Value</p></div>
</section>

<section class="ml-canvas-card">
  <header class="ml-canvas-card__header">Metricas de sucesso</header>
  <div class="ml-canvas-card__body"><ul>
<li>AUC-ROC &gt;= 0.85</li>
<li>F1-Score &gt;= 0.80</li>
<li>Precision &gt;= 0.78</li>
</ul></div>
</section>

<section class="ml-canvas-card">
  <header class="ml-canvas-card__header">Fontes de dados</header>
  <div class="ml-canvas-card__body"><ul>
<li>Telco_customer_churn.xlsx</li>
<li>Outras fontes sobre análise de churn</li>
</ul></div>
</section>

<section class="ml-canvas-card">
  <header class="ml-canvas-card__header">Features candidatas</header>
  <div class="ml-canvas-card__body"><div class="ml-canvas-scroll"><ul>
<li>Count</li>
<li>Country</li>
<li>State</li>
<li>City</li>
<li>Zip Code</li>
<li>Lat Long</li>
<li>Latitude</li>
<li>Longitude</li>
<li>Gender</li>
<li>Senior Citizen</li>
<li>Partner</li>
<li>Dependents</li>
<li>Tenure Months</li>
<li>Phone Service</li>
<li>Multiple Lines</li>
<li>Internet Service</li>
<li>Online Security</li>
<li>Online Backup</li>
<li>Device Protection</li>
<li>Tech Support</li>
<li>Streaming TV</li>
<li>Streaming Movies</li>
<li>Contract</li>
<li>Paperless Billing</li>
<li>Payment Method</li>
<li>Monthly Charges</li>
<li>Total Charges</li>
<li>Churn Label</li>
<li>Churn Score</li>
<li>CLTV</li>
<li>Churn Reason</li>
</ul></div></div>
</section>

<section class="ml-canvas-card">
  <header class="ml-canvas-card__header">Restricoes</header>
  <div class="ml-canvas-card__body"><ul>
<li>Dados fictícios — sem possibilidade de coletar mais</li>
<li>Latência de predição &lt; 100ms</li>
</ul></div>
</section>

<section class="ml-canvas-card">
  <header class="ml-canvas-card__header">Riscos</header>
  <div class="ml-canvas-card__body"><ul>
<li>Viés de permanência do cliente nos dados</li>
<li>Desbalanceamento de classes (73.5% permanência vs 26.5% churn)</li>
</ul></div>
</section>

</div>
