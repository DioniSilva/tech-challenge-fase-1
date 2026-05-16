# TELCO Customer Churn Prediction

Documentacao das definicoes do ML Canvas para o projeto de churn prediction.

> Data Readiness Score: 80%
>
> Projeto viavel: Sim



Para atualizar esta pagina, rode: `make docs-canvas`

<div class="ml-canvas-grid">

<section class="ml-canvas-card">
  <header class="ml-canvas-card__header">Problema de negocio</header>
  <div class="ml-canvas-card__body"><p>Com base nos dados apresentados, a taxa de churn histórica está girando em torno de 26,5%.No mercado de Telecom, isso é considerado um churn alto (o ideal para grandes operadoras de telefonia e internet fixa costuma orbitar abaixo de 1.5% a 2% ao mês, o que daria algo entre 18% e 24% ao ano).O nosso alvo é trazer essa taxa de 26,5% para a faixa dos 20% a 21% no acumulado.Para isso precisamos de um modelo que identifique, com alta precisão, os top 10% ou 20% de clientes com maior risco de evasão.Se conseguirmos agir preventivamente apenas nesse grupo mais crítico disparando uma oferta de retenção ou um upgrade de serviço, já batemos a nossa meta.</p></div>
</section>

<section class="ml-canvas-card">
  <header class="ml-canvas-card__header">Tarefa ML</header>
  <div class="ml-canvas-card__body"><p>Prototipação de um modelo de ML baseline e posterior evolução para Rede Neural para classificação binária (Churn: 0/1)</p></div>
</section>

<section class="ml-canvas-card">
  <header class="ml-canvas-card__header">Variavel alvo</header>
  <div class="ml-canvas-card__body"><p>Churn Value</p></div>
</section>

<section class="ml-canvas-card">
  <header class="ml-canvas-card__header">Metricas de sucesso</header>
  <div class="ml-canvas-card__body"><ul>
<li>Redução do churn de 26,5% para 20-21% no acumulado nos próximos 12 meses</li>
<li>Recall &gt;= 0.80</li>
<li>Precision &gt;= 0.60</li>
</ul></div>
</section>

<section class="ml-canvas-card">
  <header class="ml-canvas-card__header">Fontes de dados</header>
  <div class="ml-canvas-card__body"><ul>
<li>Telco_customer_churn.xlsx</li>
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
<li>Ranquamento por Risco: O modelo deve entregar a probabilidade de churn (0% a 100%) e não apenas &#x27;Sim/Não&#x27;, permitindo que o time de atendimento priorize os clientes mais críticos.</li>
<li>Explicabilidade (White Box): Precisamos saber por que o cliente está em risco (ex: variáveis mais importantes) para direcionar o argumento de retenção do atendente.</li>
<li>Valor do Cliente (Margem): A estratégia futura deve diferenciar clientes de alto valor (Fibra/Combos) de clientes de baixa margem (DSL básico).</li>
</ul></div>
</section>

<section class="ml-canvas-card">
  <header class="ml-canvas-card__header">Riscos</header>
  <div class="ml-canvas-card__body"><ul>
<li>Viés de permanência do cliente nos dados</li>
<li>Desbalanceamento de classes (73.5% permanência vs 26.5% churn)</li>
<li>Mudanças no comportamento do cliente ao longo do tempo</li>
<li>Dados Faltantes ou Inconsistentes</li>
<li>Privacidade e LGPD: Garantir que o uso dos dados esteja em conformidade com as regulamentações de privacidade, evitando o uso de informações sensíveis ou identificáveis sem consentimento adequado.</li>
<li>Fadiga do Cliente: Ligar excessivamente para clientes que o modelo apontou como risco (mas que na verdade estavam satisfeitos) pode gerar o efeito inverso: lembrar o cliente de que ele gasta muito e incentivá-lo a pesquisar a concorrência.</li>
<li>Viés de Seleção: O dataset é uma foto histórica. Se focarmos apenas em quem já saiu, podemos ignorar padrões de clientes que estão insatisfeitos hoje, mas que têm amarras contratuais diferentes dos clientes do passado.</li>
<li>Custo de Retenção Ineficiente: Gastar mais dinheiro para reter um cliente (com bônus, upgrades grátis e infraestrutura) do que o valor real que ele trará de retorno financeiro para a empresa no tempo de vida restante dele.</li>
</ul></div>
</section>

</div>
