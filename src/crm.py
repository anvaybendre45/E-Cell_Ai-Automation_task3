# C:\AI_CRM_project\src\crm.py
import os
import json
from datetime import datetime

# Change from absolute windows paths to clean relative paths
CUSTOMERS_FILE = "data/customers.json"
TICKETS_FILE = "data/tickets.json"

class CRMEngine:
    def __init__(self):
        self.customers_path = CUSTOMERS_FILE
        self.tickets_path = TICKETS_FILE
        self._ensure_files_exist()
        
    # ... (Keep the exact rest of your class code completely identical) ...
    def _ensure_files_exist(self):
        """Ensures structural JSON files are present on disk."""
        os.makedirs(os.path.dirname(self.customers_path), exist_ok=True)
        if not os.path.exists(self.customers_path):
            with open(self.customers_path, "w") as f:
                json.dump([], f)
        if not os.path.exists(self.tickets_path):
            with open(self.tickets_path, "w") as f:
                json.dump([], f)

    def _load_data(self, file_path):
        with open(file_path, "r") as f:
            return json.load(f)

    def _save_data(self, file_path, data):
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    # --- CUSTOMER CRUD OPERATIONS ---
    def create_customer(self, customer_data: dict) -> dict:
        """Adds a brand new enterprise client to the registry."""
        customers = self._load_data(self.customers_path)
        
        # Deduplication and verification safeguard
        for c in customers:
            if c["customer_id"] == customer_data.get("customer_id"):
                raise ValueError(f"Customer ID {c['customer_id']} already exists.")
                
        customers.append(customer_data)
        self._save_data(self.customers_path, customers)
        return customer_data

    def get_customer(self, customer_id: str) -> dict:
        """Retrieves profile info for a specific client ID."""
        customers = self._load_data(self.customers_path)
        for c in customers:
            if c["customer_id"] == customer_id:
                return c
        return None

    # --- TICKET CRUD & LIFECYCLE MANAGEMENT ---
    def create_ticket(self, ticket_data: dict) -> dict:
        """Creates a support ticket initialized to 'Open' status."""
        tickets = self._load_data(self.tickets_path)
        
        ticket_data["status"] = "Open"
        ticket_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        tickets.append(ticket_data)
        self._save_data(self.tickets_path, tickets)
        return ticket_data

    def update_ticket_status(self, ticket_id: str, new_status: str) -> dict:
        """Safeguards and manages ticket transition pipelines."""
        VALID_STATUSES = ["Open", "In Progress", "Escalated", "Resolved", "Closed"]
        if new_status not in VALID_STATUSES:
            raise ValueError(f"Invalid lifecycle state. Must be one of: {VALID_STATUSES}")
            
        tickets = self._load_data(self.tickets_path)
        for t in tickets:
            if t["ticket_id"] == ticket_id:
                t["status"] = new_status
                self._save_data(self.tickets_path, tickets)
                return t
        return None

    # --- PER-CUSTOMER INTEGRATED TIMELINE VIEW ---
    def get_customer_timeline(self, customer_id: str) -> list:
        """Aggregates all ticket interactions for a customer sorted chronologically."""
        tickets = self._load_data(self.tickets_path)
        
        # Filter down to specific client interactions
        customer_tickets = [t for t in tickets if t["customer_id"] == customer_id]
        
        # Sort chronologically (most recent last)
        customer_tickets.sort(key=lambda x: x["created_at"])
        return customer_tickets
