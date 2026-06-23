# 🚀 Instalação e Uso da API Telco Churn Prediction

## 📋 Resumo do que foi criado

Uma **arquitetura completa de API em FastAPI** com separação de responsabilidades em camadas, injeção de dependências massiva, e validação com Pydantic.

### Estrutura de Arquivos Criados

```
src/
├── api/                           # Camada de Entrada (Rotas)
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── predict.py         # ✨ Endpoints: /health, /predict
│   │   │   └── __init__.py
│   │   ├── api.py                 # ✨ Agregador de roteadores v1
│   │   └── __init__.py
│   └── __init__.py
│
├── core/                          # Configurações Globais
│   ├── config.py                  # ✨ Pydantic Settings (variáveis de env)
│   └── __init__.py
│
├── schemas/                       # DTOs (Data Transfer Objects)
│   ├── customer.py                # ✨ CustomerInput, PredictionResponse, HealthResponse
│   └── __init__.py
│
├── services/                      # Regra de Negócio
│   ├── predict_service.py         # ✨ PredictService com Singleton + Depends
│   └── __init__.py
│
├── api_main.py                    # ✨ Aplicação FastAPI principal
└── __init__.py
```

## 🔧 Instalação

### 1. Instalar Dependências

```bash
# Com uv (recomendado - mais rápido)
uv sync

# Ou com pip
pip install -e .
```

### 2. Validar Instalação

```bash
# Via Makefile
make api-validate

# Ou diretamente
uv run python validate_api.py
```

**Esperado**: Todas as validações devem passar ✓

## 🚀 Executar a API

### Opção 1: Com Makefile (Recomendado)

```bash
make api-run
```

### Opção 2: Com Uvicorn direto

```bash
uv run uvicorn src.api_main:app --host 0.0.0.0 --port 8000 --reload
```

### Opção 3: Com Python puro

```bash
uv run python src/api_main.py
```

## 📚 Acessar a API

A API estará disponível em: `http://localhost:8000`

### Documentação Interativa

- **Swagger UI** (recomendado): http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

- **Health Check**: `GET /api/v1/health`
- **Predict**: `POST /api/v1/predict`
- **Root**: `GET /`

## 📖 Exemplos de Uso

### Health Check

```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

**Resposta** (200 OK):
```json
{
  "status": "healthy",
  "message": "API is running correctly and model is loaded",
  "version": "1.0.0"
}
```

### Predict Churn

```bash
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

**Resposta** (200 OK):
```json
{
  "customer_id": "5575-GNVDE",
  "prediction": 0,
  "prediction_label": "No",
  "prediction_probability": 0.25,
  "confidence": 0.75
}
```

## 🏗️ Arquitetura em Camadas

### 1. **API Layer** (`src/api/`)

Responsabilidades:
- Receber requisições HTTP
- Validar entrada com Pydantic
- Chamar serviços via Depends
- Retornar respostas JSON

**Arquivo**: [src/api/v1/endpoints/predict.py](../src/api/v1/endpoints/predict.py)

```python
@router.post("/predict")
def predict(
    customer: CustomerInput,                              # Validação automática
    predict_service: PredictService = Depends(...)       # Injeção de dependência
) -> PredictionResponse:
    return predict_service.predict(customer)
```

---

### 2. **Core Layer** (`src/core/`)

Responsabilidades:
- Configurações globais (Pydantic Settings)
- Variáveis de ambiente
- Paths do projeto

**Arquivo**: [src/core/config.py](../src/core/config.py)

```python
class Settings(BaseSettings):
    app_name: str = "Telco Churn Prediction API"
    model_name: str = "mlp.joblib"
    # ...carregadas automaticamente de .env
```

---

### 3. **Schema Layer** (`src/schemas/`)

Responsabilidades:
- DTOs com Pydantic
- Validação automática
- Documentação OpenAPI
- Exemplos

**Arquivo**: [src/schemas/customer.py](../src/schemas/customer.py)

```python
class CustomerInput(BaseModel):
    customer_id: str
    gender: str = Field(..., description="Male/Female")
    tenure_months: int = Field(..., ge=0)
    # ... 30+ campos com validação
```

---

### 4. **Service Layer** (`src/services/`)

Responsabilidades:
- Lógica de negócio
- Carregamento do modelo (Singleton)
- Preparação de dados
- Execução de predições

**Arquivo**: [src/services/predict_service.py](../src/services/predict_service.py)

```python
class PredictService:
    def __init__(self, model_path: Path = None):
        # Carrega modelo uma única vez
        self.pipeline = joblib.load(model_path)
    
    def predict(self, customer: CustomerInput) -> PredictionResponse:
        # Lógica de predição
        return prediction
```

