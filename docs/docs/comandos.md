# Comandos

Os comandos abaixo estao definidos no `Makefile` e rodam ferramentas dentro do ambiente gerenciado pelo `uv`.

## Setup

```bash
make setup
```

Cria a virtualenv com `uv` e instala/sincroniza as dependencias.

## Lint e formatacao

```bash
make lint
```

Valida formatacao e regras de lint (`ruff`).

```bash
make format
```

Aplica correcoes automaticas e formata o codigo.

## Testes

```bash
make test
```

Roda a suite de testes com `pytest`.

## Documentacao

```bash
make docs
```

Sobe um servidor local do MkDocs.

```bash
make docs-build
```

Gera o site estatico em `docs/site/`.

## Limpeza

```bash
make clean
```

Remove caches e bytecode Python (`__pycache__`, `*.pyc`, `*.pyo`).
