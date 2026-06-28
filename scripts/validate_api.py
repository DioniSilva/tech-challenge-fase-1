"""
Validação rápida da API.

Este script é um smoke check de desenvolvimento: verifica imports, criação da
aplicação FastAPI e carregamento das configurações. A validação funcional dos
endpoints continua na suíte de testes.
"""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


def test_imports():
    """Testa se os módulos principais podem ser importados."""
    print("Testando importações...")

    try:
        from core.config import settings

        print("[OK] core.config importado")

        from schemas import CustomerInput, HealthResponse, PredictionResponse

        print("[OK] schemas importados")

        from services import PredictService, get_predict_service

        print("[OK] services importados")

        from api.v1.endpoints.predict import router as predict_router

        print("[OK] api.v1.endpoints.predict importado")

        from api.v1.api import api_router

        print("[OK] api.v1.api importado")

        from api_main import app

        print("[OK] api_main importado")

        # Evita falsos positivos de imports removidos por otimizadores/linters.
        _ = (
            settings,
            CustomerInput,
            HealthResponse,
            PredictionResponse,
            PredictService,
            get_predict_service,
            predict_router,
            api_router,
            app,
        )

        return True
    except Exception as e:
        print(f"[ERRO] Erro na importação: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def test_app_structure():
    """Testa se a aplicação FastAPI está estruturada corretamente."""
    print("\nTestando estrutura da aplicação...")

    try:
        from api_main import app

        print(f"[OK] Rotas registradas: {len(app.routes)}")
        if len(app.routes) > 0:
            print("  [OK] Rotas estão configuradas")

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
        print(f"[ERRO] Erro ao testar configurações: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def check_runtime_artifacts():
    """Avisa sobre arquivos necessários para executar treino/API localmente."""
    print("\nVerificando artefatos locais...")

    from config import DATA_FILE
    from core.config import settings

    has_dataset = DATA_FILE.exists()
    has_model = settings.model_path.exists()

    if has_dataset:
        print(f"[OK] Dataset encontrado: {DATA_FILE}")
    else:
        print(f"[AVISO] Dataset ausente: {DATA_FILE}")
        print("        Verifique se Telco_customer_churn.xlsx esta versionado em data/raw/.")

    if has_model:
        print(f"[OK] Modelo encontrado: {settings.model_path}")
    else:
        print(f"[AVISO] Modelo ausente: {settings.model_path}")
        print("        Execute make train após preparar o dataset.")


def main():
    """Executa as validações rápidas da API."""
    print("=" * 60)
    print("VALIDAÇÃO DA API TELCO CHURN PREDICTION")
    print("=" * 60)

    results = {
        "Importações": test_imports(),
        "Estrutura da aplicação": test_app_structure(),
        "Configurações": test_settings(),
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
    check_runtime_artifacts()

    if all_passed:
        print("\n[SUCESSO] Todas as validações passaram!")
        print("\nPróximos passos:")
        print("1. Execute a API: make serve")
        print("2. Acesse a documentação: http://localhost:8000/docs")
        print("3. Rode os testes funcionais: make test")
    else:
        print("\n[FALHA] Algumas validações falharam. Verifique os erros acima.")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
