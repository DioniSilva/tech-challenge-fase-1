import pandas as pd
from sklearn.model_selection import train_test_split

from config import LOGGING_LEVEL, RANDOM_STATE, TARGET, TEST_SIZE, set_seeds
from data.io import carregar_dados, save_pipeline
from data.mlp_config import MLPConfig
from data.training_result import TrainingResult
from modeling.model_evaluator import ModelEvaluator
from modeling.trainer import Trainer
from utils.app_logging import configurar_logging, logger
from utils.champion_selector import ChampionSelector
from utils.mlflow_tracker import MLFlowTracker


def main():

    configurar_logging(nivel=LOGGING_LEVEL)

    set_seeds()

    MLFlowTracker.configure_mlflow_tracking()

    df = carregar_dados()

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    config = MLPConfig()

    trainer = Trainer(config)

    outputs = []

    for threshold in [0.45, 0.30, 0.70]:
        output = trainer.train(
            X_train,
            y_train,
            X_test,
            y_test,
            threshold,
        )

        outputs.append(output)

    champion = ChampionSelector.select(outputs)

    save_pipeline(champion.pipeline)

    print_comparison([o.metrics for o in outputs])

    getMetricsForPopulationByGender(X_test, y_test, champion.pipeline, champion.metrics.threshold, 'Female')
    getMetricsForPopulationByGender(X_test, y_test, champion.pipeline, champion.metrics.threshold, 'Male')
    getMetricsForPopulationBySeniorCitizen(X_test, y_test, champion.pipeline, champion.metrics.threshold, 'Yes')
    getMetricsForPopulationBySeniorCitizen(X_test, y_test, champion.pipeline, champion.metrics.threshold, 'No')


def getMetricsForPopulationByGender(X_test, y_test, pipeline, threshold, gender):
    getMetricsForSpecificPopulation(X_test, y_test, pipeline, threshold, 'Gender', gender)


def getMetricsForPopulationBySeniorCitizen(X_test, y_test, pipeline, threshold, is_senior_citizen):
    getMetricsForSpecificPopulation(X_test, y_test, pipeline, threshold, 'Senior Citizen', is_senior_citizen)


def getMetricsForSpecificPopulation(X_test, y_test, pipeline, threshold, filter_feature, filter_value):
    is_targeted_feature = X_test[filter_feature] == filter_value

    X_test_filtered = X_test[is_targeted_feature]
    y_test_filtered = y_test[is_targeted_feature]

    metrics = ModelEvaluator.evaluate(
        pipeline,
        X_test_filtered,
        y_test_filtered,
        threshold,
        '',
    )

    logger.info(f"Métricas para grupo de dados filtrado ({filter_feature} = {filter_value}):")
    print_comparison([metrics])


def print_comparison(results: list[TrainingResult]):

    champion = sorted(
        results,
        key=lambda x: (x.recall, x.pr_auc),
        reverse=True,
    )[0]

    rows = []

    for result in results:
        trophy = "🏆" if result.threshold == champion.threshold else ""

        rows.append(
            {
                "Winner": trophy,
                "Threshold": result.threshold,
                "Accuracy": round(result.accuracy, 4),
                "Precision": round(result.precision, 4),
                "Recall": round(result.recall, 4),
                "F1": round(result.f1_score, 4),
                "ROC-AUC": round(result.roc_auc, 4),
                "PR-AUC": round(result.pr_auc, 4),
                "Confidence": round(result.confidence_score, 4),
            }
        )

    comparison_df = pd.DataFrame(rows)

    logger.info(
        "\n%s",
        comparison_df.to_string(index=False),
    )

    logger.info(
        "🏆 Modelo campeão: threshold=%.2f | Recall=%.4f | PR-AUC=%.4f",
        champion.threshold,
        champion.recall,
        champion.pr_auc,
    )


if __name__ == "__main__":
    main()
