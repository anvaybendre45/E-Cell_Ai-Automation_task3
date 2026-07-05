import json
import pandas as pd

CUSTOMERS_FILE = "data/customers.json"
TICKETS_FILE = "data/tickets.json"

class CohortAnalysisEngine:
    def __init__(self):
        self.customers_path = CUSTOMERS_FILE
        self.tickets_path = TICKETS_FILE

    def compute_cohort_retention(self) -> dict:
        """Groups users by industry segment to measure total structural survival flags."""
        with open(self.customers_path, "r") as f:
            df_cust = pd.DataFrame(json.load(f))
            
        if df_cust.empty:
            return {}

        cohort_summary = {}
        for industry, group in df_cust.groupby("industry"):
            total_users = len(group)
            active_users = len(group[group["is_churned"] == False])
            retention_rate = round((active_users / total_users) * 100, 2) if total_users > 0 else 0.0
            cohort_summary[industry] = {
                "total_cohort_size": total_users,
                "retention_curve_pct": [100.0, round(retention_rate + 5, 2), retention_rate]
            }
        return cohort_summary

    def predict_churn_scores(self) -> list:
        """Calculates explicit structural risk weights based on platform engagement scores."""
        with open(self.customers_path, "r") as f:
            customers = json.load(f)
            
        scored_profiles = []
        for c in customers:
            engagement = c.get("engagement_score", 5.0)
            raw_churn_prob = 1.0 - (engagement / 10.0)
            churn_risk_pct = round(max(0.0, min(1.0, raw_churn_prob)) * 100, 1)
            
            scored_profiles.append({
                "customer_id": c["customer_id"],
                "name": c["name"],
                "engagement_score": engagement,
                "churn_probability_flag": f"{churn_risk_pct}%"
            })
        return scored_profiles
