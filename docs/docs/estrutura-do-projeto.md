# Estrutura do projeto

Esta pagina descreve a organizacao de pastas/arquivos do repositorio.

```text
.
├── LICENSE            <- Licenca do projeto
├── Makefile           <- Atalhos (setup, lint, testes, docs)
├── README.md          <- README principal do projeto
├── data/
│   ├── external/      <- Dados de terceiros
│   ├── interim/       <- Dados intermediarios transformados
│   ├── processed/     <- Dados finais para modelagem
│   └── raw/           <- Dados brutos (imutaveis)
├── docs/              <- Documentacao (MkDocs)
│   ├── mkdocs.yml
│   ├── docs/          <- Fontes (Markdown)
│   └── site/          <- Site gerado (nao versionar)
├── models/            <- Modelos treinados e artefatos
├── notebooks/         <- Notebooks Jupyter
├── pyproject.toml     <- Config do projeto e ferramentas (ruff/pytest/mkdocs)
├── uv.lock            <- Lockfile do uv para reproducibilidade
├── references/        <- Dicionarios de dados, manuais e materiais de apoio
├── reports/           <- Relatorios gerados (HTML, PDF, etc.)
│   └── figures/       <- Figuras/plots gerados para relatorios
└── tech_challenge_fase_1/ <- Codigo-fonte do projeto
    ├── __init__.py    <- Torna `tech_challenge_fase_1` um modulo Python
    └── ...            <- Modulos do projeto (a evoluir)
```

## Notas

- `docs/site/` e um artefato gerado pelo MkDocs (ignorado no git).
- Se novos modulos/pipelines forem adicionados em `tech_challenge_fase_1/`, mantenha esta pagina atualizada.
