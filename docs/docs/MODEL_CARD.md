---
{}
---

# Modelo de Previsão de Churn (Tech Challenge - Fase 1)

## Sumário

Este Model Card documenta o modelo preditivo de cancelamento de clientes (Churn). O modelo utiliza uma abordagem de classificação binária com regressão logística, balanceada para lidar com o desbalanceamento de classes presente nos dados históricos.

---

## 1. Detalhes do Modelo

| Atributo | Valor |
|----------|-------|
| **Nome** | Baseline Churn Prediction Model |
| **Tipo** | Classificação Binária |
| **Algoritmo** | Regressão Logística |
| **Framework** | scikit-learn |
| **Versão do Modelo** | 1.0.0 |
| **Data de Criação** | Maio 2026 |
| **Licença** | MIT |
| **Responsável** | Equipe de MLEks - Tech Challenge |

---

## 2. Uso Pretendido

### Casos de Uso Recomendados
- Identificação de clientes em risco de cancelamento para ações proativas de retenção
- Segmentação de clientes por probabilidade de churn
- Análise de padrões e fatores de risco associados ao cancelamento
- Suporte a decisões estratégicas de retenção e pricing

### Fora de Escopo
- O modelo não deve ser usado de forma autônoma sem supervisão humana
- Não recomendado para decisões disciplinares ou penalizações
- Requer reavaliação periódica em cenários de mudanças de mercado

---

## 3. Dados de Treinamento e Validação

### Características do Dataset
- **Fonte Principal**: [Telco customer churn: IBM dataset](https://www.kaggle.com/datasets/yeanzc/telco-customer-churn-ibm-dataset)
- **Tamanho Original**: 7.043 registros
- **Período de Cobertura**: Dados históricos de clientes de telecomunicações
- **Divisão**: 80% Treino / 20% Teste

### Features Utilizadas
- **Dados Demográficos**: Idade, Gênero, Parceria, Dependentes
- **Dados de Contrato**: Tipo de Contrato, Duração da Relação (tenure)
- **Dados de Serviço**: Internet, Telefonia, Segurança Online, Backup, etc.
- **Dados Financeiros**: Cobrança Mensal, Gasto Médio Mensal, Método de Pagamento

### Atributos Sensíveis Mapeados
- **Gênero (Masculino/Feminino)** - Utilizado exclusivamente para auditoria pós-treino
- **Senior Citizen** - Monitorado para vieses etários

---

## 4. Análise de Performance

### Métricas Agregadas
| Métrica | Valor |
|---------|-------|
| **Acurácia (Treino)** | 0.7419 |
| **Acurácia (Teste)** | 0.7466 |
| **Precisão** | 0.5354 |
| **Recall (Sensibilidade)** | 0.8125 |
| **F1-Score** | 0.6455 |
| **ROC-AUC** | 0.8463 |

### Interpretação
- **Precisão 53.54%**: Do total de predições positivas (churn), ~54% estão corretas
- **Recall 81.25%**: O modelo identifica ~81% dos clientes que realmente vão fazer churn
- **F1-Score 0.6455**: Balanço entre precisão e recall
- **ROC-AUC 0.8463**: Capacidade discriminativa do modelo

---

## 5. Análise de Equidade (Fairness)

### Métricas Desagregadas por Gênero

| sensitive_feature_0   |   Acurácia |   Precisão |   Taxa de Seleção (Churn) |   Taxa de Falsos Positivos |
|:----------------------|-----------:|-----------:|--------------------------:|---------------------------:|
| Female                |     0.7458 |     0.5455 |                    0.4455 |                     0.2871 |
| Male                  |     0.7475 |     0.5243 |                    0.4156 |                     0.2718 |

### Avaliação de Disparidade
| Métrica de Disparidade | Valor | Interpretação |
|------------------------|-------|----------------|
| Disparidade de Acurácia | 0.0017 | Diferença máxima de acurácia entre grupos |
| Disparidade de Precisão | 0.0211 | Diferença máxima de precisão entre grupos |
| Disparidade de Taxa de Seleção | 0.0299 | Diferença na proporção de previsões positivas |

### Conclusões sobre Equidade
✓ **Status**: Modelo demonstra equidade razoável entre grupos demográficos
- Disparidades detectadas estão dentro de limites aceitáveis (<0.10)
- Não há viés sistemático evidente contra nenhum grupo
- Recomenda-se monitoramento contínuo durante operacionalização

---

## 6. Considerações Éticas e Limitações

### Potenciais Vieses
1. **Viés de Dados Históricos**: O modelo herda padrões dos dados históricos
2. **Desbalanceamento de Classes**: ~26% de churn vs 74% de retenção
3. **Mudanças de Mercado**: Performance pode degradar com mudanças econômicas

### Estratégias de Mitigação
- ✓ Uso de `class_weight='balanced'` para compensar desbalanceamento
- ✓ Auditoria periódica com Fairlearn
- ✓ Monitoramento de drift em produção
- ✓ Reavaliação a cada 3 meses com dados novos

### Recomendações
- Combinar com julgamento humano antes de tomar decisões
- Investigar razões por trás de previsões de alto risco
- Manter registro de feedback de especialistas em negócio
- Estabelecer limites de confiança (thresholds) para ação

---

## 7. Como Usar o Modelo em Produção

```python
import joblib
import pandas as pd

# Carregar modelo
model = joblib.load("baseline_model.joblib")

# Preparar dados novos (mesma estrutura do treinamento)
# X_novo deve ter mesmas features do treinamento
y_pred = model.predict(X_novo)
y_prob = model.predict_proba(X_novo)[:, 1]

# y_pred: 0 (sem churn) ou 1 (com churn)
# y_prob: probabilidade de churn [0-1]
```

---

## 8. Versionamento e Histórico

| Versão | Data | Principais Mudanças |
|--------|------|---------------------|
| 1.0.0 | Maio 2026 | Release inicial com Logistic Regression |

---

## 9. Contato e Suporte

- **Equipe Responsável**: MLEks - Tech Challenge
- **Para Dúvidas**: Consultar documentação no repositório
- **Avisos de Retraining**: Monitorar performance mensal