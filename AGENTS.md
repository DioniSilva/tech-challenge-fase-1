# AGENTS.md

## Project Context

- This is the Postech Tech Challenge Fase 1 repo: churn prediction for the IBM Telco dataset, with required PyTorch MLP, sklearn baselines, MLflow tracking, FastAPI, tests, and documentation.
- Keep challenge-specific requirements in sync with `agents/agent_context.md`; do not duplicate the full brief here.

## Environment And Commands

- Python is pinned to `~=3.12.0` in `pyproject.toml`; use `uv` and the Makefile instead of ad-hoc `pip` commands.
- Initial setup: `make setup` creates `.venv` with Python 3.12 and runs `uv sync`.
- Quality check: `make lint` runs `uv run ruff format --check` then `uv run ruff check`.
- Auto-format: `make format` runs `uv run ruff check --fix` then `uv run ruff format`.
- Tests: `make test` runs `uv run pytest tests`; for one file use `uv run pytest tests/test_data.py`.
- Docs: `make docs` serves MkDocs using `docs/mkdocs.yml`; `make docs-build` builds to `docs/site/`.
- `make docs` and `make docs-build` both regenerate `docs/docs/ml-canvas.md` via `make docs-canvas` first.
- MLflow UI: `make run-mlflow` changes into `data/mlflow_tracking` and runs `uv run mlflow ui`, serving `http://127.0.0.1:5000`.

## Current Repo Shape

- Importable package is `ml_pipeline` from `src/ml_pipeline`; `pyproject.toml` uses `flit_core` and `[tool.flit.module] name = "ml_pipeline"`.
- Existing utility scripts live under `src/utils`; `src/utils/build_ml_canvas.py` generates `docs/docs/ml-canvas.md` from `src/ml_pipeline/ml_canvas.py`.
- MkDocs config is `docs/mkdocs.yml`, and because that file lives under `docs/`, markdown sources are under `docs/docs/`.
- Dataset documentation currently assumes IBM Telco Customer Churn with 7043 rows, 33 variables, target `Churn Value`, and original column names with spaces.

## Gotchas

- `make test` currently fails because `tests/test_data.py` contains a placeholder `assert False`; fix or replace it before treating tests as a signal.
- `src/utils/mlflow_logger.py` currently uses `print()` and Unicode status symbols; the challenge requires structured logging and no `print()` in production code.
- `.gitignore` ignores `/data/*`, so raw/processed data and local MLflow stores are not versioned by default.
- `.gitignore` also ignores `uv.lock` even though the README describes it as the reproducibility lockfile; verify desired tracking before modifying lockfile behavior.
- Ruff only includes `pyproject.toml` and `src/**/*.py`; tests are not linted by the current config unless the config is changed.
