"""
Script de teste para a API.
Demonstra como usar os endpoints.
"""
import requests
import json


# URL base da API
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"


def test_health():
    """Testa o endpoint de health check."""
    print("\n=== Health Check ===")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_predict():
    """Testa o endpoint de predição."""
    print("\n=== Predict ===")
    
    # Exemplo de payload
    customer = {
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
        "total_charges": "5046.00",
    }
    
    response = requests.post(f"{API_URL}/predict", json=customer)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


if __name__ == "__main__":
    print("Testando API Telco Churn Prediction")
    
    try:
        health_ok = test_health()
        predict_ok = test_predict()
        
        print("\n=== Resumo ===")
        print(f"Health Check: {'✓' if health_ok else '✗'}")
        print(f"Predict: {'✓' if predict_ok else '✗'}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API")
        print(f"Certifique-se de que a API está rodando em {BASE_URL}")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
