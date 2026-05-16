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
            "Com base nos dados apresentados, a taxa de churn histórica está girando em torno de 26,5%."
            "No mercado de Telecom, isso é considerado um churn alto (o ideal para grandes operadoras de telefonia e internet fixa costuma orbitar abaixo de 1.5% a 2% ao mês, o que daria algo entre 18% e 24% ao ano)."
            "O nosso alvo é trazer essa taxa de 26,5% para a faixa dos 20% a 21% no acumulado."
            "Para isso precisamos de um modelo que identifique, com alta precisão, os top 10% ou 20% de clientes com maior risco de evasão."
            "Se conseguirmos agir preventivamente apenas nesse grupo mais crítico disparando uma oferta de retenção ou um upgrade de serviço, já batemos a nossa meta."
        ),
        ml_task="Prototipação de um modelo de ML baseline e posterior evolução para Rede Neural para classificação binária (Churn: 0/1)",
        success_metrics=[
            "Redução do churn de 26,5% para 20-21% no acumulado nos próximos 12 meses",
            "Recall >= 0.80", 
            "Precision >= 0.60"
        ],
        data_sources=["Telco_customer_churn.xlsx"],
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
            "Ranquamento por Risco: O modelo deve entregar a probabilidade de churn (0% a 100%) e não apenas 'Sim/Não', permitindo que o time de atendimento priorize os clientes mais críticos.",
            "Explicabilidade (White Box): Precisamos saber por que o cliente está em risco (ex: variáveis mais importantes) para direcionar o argumento de retenção do atendente.",
            "Valor do Cliente (Margem): A estratégia futura deve diferenciar clientes de alto valor (Fibra/Combos) de clientes de baixa margem (DSL básico)."
        ],
        risks=[
            "Viés de permanência do cliente nos dados",
            "Desbalanceamento de classes (73.5% permanência vs 26.5% churn)",
            "Mudanças no comportamento do cliente ao longo do tempo",
            "Dados Faltantes ou Inconsistentes",
            "Privacidade e LGPD: Garantir que o uso dos dados esteja em conformidade com as regulamentações de privacidade, evitando o uso de informações sensíveis ou identificáveis sem consentimento adequado.",
            "Fadiga do Cliente: Ligar excessivamente para clientes que o modelo apontou como risco (mas que na verdade estavam satisfeitos) pode gerar o efeito inverso: lembrar o cliente de que ele gasta muito e incentivá-lo a pesquisar a concorrência.",
            "Viés de Seleção: O dataset é uma foto histórica. Se focarmos apenas em quem já saiu, podemos ignorar padrões de clientes que estão insatisfeitos hoje, mas que têm amarras contratuais diferentes dos clientes do passado.",
            "Custo de Retenção Ineficiente: Gastar mais dinheiro para reter um cliente (com bônus, upgrades grátis e infraestrutura) do que o valor real que ele trará de retorno financeiro para a empresa no tempo de vida restante dele."
        ],
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    canvas = create_telco_churn_prediction_canvas()
    canvas.display()
