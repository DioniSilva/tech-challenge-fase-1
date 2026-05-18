# TELCO Customer Churn Prediction

Documentacao das definicoes do ML Canvas para o projeto de <b>churn prediction</b>.

> Data Readiness Score: 100%
>
> Projeto viavel: Sim

Para atualizar esta pagina, rode: `make docs-canvas`.

A predição de cancelamento de um serviço (também conhecida pelo termo em inglês "churn") é uma atividade comum em empresas de alta maturidade analítica. No caso de uso deste projeto, trata-se da prestação de serviço de uma empresa de telecomunicações (telecom); o modelo final será utilizado para identificar perfis com alto risco de saída, de modo que as áreas responsáveis pela manutenção do cliente (geralmente Customer Success, CS, ou Customer Relationship Management, CRM) possam fazer ações de retenção antes que a saída de fato aconteça.

Logo, em que pese tenhamos metas de desempenho técnico (relacionadas ao modelo), também é importante dar clareza à definição de sucesso para o negócio: pela análise da base de dados, descobrimos que o percentual de saída de clientes (i.e., clientes marcados com "Churn Value" = 1) é de aproximadamente 27% da quantidade total de clientes e 30% do valor mensal cobrado (coluna "Monthly Charges"). Pela descrição da base, ela representa todos os clientes da empresa da California ao fim do terceiro trimestre de um determinado ano; assim, uma estimativa de quanto vale este projeto poderia ser a seguinte.

<li><b>Valor total da fatura paga por clientes cancelados:</b> $ 139.130,00/mês</li>
<li><b>Benefício com redução de 10% de clientes cancelados:</b> $ 13.913,00/mês</li>
<li><b>Benefício monetário estimado em 12 meses:</b> 12 x $ 13.913,00 = $ 166.956,00</li>
<li><b>Receita total em 12 meses:</b> $ 12 x 456.116,60 = $ 5.473.399,20</li>
<li><b>Benefício percentual da receita estimado:</b> $ 166.956,00 ÷ $ 5.473.399,20 = 3%</li>

Para um projeto único, um aumento de 3 pontos percentuais na receita anual é bastante significativo, reforçando a viabilidade do mesmo. Importante notar ainda que a premissa adotada aqui foi um sucesso na redução do churn de apenas 10%.

Notemos, porém, que a mera identificação de clientes com maior potencial de cancelamento do serviço, por si só, não garante o sucesso do projeto: é necessário definir <i>quais</i> ações serão aplicadas a estes clientes de modo a <i>tentar</i> dissuadi-los de um futuro cancelamento. Para auxiliar as áreas de negócio nessas ações, a base de dados traz uma informação importante: o motivo do cancelamento pelos clientes que de fato cancelaram o serviço durante o período analisado.

<table>
  <thead>
    <tr>
      <th>Churn Reason</th>
      <th>Count</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Attitude of support person</td><td>192</td></tr>
    <tr><td>Competitor offered higher download speeds</td><td>189</td></tr>
    <tr><td>Competitor offered more data</td><td>162</td></tr>
    <tr><td>Don't know</td><td>154</td></tr>
    <tr><td>Competitor made better offer</td><td>140</td></tr>
    <tr><td>Attitude of service provider</td><td>135</td></tr>
    <tr><td>Competitor had better devices</td><td>130</td></tr>
    <tr><td>Network reliability</td><td>103</td></tr>
    <tr><td>Product dissatisfaction</td><td>102</td></tr>
    <tr><td>Price too high</td><td>98</td></tr>
    <tr><td>Service dissatisfaction</td><td>89</td></tr>
    <tr><td>Lack of self-service on Website</td><td>88</td></tr>
    <tr><td>Extra data charges</td><td>57</td></tr>
    <tr><td>Moved</td><td>53</td></tr>
    <tr><td>Lack of affordable download/upload speed</td><td>44</td></tr>
    <tr><td>Limited range of services</td><td>44</td></tr>
    <tr><td>Long distance charges</td><td>44</td></tr>
    <tr><td>Poor expertise of phone support</td><td>20</td></tr>
    <tr><td>Poor expertise of online support</td><td>19</td></tr>
    <tr><td>Deceased</td><td>6</td></tr>
  </tbody>
  <tfoot>
  <th></th><th></th>
    <tr>
      <td><b>Total</b></td>
      <td>1.869</td>
    </tr>
  </tfoot>
</table>

Notemos que das cinco principais razões para o cancelamento (que sozinhas representam mais de 44% do total), três estão relacionadas a uma maior percepção de valor dos competidores versus o serviço sendo oferecido naquele momento; destas, apenas uma parece ter relação com o valor sendo cobrado ("better offer"), enquanto as outras duas parecem ter relação com o produto sendo consumido ("higher download speed" e "more data"); por fim, o principal motivo de cancelamento está no relacionamento das equipes de suporte ao cliente -- motivo parecido aparece na sexta posição, desta vez direcionado ao prestador de serviço, provavelmente técnico de campos.

Assim, uma primeira recomendação para as áreas de negócio nas ações de retenção dos clientes com maior probabilidade de cancelamento, a serem identificados pelo modelo final, seria a seguinte.

<ol>
  <li>Reavaliar se os atuais produtos, principalmente de dados, está aderente à necessidade individual</li>
  <li>Reciclar processos existentes de atendimento ao cliente, sejam eles técnicos ou não</li>
  <li>Priorizar clientes com maior margem de lucro, se necessário</li>
  <li>Revisar o valor sendo cobrado para determinados clientes ou cidades</li>
</ol>

Estas ações deveriam ser um primeiro bom conjunto de iniciativa de retenção de clientes, e que devem ser revisitadas no futuro quando o mais percepções serão retiradas do modelo final.

<div class="ml-canvas-grid">

<section class="ml-canvas-card">
  <header class="ml-canvas-card__header">Problema de negocio</header>
  <div class="ml-canvas-card__body"><p>Reduzir o churn através da identificação de clientes com perfis de alto risco de saída.</p><p></p></div>
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
