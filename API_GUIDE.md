# API Telco Churn Prediction

Documentação completa da API FastAPI para predição de churn.

## Estrutura do Projeto

```
tech-challenge-fase-1/
├── src/
│   ├── api/                      # Camada de Entrada (Rotas)
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── predict.py   # Endpoints de predição e health
│   │   │   └── api.py           # Agregador de roteadores v1
│   │   └── __init__.py
│   ├── core/                     # Configurações Globais
│   │   ├── config.py            # Variáveis de ambiente (Pydantic Settings)
│   │   └── __init__.py
│   ├── schemas/                  # DTOs (Pydantic)
│   │   ├── customer.py          # Schemas: CustomerInput, PredictionResponse
│   │   └── __init__.py
│   ├── services/                 # Regras de Negócio
│   │   ├── predict_service.py   # Lógica de predição
│   │   └── __init__.py
│   ├── api_main.py              # Aplicação FastAPI principal
│   └── __init__.py
└── tests/
    └── test_api.py              # Testes da API
```

## Arquitetura de Camadas

### 1. **API Layer** (`src/api/`)
- Responsável por receber e responder requisições HTTP
- Define endpoints (`/health`, `/predict`)
- Usa APIRouter para modularização
- Realiza validação básica de requisições

### 2. **Core Layer** (`src/core/`)
- Configurações globais da aplicação
- Pydantic Settings para variáveis de ambiente
- Definições de paths, versão, log level

### 3. **Schema Layer** (`src/schemas/`)
- DTOs (Data Transfer Objects) com Pydantic
- Validação automática de entrada/saída
- Documentação de campos no OpenAPI

### 4. **Service Layer** (`src/services/`)
- Regras de negócio
- Carregamento e gerenciamento do modelo
- Preparação de dados
- Execução de predições
- Implementa Singleton para carregar modelo uma única vez

## Injeção de Dependências

A API utiliza massivamente o sistema de `Depends` do FastAPI:

```python
@router.post("/predict")
def predict(
    customer: CustomerInput,
    predict_service: PredictService = Depends(get_predict_service),
) -> PredictionResponse:
    # predict_service é injetado automaticamente
    return predict_service.predict(customer)
```

## Como Rodar a API

### 1. Instalar Dependências

```bash
pip install -e .
# ou
pip install -r requirements.txt
```

### 2. Iniciar o Servidor

```bash
# Opção 1: Diretamente com Uvicorn
uvicorn src.api_main:app --host 0.0.0.0 --port 8000 --reload

# Opção 2: Com Python
python src/api_main.py

# Opção 3: Via Makefile (se configurado)
make api-run
```

### 3. Acessar a API

- **Documentação Interativa (Swagger)**: http://localhost:8000/docs
- **Documentação Alternativa (ReDoc)**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000/

## Endpoints

### 1. Health Check

**Endpoint**: `GET /api/v1/health`

**Descrição**: Verifica o status da aplicação e disponibilidade do modelo

**Response** (200 OK):
```json
{
  "status": "healthy",
  "message": "API is running correctly and model is loaded",
  "version": "1.0.0"
}
```

**Possíveis Respostas**:
- `200 OK`: API está saudável
- `503 SERVICE_UNAVAILABLE`: Modelo não carregado

---

### 2. Predict Churn

**Endpoint**: `POST /api/v1/predict`

**Descrição**: Executa predição de churn para um cliente

**Request Body** (CustomerInput):
```json
{
  "customer_id": "5575-GNVDE",
  "count": 1,
  "country": "United States",
  "state": "California",
  "city": "Los Angeles",
  "zip_code": 90001,
  "latitude": 34.09,
  "longitude": -118.26,
  "gender": "Male",
  "senior_citizen": "Yes",
  "partner": "Yes",
  "dependents": "Yes",
  "tenure_months": 48,
  "phone_service": "Yes",
  "multiple_lines": "Yes",
  "internet_service": "Fiber optic",
  "online_security": "No",
  "online_backup": "No",
  "device_protection": "No",
  "tech_support": "No",
  "streaming_tv": "Yes",
  "streaming_movies": "Yes",
  "contract": "One year",
  "paperless_billing": "No",
  "payment_method": "Credit card (automatic)",
  "monthly_charges": 105.25,
  "total_charges": "5046.00"
}
```

**Response** (200 OK):
```json
{
  "customer_id": "5575-GNVDE",
  "prediction": 0,
  "prediction_label": "No",
  "prediction_probability": 0.25,
  "confidence": 0.75
}
```

**Possíveis Respostas**:
- `200 OK`: Predição realizada com sucesso
- `400 BAD_REQUEST`: Dados de entrada inválidos
- `503 SERVICE_UNAVAILABLE`: Modelo não disponível
- `500 INTERNAL_SERVER_ERROR`: Erro na execução da predição

---

## Exemplos de Uso

### Com cURL

```bash
# Health Check
curl -X GET "http://localhost:8000/api/v1/health"

# Predict
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "5575-GNVDE",
    "count": 1,
    "country": "United States",
    "state": "California",
    "city": "Los Angeles",
    "zip_code": 90001,
    "latitude": 34.09,
    "longitude": -118.26,
    "gender": "Male",
    "senior_citizen": "Yes",
    "partner": "Yes",
    "dependents": "Yes",
    "tenure_months": 48,
    "phone_service": "Yes",
    "multiple_lines": "Yes",
    "internet_service": "Fiber optic",
    "online_security": "No",
    "online_backup": "No",
    "device_protection": "No",
    "tech_support": "No",
    "streaming_tv": "Yes",
    "streaming_movies": "Yes",
    "contract": "One year",
    "paperless_billing": "No",
    "payment_method": "Credit card (automatic)",
    "monthly_charges": 105.25,
    "total_charges": "5046.00"
  }'
```

