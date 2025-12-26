from .llm_client import generate_json
from .utils import load_json, save_json

def generate_mock_billing(profile_data=None):
    """
    Generates synthetic cloud billing data based on the project profile.
    """
    
    # Load profile if not provided
    if not profile_data:
        profile_data = load_json("project_profile.json")
        if not profile_data:
            print("Error: No profile found. Run step 1 first.")
            return None

    project_name = profile_data.get("name", "Project")
    budget = profile_data.get("budget_inr_per_month", 5000)
    tech_stack = profile_data.get("tech_stack", {})

    prompt = f"""
    Generate realistic synthetic cloud billing data for a project named "{project_name}".
    
    CONTEXT:
    - Budget: {budget} INR/month
    - Tech Stack: {tech_stack}
    
    TASK:
    Create a list of 12-20 billing records for the current month.
    Include a mix of compute, database, storage, and networking costs.
    Ensure the total cost is close to the budget (slightly over or under is okay).
    
    REQUIRED JSON FORMAT (Array of Objects):
    [
        {{
            "month": "2025-01",
            "service": "Service Name (e.g., EC2, RDS, CloudStorage)",
            "resource_id": "unique-id-123",
            "usage_type": "description of usage",
            "usage_quantity": (number),
            "unit": "hours/GB/requests",
            "cost_inr": (number),
            "desc": "Short description of what this charge is for"
        }},
        ... more records
    ]
    """

    print("Generating mock billing data...")
    billing_data = generate_json(prompt, max_tokens=2500)

    if billing_data:
        save_json("mock_billing.json", billing_data)
        return billing_data
    else:
        print("Failed to generate billing data.")
        return None