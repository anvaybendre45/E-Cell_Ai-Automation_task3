# C:\AI_CRM_project\verify_analytics.py
from src.cohort import CohortAnalysisEngine
from src.heart import HEARTEvaluationDashboard

cohort_engine = CohortAnalysisEngine()
heart_engine = HEARTEvaluationDashboard()

print("--- Testing Modules 3 & 4: Analytical Calculations Engine ---")

# 1. Evaluate Cohort Trends
cohorts = cohort_engine.compute_cohort_retention()
print("\n[1/3] Cohort Segmentation Summary (By Industry Vertical):")
for ind, metrics in list(cohorts.items())[:3]:
    print(f"      Industry: {ind} | Total Scale: {metrics['total_cohort_size']} | Retention Vector: {metrics['retention_curve_pct']}")

# 2. Evaluate Predictive Risk Flags
predictions = cohort_engine.predict_churn_scores()
print(f"\n[2/3] Predictive Risk Engine Output Examples:")
for p in predictions[:2]:
    print(f"      Client ID: {p['customer_id']} ({p['name']}) -> Risk Churn Score: {p['churn_probability_flag']}")

# 3. Evaluate Framework Metrics Calculation Vector
heart_metrics = heart_engine.calculate_live_heart_metrics()
print("\n[3/3] Calculated Live Google HEART Framework Vectors:")
for metric_key, value in heart_metrics.items():
    print(f"      {metric_key}: {value}")