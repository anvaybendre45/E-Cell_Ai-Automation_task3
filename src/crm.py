# C:\AI_CRM_project\src\crm.py
import os
import json
from datetime import datetime

# Relative paths for cross-platform compatibility (Windows & Streamlit Linux cloud)
CUSTOMERS_FILE = "data/customers.json"
TICKETS_FILE = "data/tickets.json"

class CRMEngine:
    def __init__(self):
        self.customers_path = CUSTOMERS_FILE
        self.tickets_path = TICKETS_FILE
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        """Creates the data directory and mock data files if they do not exist."""
        os.makedirs(os.path.dirname(self.customers_path), exist_ok=True)
        
        if not os.path.exists(self.customers_path):
            with open(self.customers_path, "w") as f:
                json.dump([], f)
                
        if not os.path.exists(self.tickets_path):
            with open(self.tickets_path, "w") as f:
                json.dump([], f)

    def create_ticket(self, ticket_data: dict) -> dict:
        """Appends a newly raised support ticket payload into the JSON persistence layer."""
        with open(self.tickets_path, "r") as f:
            try:
                tickets = json.load(f)
            except json.JSONDecodeError:
                tickets = []

        # Ensure essential structure fields exist
        ticket_data["status"] = ticket_data.get("status", "Open")
        ticket_data["created_at"] = datetime.now().isoformat()
        
        tickets.append(ticket_data)
        
        with open(self.tickets_path, "w") as f:
            json.dump(tickets, f, indent=4)
            
        return ticket_data

    def get_customer_tickets(self, customer_id: str) -> list:
        """Filters and returns all active ticket records linked to a specific customer ID."""
        with open(self.tickets_path, "r") as f:
            try:
                tickets = json.load(f)
            except json.JSONDecodeError:
                return []
                
        return [t for t in tickets if t.get("customer_id") == customer_id]
