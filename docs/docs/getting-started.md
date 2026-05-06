# Primeiros passos

## Requisitos

- Python 3.12
- `uv` instalado

## Configurar ambiente e dependências

Use o comando abaixo para criar o ambiente e instalar as dependências do projeto:

```bash
make setup
```

## Qualidade e testes

```bash
make lint
make format
make test
```

## Documentação

Subir a documentação localmente:

```bash
make docs
```

Gerar o site estático em `docs/site/`:

```bash
make docs-build
```
