# Telco customer churn: IBM dataset

Esta página descreve o dataset utilizado no projeto (visão geral e dicionário de dados).

## Fonte

- Kaggle: [Telco Customer Churn (IBM)](https://www.kaggle.com/datasets/yeanzc/telco-customer-churn-ibm-dataset/data?select=Telco_customer_churn.xlsx)

## Visão geral

- 7043 observações (clientes)
- 33 variáveis
- Tema: características demográficas, localização, serviços contratados, faturamento e churn

## Nomenclatura

Os nomes abaixo seguem as colunas do arquivo, incluindo espaços (ex.: `Zip Code`, `Tenure Months`).

## Dicionário de dados

### 1. Identificação do cliente

| Variável | Tipo | Descrição |
|---|---|---|
| `CustomerID` | `object` | Identificador único do cliente |
| `Count` | `int64` | Valor utilizado para contagem em relatórios e dashboards |

### 2. Informações geográficas

| Variável | Tipo | Descrição |
|---|---|---|
| `Country` | `object` | País de residência principal do cliente |
| `State` | `object` | Estado de residência principal |
| `City` | `object` | Cidade de residência principal |
| `Zip Code` | `int64` | CEP do cliente |
| `Lat Long` | `object` | Latitude e longitude combinadas |
| `Latitude` | `float64` | Latitude da residência |
| `Longitude` | `float64` | Longitude da residência |

### 3. Perfil demográfico

| Variável | Tipo | Descrição | Valores |
|---|---|---|---|
| `Gender` | `object` | Gênero do cliente | Male, Female |
| `Senior Citizen` | `object` | Cliente possui 65 anos ou mais | Yes, No |
| `Partner` | `object` | Cliente possui parceiro(a) | Yes, No |
| `Dependents` | `object` | Cliente possui dependentes | Yes, No |

### 4. Relacionamento com a empresa

| Variável | Tipo | Descrição |
|---|---|---|
| `Tenure Months` | `int64` | Quantidade total de meses que o cliente permaneceu na empresa |

### 5. Serviços de telefonia

| Variável | Tipo | Descrição | Valores |
|---|---|---|---|
| `Phone Service` | `object` | Cliente possui serviço telefônico residencial | Yes, No |
| `Multiple Lines` | `object` | Cliente possui múltiplas linhas telefônicas | Yes, No |

### 6. Serviços de internet

| Variável | Tipo | Descrição | Valores |
|---|---|---|---|
| `Internet Service` | `object` | Tipo de serviço de internet contratado | No, DSL, Fiber Optic, Cable |
| `Online Security` | `object` | Serviço adicional de segurança online | Yes, No |
| `Online Backup` | `object` | Serviço adicional de backup online | Yes, No |
| `Device Protection` | `object` | Plano de proteção de dispositivos | Yes, No |
| `Tech Support` | `object` | Plano adicional de suporte técnico | Yes, No |
| `Streaming TV` | `object` | Uso do serviço para streaming de TV | Yes, No |
| `Streaming Movies` | `object` | Uso do serviço para streaming de filmes | Yes, No |

### 7. Contrato e pagamento

| Variável | Tipo | Descrição | Valores |
|---|---|---|---|
| `Contract` | `object` | Tipo de contrato atual | Month-to-Month, One Year, Two Year |
| `Paperless Billing` | `object` | Cliente utiliza cobrança digital | Yes, No |
| `Payment Method` | `object` | Método de pagamento da fatura | Bank Withdrawal, Credit Card, Mailed Check |

### 8. Informações financeiras

| Variável | Tipo | Descrição |
|---|---|---|
| `Monthly Charges` | `float64` | Valor mensal atual pago pelo cliente |
| `Total Charges` | `object` | Valor total pago até o final do período analisado |

## Variáveis relacionadas ao churn

### 9. Indicadores de churn

| Variável | Tipo | Descrição |
|---|---|---|
| `Churn Label` | `object` | Indica se o cliente deixou a empresa no trimestre |
| `Churn Value` | `int64` | Representação numérica do churn (1 = saiu, 0 = permaneceu) |

### 10. Métricas preditivas

| Variável | Tipo | Descrição |
|---|---|---|
| `Churn Score` | `int64` | Score de propensão ao churn (0–100) gerado pelo IBM SPSS Modeler |
| `CLTV` | `int64` | Customer Lifetime Value estimado do cliente |

### 11. Motivo do cancelamento

| Variável | Tipo | Descrição |
|---|---|---|
| `Churn Reason` | `object` | Motivo específico pelo qual o cliente deixou a empresa |

## Possíveis categorizações para análise

### Variáveis categóricas

- `Gender`
- `Senior Citizen`
- `Partner`
- `Dependents`
- `Phone Service`
- `Multiple Lines`
- `Internet Service`
- `Online Security`
- `Online Backup`
- `Device Protection`
- `Tech Support`
- `Streaming TV`
- `Streaming Movies`
- `Contract`
- `Paperless Billing`
- `Payment Method`
- `Churn Label`
- `Churn Reason`

### Variáveis numéricas

- `Tenure Months`
- `Monthly Charges`
- `Total Charges`
- `Churn Score`
- `CLTV`
- `Latitude`
- `Longitude`

### Variáveis geográficas

- `Country`
- `State`
- `City`
- `Zip Code`
- `Latitude`
- `Longitude`
- `Lat Long`

## Objetivo potencial do dataset

Este dataset é altamente adequado para:

- Predição de churn de clientes
- Segmentação de clientes
- Análise de retenção
- Modelos de Customer Lifetime Value (CLTV)
- Análise geográfica de cancelamentos
- Sistemas de recomendação de retenção
- Análise de impacto de serviços adicionais na permanência do cliente
- Modelos supervisionados de classificação
- EDA (Exploratory Data Analysis)
- Dashboards de BI e métricas de negócio

## Variável alvo (target)

| Variável | Tipo | Objetivo |
|---|---|---|
| `Churn Label` | `object` | Predição de churn |
| `Churn Value` | `int64` | Modelagem supervisionada |
