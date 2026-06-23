class ChampionSelector:
    @staticmethod
    def select(results):

        return max(
            results,
            key=lambda r: (
                r.metrics.recall,
                r.metrics.pr_auc,
            ),
        )
