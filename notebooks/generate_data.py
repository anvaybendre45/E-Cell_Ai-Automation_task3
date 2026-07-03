# C:\AI_CRM_project\notebooks\generate_data.py
import os
import json
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Step 1: Force load the environment configuration via absolute disk path
dotenv_path = "C:\\AI_CRM_project\\.env"
load_dotenv(dotenv_path=dotenv_path)

# Step 2: Extract key details and initialize the Google GenAI Engine safely
llm_strategy = os.getenv("LLM_STRATEGY", "OPTION_B")
api_key_val = os.getenv("GEMINI_API_KEY")
client = None

if llm_strategy == "OPTION_B":
    try:
        from google import genai
        # If key exists and is not the default placeholder text, instantiate client
        if api_key_val and "your_actual_gemini" not in api_key_val.lower() and "placeholder" not in api_key_val.lower():
            client = genai.Client(api_key=api_key_val)
            print("[INFO] Google Gemini client initialized successfully with API key.")
        else:
            print("[WARNING] Valid GEMINI_API_KEY not detected in .env file. Running in fallback mode.")
    except ImportError:
        print("[ERROR] 'google-genai' library missing. Run: pip install google-genai")

# System Domain Configurations
INDUSTRIES = ["SaaS", "Fintech", "Healthcare", "E-commerce", "Logistics"]
TIERS = ["Growth", "Enterprise", "Startup"]
TICKET_CATEGORIES = ["Billing", "Technical Bug", "Onboarding", "Feature Request", "Account Access"]
STATUSES = ["Open", "In Progress", "Escalated", "Resolved", "Closed"]

def generate_customer_registry(count=500):
    """Generates 500 structured synthetic customer profiles"""
    customers = []
    start_date = datetime.now() - timedelta(days=180)
    
    print(f"\nGenerating {count} customer records...")
    for i in range(1, count + 1):
        industry = random.choice(INDUSTRIES)
        tier = random.choice(TIERS)
        acq_offset = random.randint(0, 150)
        created_at = start_date + timedelta(days=acq_offset)
        
        customer = {
            "customer_id": f"CUST-{i:03d}",
            "name": f"Enterprise Partner {i}",
            "industry": industry,
            "product_tier": tier,
            "tenure_months": random.randint(1, 24),
            "engagement_score": round(random.uniform(2.0, 10.0), 1),
            "acquisition_date": created_at.strftime("%Y-%m-%d"),
            "is_churned": random.choices([True, False], weights=[0.15, 0.85])[0]
        }
        customers.append(customer)
    return customers

def mock_llm_ticket_text(category, industry):
    """High-speed local text backup engine to bypass network latency or rate-limiting constraints"""
    issues = {
        "Billing": "Discrepancy spotted in monthly platform usage invoices vs API rate limit quotas.",
        "Technical Bug": "Webhook payloads failing intermittently with standard 504 gateway timeout loops.",
        "Onboarding": "Unable to sync OAuth internal team data permissions during main dashboard setup configuration.",
        "Feature Request": "Requesting advanced role-based column masking configuration filters for security compliance.",
        "Account Access": "Admin system user locked out following multi-factor authentication reset security sync."
    }
    return f"Customer from {industry} division reported a {category} issue: {issues[category]}"

def generate_llm_ticket_details(category, industry):
    """Calls the live Gemini API engine to generate organic customer dialogue text records"""
    if client is None:
        return mock_llm_ticket_text(category, industry)
        
    prompt = f"""
    Generate a concise conversation transcript for an enterprise B2B software CRM support ticket system logs.
    Customer Industry Segment: {industry}
    Ticket Classification Category: {category}
    
    Format output precisely matching this layout:
    [Timestamp] Customer: <concise ticket complaint context>
    [Timestamp] Support Agent: <diagnostic actions and updates>
    """
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        # Automatically defaults to local mock if API drops due to throttling/network hiccups
        return mock_llm_ticket_text(category, industry)

def generate_ticket_dataset(customers, total_tickets=1000):
    """Generates 1,000 relational operational records mapped across your base client IDs"""
    tickets = []
    start_date = datetime.now() - timedelta(days=180)
    
    print(f"Generating {total_tickets} relational support tickets across historical timeframe...")
    for i in range(1, total_tickets + 1):
        customer = random.choice(customers)
        category = random.choice(TICKET_CATEGORIES)
        status = random.choice(STATUSES)
        
        day_offset = random.randint(0, 180)
        created_at = start_date + timedelta(days=day_offset)
        
        # We process the first 25 records through the live LLM for real interactive variations.
        # The remainder uses the mock layout to bypass API rate caps.
        if i <= 25:
            interaction_log = generate_llm_ticket_details(category, customer["industry"])
        else:
            interaction_log = mock_llm_ticket_text(category, customer["industry"])
            
        ticket = {
            "ticket_id": f"TCK-{i:04d}",
            "customer_id": customer["customer_id"],
            "category": category,
            "status": status,
            "priority": random.choice(["Low", "Medium", "High", "Critical"]),
            "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "interaction_history": interaction_log
        }
        tickets.append(ticket)
        if i % 200 == 0:
            print(f"  -> Successfully generated {i}/{total_tickets} ticket rows...")
            
    return tickets

def save_data():
    target_dir = "C:\\AI_CRM_project\\data"
    os.makedirs(target_dir, exist_ok=True)
    
    # 1. Process Customers
    customers = generate_customer_registry(500)
    cust_path = os.path.join(target_dir, "customers.json")
    with open(cust_path, "w") as f:
        json.dump(customers, f, indent=4)
    print(f"[SUCCESS] Dropped 500 records to: {cust_path}")
    
    # 2. Process Tickets
    tickets = generate_ticket_dataset(customers, 1000)
    tck_path = os.path.join(target_dir, "tickets.json")
    with open(tck_path, "w") as f:
        json.dump(tickets, f, indent=4)
    print(f"[SUCCESS] Dropped 1,000 records to: {tck_path}")

if __name__ == "__main__":
    save_data()