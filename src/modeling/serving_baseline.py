import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class BaselineServingTransformer(BaseEstimator, TransformerMixin):
    FEATURE_COLUMNS = [
        "zip_code",
        "monthly_charges",
        "average_monthly_spend",
        "gender_Male",
        "senior_citizen_Yes",
        "partner_Yes",
        "dependents_Yes",
        "phone_service_Yes",
        "multiple_lines_No phone service",
        "multiple_lines_Yes",
        "internet_service_Fiber optic",
        "internet_service_No",
        "online_security_No internet service",
        "online_security_Yes",
        "online_backup_No internet service",
        "online_backup_Yes",
        "device_protection_No internet service",
        "device_protection_Yes",
        "tech_support_No internet service",
        "tech_support_Yes",
        "streaming_tv_No internet service",
        "streaming_tv_Yes",
        "streaming_movies_No internet service",
        "streaming_movies_Yes",
        "contract_One year",
        "contract_Two year",
        "paperless_billing_Yes",
        "payment_method_Credit card (automatic)",
        "payment_method_Electronic check",
        "payment_method_Mailed check",
    ]

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        df.columns = [str(column).lower().replace(" ", "_") for column in df.columns]

        total_charges = pd.to_numeric(df.get("total_charges"), errors="coerce").fillna(0.0)
        tenure_months = pd.to_numeric(df.get("tenure_months"), errors="coerce").fillna(0.0)
        monthly_charges = pd.to_numeric(df.get("monthly_charges"), errors="coerce").fillna(0.0)
        zip_code = pd.to_numeric(df.get("zip_code"), errors="coerce").fillna(0.0)

        average_monthly_spend = np.where(tenure_months > 0, total_charges / tenure_months, 0.0)

        features = pd.DataFrame(index=df.index)
        features["zip_code"] = zip_code.astype(float)
        features["monthly_charges"] = monthly_charges.astype(float)
        features["average_monthly_spend"] = average_monthly_spend.astype(float)

        features["gender_Male"] = self._match(df, "gender", "Male")
        features["senior_citizen_Yes"] = self._match(df, "senior_citizen", "Yes")
        features["partner_Yes"] = self._match(df, "partner", "Yes")
        features["dependents_Yes"] = self._match(df, "dependents", "Yes")
        features["phone_service_Yes"] = self._match(df, "phone_service", "Yes")
        features["multiple_lines_No phone service"] = self._match(
            df, "multiple_lines", "No phone service"
        )
        features["multiple_lines_Yes"] = self._match(df, "multiple_lines", "Yes")
        features["internet_service_Fiber optic"] = self._match(
            df, "internet_service", "Fiber optic"
        )
        features["internet_service_No"] = self._match(df, "internet_service", "No")
        features["online_security_No internet service"] = self._match(
            df, "online_security", "No internet service"
        )
        features["online_security_Yes"] = self._match(df, "online_security", "Yes")
        features["online_backup_No internet service"] = self._match(
            df, "online_backup", "No internet service"
        )
        features["online_backup_Yes"] = self._match(df, "online_backup", "Yes")
        features["device_protection_No internet service"] = self._match(
            df, "device_protection", "No internet service"
        )
        features["device_protection_Yes"] = self._match(df, "device_protection", "Yes")
        features["tech_support_No internet service"] = self._match(
            df, "tech_support", "No internet service"
        )
        features["tech_support_Yes"] = self._match(df, "tech_support", "Yes")
        features["streaming_tv_No internet service"] = self._match(
            df, "streaming_tv", "No internet service"
        )
        features["streaming_tv_Yes"] = self._match(df, "streaming_tv", "Yes")
        features["streaming_movies_No internet service"] = self._match(
            df, "streaming_movies", "No internet service"
        )
        features["streaming_movies_Yes"] = self._match(df, "streaming_movies", "Yes")
        features["contract_One year"] = self._match(df, "contract", "One year")
        features["contract_Two year"] = self._match(df, "contract", "Two year")
        features["paperless_billing_Yes"] = self._match(df, "paperless_billing", "Yes")
        features["payment_method_Credit card (automatic)"] = self._match(
            df, "payment_method", "Credit card (automatic)"
        )
        features["payment_method_Electronic check"] = self._match(
            df, "payment_method", "Electronic check"
        )
        features["payment_method_Mailed check"] = self._match(df, "payment_method", "Mailed check")

        return features.reindex(columns=self.FEATURE_COLUMNS, fill_value=0.0)

    def _match(self, df, column_name, expected_value):
        series = df.get(column_name)
        if series is None:
            return pd.Series(0.0, index=df.index)
        return series.fillna("").astype(str).eq(expected_value).astype(float)
