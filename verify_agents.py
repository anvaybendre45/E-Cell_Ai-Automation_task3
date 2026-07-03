# C:\AI_CRM_project\verify_agents.py
from src.agents import AIIntelligenceLayer
from src.memory import CustomerInteractionMemory

ai_layer = AIIntelligenceLayer()
memory = CustomerInteractionMemory()

print("--- Testing Module 2: AI Intelligence & Routing Layer ---")

# 1. Test Persistent Memory
memory.save_interaction(
    customer_id="CUST-053",
    human_msg="Hey, our automated webhook events are dropping completely.",
    ai_msg="Checking server clusters now.",
    summary_update="Customer is highly technical, uses advanced webhook routing profiles."
)
loaded_mem = memory.get_context("CUST-053")
print(f"\n[1/3] Memory Long-Term Layer Saved: {loaded_mem['long_term_preferences']}")

# 2. Test Ticket Summarization Execution
mock_history = "[10:00 AM] Customer: Payment went through twice but my tier didn't upgrade. [10:02 AM] Agent: Checking the billing logs."
summary = ai_layer.summarize_ticket(mock_history)
print(f"\n[2/3] Extraction Summary Output:")
print(f"      Key Issue: {summary.get('key_issues')}")
print(f"      Urgency: {summary.get('urgency')}")

# 3. Test LangGraph Workflow Routing Execution
next_state = ai_layer.route_workflow_state(ticket_category="Billing", urgency=summary.get("urgency", "High"))
print(f"\n[3/3] Workflow State Router Transition Destination: {next_state}")