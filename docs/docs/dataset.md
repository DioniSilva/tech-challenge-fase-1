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

| Variável | Descrição |
|---|---|
| `CustomerID` | Identificador único do cliente |
| `Count` | Valor utilizado para contagem em relatórios e dashboards |

### 2. Informações geográficas

| Variável | Descrição |
|---|---|
| `Country` | País de residência principal do cliente |
| `State` | Estado de residência principal |
| `City` | Cidade de residência principal |
| `Zip Code` | CEP do cliente |
| `Lat Long` | Latitude e longitude combinadas |
| `Latitude` | Latitude da residência |
| `Longitude` | Longitude da residência |

### 3. Perfil demográfico

| Variável | Descrição | Valores |
|---|---|---|
| `Gender` | Gênero do cliente | Male, Female |
| `Senior Citizen` | Cliente possui 65 anos ou mais | Yes, No |
| `Partner` | Cliente possui parceiro(a) | Yes, No |
| `Dependents` | Cliente possui dependentes | Yes, No |

### 4. Relacionamento com a empresa

| Variável | Descrição |
|---|---|
| `Tenure Months` | Quantidade total de meses que o cliente permaneceu na empresa |

### 5. Serviços de telefonia

| Variável | Descrição | Valores |
|---|---|---|
| `Phone Service` | Cliente possui serviço telefônico residencial | Yes, No |
| `Multiple Lines` | Cliente possui múltiplas linhas telefônicas | Yes, No |

### 6. Serviços de internet

| Variável | Descrição | Valores |
|---|---|---|
| `Internet Service` | Tipo de serviço de internet contratado | No, DSL, Fiber Optic, Cable |
| `Online Security` | Serviço adicional de segurança online | Yes, No |
| `Online Backup` | Serviço adicional de backup online | Yes, No |
| `Device Protection` | Plano de proteção de dispositivos | Yes, No |
| `Tech Support` | Plano adicional de suporte técnico | Yes, No |
| `Streaming TV` | Uso do serviço para streaming de TV | Yes, No |
| `Streaming Movies` | Uso do serviço para streaming de filmes | Yes, No |

### 7. Contrato e pagamento

| Variável | Descrição | Valores |
|---|---|---|
| `Contract` | Tipo de contrato atual | Month-to-Month, One Year, Two Year |
| `Paperless Billing` | Cliente utiliza cobrança digital | Yes, No |
| `Payment Method` | Método de pagamento da fatura | Bank Withdrawal, Credit Card, Mailed Check |

### 8. Informações financeiras

| Variável | Descrição |
|---|---|
| `Monthly Charge` | Valor mensal atual pago pelo cliente |
| `Total Charges` | Valor total pago até o final do período analisado |

## Variáveis relacionadas ao churn

### 9. Indicadores de churn

| Variável | Descrição |
|---|---|
| `Churn Label` | Indica se o cliente deixou a empresa no trimestre |
| `Churn Value` | Representação numérica do churn (1 = saiu, 0 = permaneceu) |

### 10. Métricas preditivas

| Variável | Descrição |
|---|---|
| `Churn Score` | Score de propensão ao churn (0–100) gerado pelo IBM SPSS Modeler |
| `CLTV` | Customer Lifetime Value estimado do cliente |

### 11. Motivo do cancelamento

| Variável | Descrição |
|---|---|
| `Churn Reason` | Motivo específico pelo qual o cliente deixou a empresa |

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
- `Monthly Charge`
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
| `Churn Label` | Categórica | Predição de churn |
| `Churn Value` | Binária | Modelagem supervisionada |
