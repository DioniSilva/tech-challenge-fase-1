---
{}
---

# Modelo de Previsão de Churn (Tech Challenge - Fase 1)

## Sumário

Este `modelcard` documenta o modelo preditivo de cancelamento de clientes (churn) finalista. O modelo utiliza uma abordagem de redes neurais lidando com o desbalanceamento de classes presente nos dados históricos.

---

## 1. Detalhes do Modelo

| Atributo | Valor |
|----------|-------|
| **Nome** |  MLP (PyTorch) |
| **Tipo** | Classificação binária |
| **Algoritmo** | Redes Neurais |
| **Framework** | PyTorch |
| **Versão do Modelo** | 1.0.5 |
| **Data de Criação** | Junho de 2026 |
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
- **Período de Cobertura**: dados históricos de clientes de telecomunicações
- **Divisão**: 80% treino / 20% teste

### Atributos Utilizados
- **Dados Demográficos**: gênero, localidade, indicador se idade é acima de 65 anos, indicador se estado civil é casado, indicador se moradia possui dependentes
- **Dados Contratuais**: duração da relação, indicador se conta digital, forma de pagamento, valor mensal cobrado, valor trimestral cobrado, carência
- **Dados de Serviço**: indicador se telefone fixo, indicador se telefone móvel, indicador se internet fixa, indicadores de proteção, indicadores de streaming

### Atributos Sensíveis Mapeados
- **Gênero (masculino/feminino)**: utilizado para verificação de viés pós-treino
- **Terceira idade**: idem

---

## 4. Análise de Performance

### Métricas Agregadas
| Métrica | Valor |
|---------|-------|
| **Acurácia (treino)** | 0.6998 |
| **Precisão** | 0.4594 |
| **Sensibilidade** | 0.8986 |
| **F1-Score** | 0.6080 |
| **ROC-AUC** | 0.8597 |

### Interpretações de Performance
Pela natureza do problema, entendemos que as métricas mais importantes são sensibilidade e precisão.

- **Sensibilidade**: dentre todas as classificações da classe positiva (churn) reais, quantas estão identificadas. Neste modelo, aproximadamente 90% das observações são identificadas.
- **Precisão**: dentre todas as classificações da classe positiva (churn) esperadas, quantas estão corretas. Neste modelo, aproximadamente 46% das previsões são corretas.

Tais métricas são importantes por dois motivos principais: (1) queremos direcionar ações de retenção aos clientes que de fato irão cancelar o serviço (sensibilidade); e (2) queremos que tais ações sejam eficientes economicamente (precisão). A primeira mantém a base ativa, enquanto a segunda mantém o custo controlado.

---

## 5. Análise de Equidade (Fairness)

### Métricas Desagregadas por Gênero

| sensitive_feature_0   |   Acurácia |   Precisão |   Seleção |
|:----------------------|-----------:|-----------:|----------:|
| Feminino                |     0.6798 |     0.4185 |     0.9198 |
| Masculino                  |     0.7475 |     0.5243 |     0.8818 |
| Não-idoso                |     0.6594 |     0.5542 |     0.9583 |
| Idoso                  |     0.7076 |     0.4307 |     0.8773 |


### Avaliação de Disparidade: gênero
| Métrica de Disparidade | Valor | Interpretação |
|------------------------|-------|----------------|
| Disparidade de Acurácia | 0.0677 | Diferença máxima de acurácia entre grupos |
| Disparidade de Precisão | 0.1058 | Diferença máxima de precisão entre grupos |
| Disparidade de Taxa de Seleção | 0.0380 | Diferença na proporção de previsões positivas |

### Avaliação de Disparidade: terceira idade
| Métrica de Disparidade | Valor | Interpretação |
|------------------------|-------|----------------|
| Disparidade de Acurácia | 0.0482 | Diferença máxima de acurácia entre grupos |
| Disparidade de Precisão | 0.1235 | Diferença máxima de precisão entre grupos |
| Disparidade de Taxa de Seleção | 0.0810 | Diferença na proporção de previsões positivas |

### Conclusões sobre Equidade
Modelo demonstra equidade no limite do razoável, demonstrando alguma tendência entre grupos demográficos (tanto gênero quanto terceira idade).
- Disparidades detectadas estão dentro de limites aceitáveis (<0.10), exceto Precisão para terceira idade
- Observa-se algum viés para grupos e métricas, mas sem uma direção óbvia (às vezes maior, às vezes menor)
- Recomenda-se monitoramento contínuo em produção e um maior entendimento das causas raízes de negócio

---

## 6. Considerações Éticas e Limitações

### Potenciais Vieses
1. **Viés de Dados Históricos**: O modelo herda padrões dos dados históricos
2. **Desbalanceamento de Classes**: ~26% de churn vs 74% de retenção
3. **Mudanças de Mercado**: Performance pode degradar com mudanças econômicas

### Estratégias de Mitigação
- Uso de `class_weight='balanced'` para compensar desbalanceamento
- Auditoria periódica com Fairlearn
- Monitoramento de drift em produção
- Reavaliação a cada 3 meses com dados novos

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
model = joblib.load("models/mlp.joblib")

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
| 1.0.1 | Maio de 2026 | Release inicial com técnica de regressão logística (baseline) |
| 1.0.2 | Maio de 2026 | Nova release com técnica de árvore de decisão |
| 1.0.3 | Junho de 2026 | Nova release com técnica de random forest |
| 1.0.4 | Junho de 2026 | Nova release com técnica de gradient boosting |
| 1.0.5 | Junho de 2026 | Release final com técnica de rede neural |

---

## 9. Contato e Suporte

- **Equipe responsável**: MLEks - Tech Challenge
- **Repositório**: https://github.com/DioniSilva/tech-challenge-fase-1
- **Em caso de dúvidas**: consultar a documentação no repositório
- **Avisos de retreino**: recomenda-se monitorar performance mensalmente
