# C:\AI_CRM_project\dashboard\app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from src.cohort import CohortAnalysisEngine
from src.heart import HEARTEvaluationDashboard

st.set_page_config(page_title="AI-CRM Analytics Dashboard", layout="wide")

cohort_engine = CohortAnalysisEngine()
heart_engine = HEARTEvaluationDashboard()

st.title("📊 Enterprise AI-CRM Analytics Platform")
st.markdown("Live computation engine tracking cohort retention curves and Google HEART dimensions.")
st.divider()

# HEART Framework Scorecard
st.header("❤️ Google HEART Framework Scorecard")
heart_metrics = heart_engine.calculate_live_heart_metrics()

cols = st.columns(5)
for idx, (metric_name, value) in enumerate(heart_metrics.items()):
    with cols[idx]:
        st.metric(label=metric_name.split(":")[0], value=value)

st.divider()

# Cohort Retention Curve Vector by Industry
st.header("📉 Cohort Retention Curves")
cohort_data = cohort_engine.compute_cohort_retention()

plot_rows = []
for industry, metrics in cohort_data.items():
    curve = metrics["retention_curve_pct"]
    for month_idx, pct in enumerate(curve):
        plot_rows.append({
            "Industry": industry,
            "Timeline": f"Month {month_idx}",
            "Retention Rate (%)": pct
        })

df_plot = pd.DataFrame(plot_rows)
fig = px.line(df_plot, x="Timeline", y="Retention Rate (%)", color="Industry", markers=True)
st.plotly_chart(fig, use_container_width=True)