---

## 💉 Injeção de Dependências

Uso massivo do padrão de Injeção de Dependências com FastAPI:

```python
# Dependência retorna PredictService
def get_predict_service() -> PredictService:
    global _predict_service
    if _predict_service is None:
        _predict_service = PredictService()
    return _predict_service

# Uso em endpoints
@router.post("/predict")
def predict(
    customer: CustomerInput,
    predict_service: PredictService = Depends(get_predict_service),
) -> PredictionResponse:
    # FastAPI injeta automaticamente
    return predict_service.predict(customer)
```

**Benefícios**:
- ✓ Reutilização de instâncias (Singleton)
- ✓ Testabilidade (fácil mockar)
- ✓ Separação de responsabilidades
- ✓ Code-splitting limpo

## 📋 Modelos Pydantic

### CustomerInput

**33 campos** representando todas as features do dataset IBM Telco:

- Identificação: `customer_id`, `count`
- Localização: `country`, `state`, `city`, `zip_code`, `latitude`, `longitude`
- Pessoal: `gender`, `senior_citizen`, `partner`, `dependents`
- Serviços: `phone_service`, `multiple_lines`, `internet_service`, etc.
- Contrato: `contract`, `paperless_billing`, `payment_method`
- Charges: `monthly_charges`, `total_charges`

### PredictionResponse

```python
{
    "customer_id": "5575-GNVDE",
    "prediction": 0,                    # 0=No, 1=Yes
    "prediction_label": "No",           # Label legível
    "prediction_probability": 0.25,     # Prob de churn
    "confidence": 0.75                  # Confiança
}
```

### HealthResponse

```python
{
    "status": "healthy",
    "message": "API is running correctly and model is loaded",
    "version": "1.0.0"
}
```

## 🧪 Testes

### Validação Rápida

```bash
make api-validate
```

### Teste de API

```bash
# Com Python
uv run python tests/test_api.py

# Com pytest
uv run pytest tests/test_api.py -v
```

## 🔐 Segurança

A API já tem:

- ✓ Validação de entrada com Pydantic
- ✓ CORS configurado
- ✓ Error handling robusto
- ✓ Logging centralizado

**Para produção, adicionar**:
- [ ] Autenticação (JWT/API Key)
- [ ] Rate Limiting
- [ ] HTTPS/SSL
- [ ] Restringir CORS origins
- [ ] Input sanitization adicional

## 📝 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Aplicação
APP_NAME=Telco Churn Prediction API
DEBUG=false
LOG_LEVEL=INFO

# Modelo
MODEL_NAME=mlp.joblib
```

## 📚 Documentação

- **Completa**: [API_GUIDE.md](../API_GUIDE.md)
- **Arquitetura**: Veja o `README.md` do projeto

## 🐛 Troubleshooting

### Erro: "Modelo não encontrado"

```
FileNotFoundError: Modelo não encontrado em: .../models/mlp.joblib
```

**Solução**: Certifique-se que o arquivo `models/mlp.joblib` existe

### Erro: "Porta 8000 em uso"

```
OSError: [Errno 48] Address already in use
```

**Solução**: Use outra porta:
```bash
uv run uvicorn src.api_main:app --port 8001
```

### Erro: "ModuleNotFoundError"

```
ModuleNotFoundError: No module named 'pydantic_settings'
```

**Solução**: Reinstale dependências:
```bash
uv sync
```

## 📦 Próximos Passos

1. **Testar a API**
   ```bash
   make api-run
   # Abrir http://localhost:8000/docs
   ```

2. **Adicionar autenticação** (JWT/API Key)

3. **Deploy** em produção (Docker, AWS Lambda, etc.)

4. **Monitoramento** (Prometheus, DataDog, etc.)

5. **Rate Limiting** e **Caching**

## ✅ Checklist

- [x] Estrutura de camadas implementada
- [x] FastAPI + Pydantic
- [x] Validação automática
- [x] Injeção de dependências
- [x] Endpoints `/health` e `/predict`
- [x] Documentação automática (Swagger)
- [x] Logging centralizado
- [x] CORS configurado
- [x] Error handling robusto
- [x] Arquivo de configuração (Pydantic Settings)
- [x] Makefile targets
- [x] Script de validação
- [x] Documentação completa

## 📞 Suporte

Para dúvidas:
1. Consulte a documentação em `/docs` (Swagger)
2. Leia [API_GUIDE.md](../API_GUIDE.md)
3. Verifique os logs da aplicação

---

**Status**: ✅ Pronto para uso! 🎉
