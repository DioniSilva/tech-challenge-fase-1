"""ML Canvas — exercício interativo para mapeamento de projeto de ML.

Auxilia na definição do problema, dados necessários, métricas de sucesso
e critérios de viabilidade antes de iniciar o desenvolvimento.

Uso:
    python ml_canvas.py
"""

from dataclasses import dataclass, field
import logging


def _render_canvas_as_text(canvas: "MLCanvas") -> str:
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append(f"ML CANVAS — {canvas.project_name}")
    lines.append("=" * 60)
    lines.append(f"Problema de negócio: {canvas.business_problem}")
    lines.append(f"Tarefa ML: {canvas.ml_task}")
    lines.append(f"Variável alvo: {canvas.target}")
    lines.append(f"Métricas de sucesso: {', '.join(canvas.success_metrics)}")
    lines.append(f"Fontes de dados: {', '.join(canvas.data_sources)}")
    lines.append(f"Features candidatas: {', '.join(canvas.features)}")
    lines.append(f"Restrições: {', '.join(canvas.constraints) or 'Nenhuma'}")
    lines.append(f"Riscos: {', '.join(canvas.risks) or 'Nenhum'}")
    lines.append("-" * 60)
    score = canvas.data_readiness_score()
    lines.append(f"Data Readiness Score: {score * 100:.0f}%")
    lines.append(f"Projeto viável: {'✓' if canvas.is_viable() else '✗'}")
    return "\n".join(lines) + "\n"


logger = logging.getLogger(__name__)


@dataclass
class MLCanvas:
    """Representação do ML Canvas para um projeto de ML.

    Attributes:
        project_name: Nome do projeto.
        business_problem: Descrição do problema de negócio.
        ml_task: Tipo de tarefa ML (classificação, regressão, etc.).
        success_metrics: Métricas de sucesso do projeto.
        data_sources: Fontes de dados disponíveis.
        features: Features candidatas.
        target: Variável alvo.
        constraints: Restrições do projeto.
        risks: Riscos identificados.
    """

    project_name: str = ""
    business_problem: str = ""
    ml_task: str = ""
    success_metrics: list[str] = field(default_factory=list)
    data_sources: list[str] = field(default_factory=list)
    features: list[str] = field(default_factory=list)
    target: str = ""
    constraints: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)

    def data_readiness_score(self) -> float:
        """Calcula score de prontidão dos dados (0.0 a 1.0).

        Returns:
            Score entre 0.0 (sem dados) e 1.0 (totalmente pronto).
        """
        checks = [
            bool(self.data_sources),
            bool(self.features),
            bool(self.target),
            len(self.data_sources) >= 2,
            len(self.features) >= 3,
        ]
        return sum(checks) / len(checks)

    def is_viable(self) -> bool:
        """Verifica se o projeto possui os elementos mínimos definidos.

        Returns:
            True se o projeto está minimamente definido, False caso contrário.
        """
        return all(
            [
                self.project_name,
                self.business_problem,
                self.ml_task,
                self.target,
                self.success_metrics,
            ]
        )

    def display(self) -> None:
        """Exibe o canvas formatado no log."""
        for line in _render_canvas_as_text(self).splitlines():
            logger.info("%s", line)


# TODO: considerar externalizar este canvas para YAML (fonte de verdade) e gerar a doc automaticamente a partir dele.
def create_telco_churn_prediction_canvas() -> MLCanvas:
    """Cria ML Canvas para o dataset Telco Churn Prediction.

    Returns:
        MLCanvas preenchido com dados do projeto Telco Churn Prediction.
    """
    return MLCanvas(
        project_name="TELCO Customer Churn Prediction",
        business_problem=(
            "Reduzir o Churn através da identificação de clientes "
            "com perfis de alto risco de saída e alto LTV."
        ),
        ml_task="Rede Neural para classificação binária (Churn: 0/1)",
        success_metrics=["AUC-ROC >= 0.85", "F1-Score >= 0.80", "Precision >= 0.78"],
        data_sources=["Telco_customer_churn.xlsx", "Outras fontes sobre análise de churn"],
        features=[
            "Count",
            "Country",
            "State",
            "City",
            "Zip Code",
            "Lat Long",
            "Latitude",
            "Longitude",
            "Gender",
            "Senior Citizen",
            "Partner",
            "Dependents",
            "Tenure Months",
            "Phone Service",
            "Multiple Lines",
            "Internet Service",
            "Online Security",
            "Online Backup",
            "Device Protection",
            "Tech Support",
            "Streaming TV",
            "Streaming Movies",
            "Contract",
            "Paperless Billing",
            "Payment Method",
            "Monthly Charges",
            "Total Charges",
            "Churn Label",
            "Churn Score",
            "CLTV",
            "Churn Reason",
        ],
        target="Churn Value",
        constraints=[
            "Dados fictícios — sem possibilidade de coletar mais",
            "Latência de predição < 100ms",
        ],
        risks=[
            "Viés de permanência do cliente nos dados",
            "Desbalanceamento de classes (73.5% permanência vs 26.5% churn)",
        ],
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    canvas = create_telco_churn_prediction_canvas()
    canvas.display()
