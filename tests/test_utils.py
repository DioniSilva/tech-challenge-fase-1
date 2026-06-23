import html
import argparse
from pathlib import Path

import pandas as pd
from ml_pipeline.ml_canvas import MLCanvas, create_telco_churn_prediction_canvas
from utils.build_ml_canvas import render_value, iter_canvas_fields, render_canvas_page, humanize_field_name


def test_humanize_field_name():
    assert humanize_field_name("business_problem") == "Business Problem"
    assert humanize_field_name("target") == "Target"


def test_render_value_renders_scalar_and_list():
    assert render_value("hello", field_name="business_problem") == "<p>hello</p>"
    assert "<ul>" in render_value(["a", "b"], field_name="features")


def test_iter_canvas_fields_preserves_preferred_order():
    canvas = MLCanvas(
        project_name="Test",
        business_problem="Problem",
        ml_task="Classificação",
        success_metrics=["AUC"],
        data_sources=["data.csv"],
        features=["f1", "f2", "f3"],
        target="target",
    )

    fields_order = iter_canvas_fields(canvas)
    assert fields_order[0] == "business_problem"
    assert fields_order[1] == "ml_task"
    assert "features" in fields_order


def test_render_canvas_page_contains_expected_sections():
    canvas = create_telco_churn_prediction_canvas()
    content = render_canvas_page(canvas)

    assert "TELCO Customer Churn Prediction" in content
    assert "Data Readiness Score" in content
    assert "Projeto" in content
    assert "vi" in content.lower()
