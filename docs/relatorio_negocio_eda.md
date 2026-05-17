# RELATÓRIO EXECUTIVO DE NEGÓCIOS: ANÁLISE EXPLORATÓRIA DE DADOS (EDA)

**Para:** Documentação do Projeto de Predição de Churn

**Patrocinador do Projeto:** Diretor de Retenção e Experiência do Cliente (CSO)

**Status:** Validado e Aprovado para Fase de Modelagem

---

## 1. Visão Geral e Alinhamento Estratégico

Os achados da Análise Exploratória de Dados (EDA) confirmam que o churn da nossa base (**26,5%**) não é homogêneo. Ele está concentrado em gargalos operacionais e de produto muito específicos. Identificamos quatro alavancas críticas de negócio onde o modelo preditivo deverá atuar para alcançarmos a meta de redução de **20% a 25%** no volume de evasão nos próximos 12 meses.

## 2. Principais Diagnósticos de Negócio (Os Ralos de Receita)

### 2.1 **O Gargalo dos Primeiros Meses (Contrato Mensal):**
* *Achado:* O churn está massivamente concentrado entre o **0 e 5º mês de casa** de clientes com contratos *Month-to-month*.
* *Impacto:* Alto custo de aquisição (CAC) desperdiçado em clientes que não se pagam no tempo de vida ($LTV$).
* *Diretriz:* O modelo precisa disparar alertas precoces (no 2º mês) para ações de migração para planos anuais.


### 2.2 **A Crise de Retenção na Fibra Óptica:**
* *Achado:* Clientes do produto Fibra Óptica apresentam taxas de evasão significativamente maiores que os de tecnologia legada (DSL), apesar de ser um produto teoricamente superior.
* *Impacto:* Estamos perdendo os clientes que possuem o maior gasto mensal médio (*Monthly Charges*), gerando grande impacto no faturamento recorrente (MRR).
* *Diretriz:* Investigar a fundo a elasticidade de preço e a estabilidade do serviço nos primeiros meses deste cluster.


### 2.3 **Serviços de Valor Agregado (SVA) como Âncoras de Lealdade:**
* *Achado:* Clientes que **NÃO** possuem *TechSupport* (Suporte Técnico) e *OnlineSecurity* (Segurança Online) têm uma propensão drasticamente maior ao churn.
* *Impacto:* A ausência desses serviços reduz o custo de mudança do cliente, facilitando a ida para a concorrência por qualquer oscilação de preço.
* *Diretriz:* Mapear a ausência desses SVAs como fortes preditores de risco no modelo.


### 2.4 **O Atrito Financeiro do Boleto Eletrônico (*Electronic Check*):**
* *Achado:* O método de pagamento por boleto eletrônico está diretamente correlacionado a picos de churn quando comparado ao cartão de crédito ou débito automático.
* *Impacto:* O processo proativo de pagamento mensal gera um atrito psicológico de consumo desnecessário na base.


## 3. Requisitos de Negócio para o Input do Modelo (Features)

Para garantir a explicabilidade exigida pelo time de call center, as seguintes variáveis devem ser tratadas com alta prioridade no *feature engineering*:

1. **Tipo de Contrato** (foco em contratos mensais).
2. **Tipo de Serviço de Internet** (isolando o comportamento da Fibra Óptica).
3. **Presença de SVAs** (*TechSupport* e *OnlineSecurity* combinados ou isolados).
4. **Método de Pagamento** (identificando *Electronic Check*).
5. **Interação Preço x Tempo de Casa** (`MonthlyCharges` vs. `tenure`).

## 4. Conclusão e Próximos Passos

O mapeamento das dores está concluído. Do ponto de vista de negócios, o analista está autorizado a prosseguir para a **Fase de Modelagem Baseline**, mantendo os critérios de sucesso previamente combinados: foco inicial em **Recall ($\ge 0.80$)** para capturar a volumetria desses grupos de risco, e monitoramento da **Precision ($\ge 0.60$)** para controle de eficiência orçamentária dos incentivos.
