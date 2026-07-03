# C:\AI_CRM_project\src\heart.py
import json
import pandas as pd

CUSTOMERS_FILE = "data/customers.json"
TICKETS_FILE = "data/tickets.json"

class HEARTEvaluationDashboard:
    def __init__(self):
        self.customers_path = CUSTOMERS_FILE
        self.tickets_path = TICKETS_FILE

    def calculate_live_heart_metrics(self) -> dict:
        """Computes Google HEART framework variables from live operational records."""
        with open(self.customers_path, "r") as f:
            df_cust = pd.DataFrame(json.load(f))
        with open(self.tickets_path, "r") as f:
            df_tick = pd.DataFrame(json.load(f))

        # 1. Happiness: Average structural CSAT derived from engagement scales
        avg_csat = round(df_cust["engagement_score"].mean() * 10, 1) if not df_cust.empty else 75.0

        # 2. Engagement: Average tickets filed per active client segment profile
        total_tickets = len(df_tick)
        total_clients = len(df_cust)
        engagement_density = round(total_tickets / total_clients, 2) if total_clients > 0 else 0.0

        # 3. Adoption: Percentage of premium client footprints sitting on Enterprise Tier structures
        enterprise_count = len(df_cust[df_cust["product_tier"] == "Enterprise"])
        adoption_rate = round((enterprise_count / total_clients) * 100, 1) if total_clients > 0 else 0.0

        # 4. Retention: Active survival footprint ratio
        active_count = len(df_cust[df_cust["is_churned"] == False])
        retention_rate = round((active_count / total_clients) * 100, 1) if total_clients > 0 else 0.0

        # 5. Task Success: Simulation tracking of Closed resolution rates
        closed_tickets = len(df_tick[df_tick["status"] == "Closed"])
        task_success_rate = round((closed_tickets / total_tickets) * 100, 1) if total_tickets > 0 else 0.0

        return {
            "Dimension H: Happiness (Avg CSAT Score)": f"{avg_csat}%",
            "Dimension E: Engagement (Ticket Index Density)": f"{engagement_density} tickets/client",
            "Dimension A: Adoption (Enterprise Tier Footprint)": f"{adoption_rate}%",
            "Dimension R: Retention (System Survival Pct)": f"{retention_rate}%",
            "Dimension T: Task Success (Ticket Resolution Efficiency)": f"{task_success_rate}%"
        }
