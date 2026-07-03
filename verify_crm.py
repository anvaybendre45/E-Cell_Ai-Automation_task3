# C:\AI_CRM_project\verify_crm.py
import json
from src.crm import CRMEngine

crm = CRMEngine()

print("--- Testing Core CRM Engine Module ---")

# Load tickets to find an active customer ID quickly
with open("C:\\AI_CRM_project\\data\\tickets.json", "r") as f:
    tickets_data = json.load(f)

if not tickets_data:
    print("[ERROR] No tickets found in tickets.json! Please rerun the generator.")
else:
    # Grab the customer ID from the very first ticket row
    active_cust_id = tickets_data[0]["customer_id"]
    active_ticket_id = tickets_data[0]["ticket_id"]
    
    # 1. Load Profile
    sample_customer = crm.get_customer(active_cust_id)
    print(f"\n[1/3] Loaded Profile: {sample_customer['name']} ({active_cust_id})")
    print(f"      Industry: {sample_customer['industry']} | Tier: {sample_customer['product_tier']}")
    
    # 2. Extract Timeline
    timeline = crm.get_customer_timeline(active_cust_id)
    print(f"\n[2/3] Total tickets logged for {active_cust_id}: {len(timeline)}")
    
    # 3. Test Lifecycle Transitions (Open -> In Progress)
    print(f"\n[3/3] Target Ticket Found: {active_ticket_id}")
    print(f"      Current Lifecycle State: {tickets_data[0]['status']}")
    
    updated = crm.update_ticket_status(active_ticket_id, "In Progress")
    print(f"      Updated Lifecycle State: {updated['status']} << State Transition Confirmed!")