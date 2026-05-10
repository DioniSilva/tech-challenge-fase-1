"""Gera a pagina de documentacao do ML Canvas.

Este script e usado pelo target `make docs-canvas` para gerar a pagina do MkDocs
em `docs/docs/ml-canvas.md`.
"""

from __future__ import annotations

import argparse
from dataclasses import fields
import html
from pathlib import Path

from ml_pipeline.ml_canvas import MLCanvas, create_telco_churn_prediction_canvas

PREFERRED_ORDER: list[str] = [
    "business_problem",
    "ml_task",
    "target",
    "success_metrics",
    "data_sources",
    "features",
    "constraints",
    "risks",
]

FIELD_LABELS: dict[str, str] = {
    "business_problem": "Problema de negocio",
    "ml_task": "Tarefa ML",
    "success_metrics": "Metricas de sucesso",
    "data_sources": "Fontes de dados",
    "features": "Features candidatas",
    "target": "Variavel alvo",
    "constraints": "Restricoes",
    "risks": "Riscos",
}


def humanize_field_name(name: str) -> str:
    return " ".join([part.capitalize() for part in name.split("_") if part])


def _card(title: str, body_html: str) -> str:
    return (
        '<section class="ml-canvas-card">\n'
        f'  <header class="ml-canvas-card__header">{html.escape(title)}</header>\n'
        f'  <div class="ml-canvas-card__body">{body_html}</div>\n'
        "</section>\n"
    )


def _render_scalar(value: object) -> str:
    if value is None:
        return "<p>-</p>"

    if isinstance(value, str):
        text = value.strip() or "-"
        return f"<p>{html.escape(text)}</p>"

    return f"<pre>{html.escape(repr(value))}</pre>"


def _render_list(items: list[object], *, scroll: bool) -> str:
    if not items:
        return "<p>-</p>"

    lis = "\n".join([f"<li>{html.escape(str(item))}</li>" for item in items])
    ul = f"<ul>\n{lis}\n</ul>"
    if scroll:
        return f'<div class="ml-canvas-scroll">{ul}</div>'
    return ul


def render_value(value: object, *, field_name: str) -> str:
    if isinstance(value, list):
        # Listas sao sempre visiveis. Para listas longas, manter o card compacto.
        scroll = len(value) > 10 or field_name in {"features"}
        return _render_list(value, scroll=scroll)

    return _render_scalar(value)


def iter_canvas_fields(canvas: MLCanvas):
    all_fields = [f.name for f in fields(canvas) if f.name != "project_name"]

    preferred = [name for name in PREFERRED_ORDER if name in all_fields]
    preferred_set = set(preferred)
    remaining = [name for name in all_fields if name not in preferred_set]
    return preferred + remaining


def render_canvas_page(canvas: MLCanvas) -> str:
    title = canvas.project_name.strip() or "ML Canvas"

    parts: list[str] = []
    parts.append(f"# {title}\n")
    parts.append("Documentacao das definicoes do ML Canvas para o projeto de churn prediction.\n")
    parts.append(
        f"> Data Readiness Score: {canvas.data_readiness_score() * 100:.0f}%\n"
        ">\n"
        f"> Projeto viavel: {'Sim' if canvas.is_viable() else 'Nao'}\n"
    )
    parts.append("\n")
    parts.append("Para atualizar esta pagina, rode: `make docs-canvas`\n")

    parts.append('<div class="ml-canvas-grid">\n')
    for field_name in iter_canvas_fields(canvas):
        value = getattr(canvas, field_name)
        label = FIELD_LABELS.get(field_name) or humanize_field_name(field_name)
        body = render_value(value, field_name=field_name)
        parts.append(_card(label, body))

    parts.append("</div>\n")

    return "\n".join(parts).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera a pagina do ML Canvas para o MkDocs")
    parser.add_argument(
        "--out",
        default="docs/docs/ml-canvas.md",
        help="Caminho do arquivo Markdown de saida (padrao: docs/docs/ml-canvas.md)",
    )
    args = parser.parse_args()

    canvas = create_telco_churn_prediction_canvas()
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_canvas_page(canvas), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