### Com Python (requests)

```python
import requests

# Health Check
response = requests.get("http://localhost:8000/api/v1/health")
print(response.json())

# Predict
customer = {
    "customer_id": "5575-GNVDE",
    "count": 1,
    # ... outros dados
}

response = requests.post(
    "http://localhost:8000/api/v1/predict",
    json=customer
)
print(response.json())
```

### Com JavaScript/Fetch

```javascript
// Health Check
fetch('http://localhost:8000/api/v1/health')
  .then(response => response.json())
  .then(data => console.log(data));

// Predict
const customer = {
  customer_id: "5575-GNVDE",
  count: 1,
  // ... outros dados
};

fetch('http://localhost:8000/api/v1/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(customer)
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Modelos Pydantic

### CustomerInput

Schema de entrada para predição. Contém todas as 33 features do dataset IBM Telco.

**Campos principais**:
- `customer_id` (str): ID único do cliente
- `gender` (str): Gênero (Male/Female)
- `senior_citizen` (str): É senior (Yes/No)
- `partner` (str): Tem parceiro (Yes/No)
- `dependents` (str): Tem dependentes (Yes/No)
- `tenure_months` (int): Meses de permanência
- `internet_service` (str): Tipo de internet (DSL/Fiber optic/No)
- `contract` (str): Tipo de contrato (Month-to-month/One year/Two year)
- `monthly_charges` (float): Cobrança mensal
- `total_charges` (str): Cobrança total

E muitos outros campos referentes aos serviços contratados.

### PredictionResponse

Schema de saída da predição.

**Campos**:
- `customer_id` (str): ID do cliente
- `prediction` (int): Predição (0=Não churn, 1=Churn)
- `prediction_label` (str): Label da predição (Yes/No)
- `prediction_probability` (float): Probabilidade de churn (0.0 a 1.0)
- `confidence` (float): Confiança da predição (0.0 a 1.0)

## Validação de Dados

A API utiliza Pydantic para validação automática de todos os dados de entrada. Se dados inválidos forem enviados, a API retornará um `400 BAD_REQUEST` com detalhes do erro:

```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["body", "tenure_months"],
      "msg": "Input should be a valid integer",
      "input": "invalid"
    }
  ]
}
```

## Logging

A API registra todas as operações importantes:
- Inicialização da aplicação
- Carregamento do modelo
- Requisições de predição
- Erros e exceções

Os logs estão configurados em `src/utils/app_logging.py` e podem ser consultados no console ou em arquivo de log.

## Tratamento de Erros

| Status Code | Descrição | Exemplo |
|------------|-----------|---------|
| 200 | Sucesso | Predição realizada |
| 400 | Requisição inválida | Dados não conformes ao schema |
| 500 | Erro interno | Erro na execução da predição |
| 503 | Serviço indisponível | Modelo não carregado |

## Variáveis de Ambiente

Configure as variáveis no arquivo `.env`:

```env
# Aplicação
APP_NAME=Telco Churn Prediction API
DEBUG=false
LOG_LEVEL=INFO

# Modelo
MODEL_NAME=mlp.joblib
```

## Desenvolvimento

### Adicionar Novo Endpoint

1. Criar função no `src/api/v1/endpoints/`
2. Definir schemas em `src/schemas/`
3. Implementar lógica em `src/services/`
4. Adicionar rota ao roteador
5. Incluir roteador em `src/api/v1/api.py`

### Executar Testes

```bash
# Teste de API
python tests/test_api.py

# Teste com pytest
pytest tests/test_api.py -v
```

## Performance e Otimizações

- **Modelo em cache**: O pipeline é carregado uma única vez na inicialização
- **Injeção de dependências**: Reutiliza instâncias de serviços
- **Validação automática**: Pydantic valida em tempo de parsing
- **Async ready**: Estrutura pronta para endpoints assíncronos

## Segurança

Para produção, considere:

1. **CORS**: Configurar origens permitidas
2. **HTTPS**: Usar SSL/TLS
3. **Autenticação**: Adicionar JWT ou API Key
4. **Rate Limiting**: Limitar requisições por IP/usuário
5. **Input Validation**: Já implementado com Pydantic
6. **Secrets**: Usar variáveis de ambiente para senhas/chaves

Exemplo de CORS mais restritivo:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://seu-frontend.com"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)
```

## Troubleshooting

### Modelo não encontrado

**Erro**: `FileNotFoundError: Modelo não encontrado`

**Solução**: Verifique se o arquivo `mlp.joblib` existe em `models/`

### Erro de Importação

**Erro**: `ModuleNotFoundError: No module named 'pydantic_settings'`

**Solução**: Instale as dependências com `pip install -e .`

### Porta em uso

**Erro**: `OSError: [Errno 48] Address already in use`

**Solução**: Use outra porta: `uvicorn src.api_main:app --port 8001`

## Suporte

Para dúvidas ou problemas, consulte a documentação interativa em `/docs` ou abra uma issue no repositório.
