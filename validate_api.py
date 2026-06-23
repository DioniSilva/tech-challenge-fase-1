"""
Script de validação rápida da API.
Testa se os módulos podem ser importados e se a estrutura está correta.
"""
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Testa se todos os módulos podem ser importados."""
    print("Testando importações...")
    
    try:
        from core.config import settings
        print("[OK] core.config importado")
        
        from schemas import CustomerInput, PredictionResponse, HealthResponse
        print("[OK] schemas importados")
        
        from services import PredictService, get_predict_service
        print("[OK] services importados")
        
        from api.v1.endpoints.predict import router as predict_router
        print("[OK] api.v1.endpoints.predict importado")
        
        from api.v1.api import api_router
        print("[OK] api.v1.api importado")
        
        from api_main import app
        print("[OK] api_main importado")
        
        return True
    except Exception as e:
        print(f"[ERRO] Erro na importacao: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_app_structure():
    """Testa se a aplicação FastAPI está estruturada corretamente."""
    print("\nTestando estrutura da aplicação...")
    
    try:
        from api_main import app
        
        # Verificar se a aplicação tem rotas
        print(f"[OK] Rotas registradas: {len(app.routes)}")
        
        # Verificar se há rotas definidas
        has_routes = len(app.routes) > 0
        
        if has_routes:
            print(f"  [OK] Rotas estao configuradas")
        
        # Verificar middlewares
        print(f"[OK] Middlewares configurados: {len(app.user_middleware)}")
        
        return True
    except Exception as e:
        print(f"[ERRO] Erro ao testar estrutura: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_settings():
    """Testa se as configurações estão carregadas corretamente."""
    print("\nTestando configurações...")
    
    try:
        from core.config import settings
        
        print(f"[OK] App Name: {settings.app_name}")
        print(f"[OK] App Version: {settings.app_version}")
        print(f"[OK] API Prefix: {settings.api_prefix}")
        print(f"[OK] Model Name: {settings.model_name}")
        print(f"[OK] Models Dir: {settings.models_dir}")
        
        return True
    except Exception as e:
        print(f"[ERRO] Erro ao testar configuracoes: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Função principal de validação."""
    print("=" * 60)
    print("VALIDACAO DA API TELCO CHURN PREDICTION")
    print("=" * 60)
    
    results = {
        "Importacoes": test_imports(),
        "Estrutura da Aplicacao": test_app_structure(),
        "Configuracoes": test_settings(),
    }
    
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "[PASSOU]" if passed else "[FALHOU]"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n[SUCESSO] Todas as validacoes passaram!")
        print("\nProximos passos:")
        print("1. Execute a API: uv run uvicorn src.api_main:app --reload")
        print("2. Acesse a documentacao: http://localhost:8000/docs")
        print("3. Teste os endpoints com cURL ou Postman")
    else:
        print("\n[FALHA] Algumas validacoes falharam. Verifique os erros acima.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
