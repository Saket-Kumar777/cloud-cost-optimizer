from .llm_client import generate_json
from .utils import load_json, save_json

def analyze_costs():
    """
    Analyzes the billing data against the budget and generates recommendations.
    """
    
    # Load previous steps
    profile = load_json("project_profile.json")
    billing = load_json("mock_billing.json")

    if not profile or not billing:
        print("Error: Missing profile or billing data. Run previous steps first.")
        return None

    # Calculate current totals for context
    total_cost = sum(item['cost_inr'] for item in billing)
    budget = profile.get('budget_inr_per_month', 0)
    
    prompt = f"""
    Act as a Cloud FinOps expert. Analyze the following project costs and recommend optimizations.
    
    PROJECT CONTEXT:
    - Name: {profile.get('name')}
    - Budget: {budget} INR
    - Actual Spend: {total_cost} INR
    - Tech Stack: {profile.get('tech_stack')}
    
    BILLING RECORDS:
    {billing}
    
    TASK:
    1. Analyze the spending.
    2. Provide 5-8 actionable recommendations to save money (e.g., use Spot instances, switch to Open Source, Right-sizing).
    3. Suggest specific multi-cloud alternatives (AWS, Azure, GCP).
    
    REQUIRED JSON FORMAT:
    {{
        "project_name": "{profile.get('name')}",
        "analysis": {{
            "total_monthly_cost": {total_cost},
            "budget": {budget},
            "budget_variance": {total_cost - budget},
            "is_over_budget": {str(total_cost > budget).lower()},
            "service_costs": {{ "Service Name": 1234, ... }}
        }},
        "recommendations": [
            {{
                "title": "Short title",
                "service": "Service involved (e.g. EC2)",
                "current_cost": 100,
                "potential_savings": 50,
                "recommendation_type": "open_source_alternative / right_sizing / etc",
                "description": "Explanation of what to do",
                "cloud_providers": ["AWS", "Azure", "GCP"]
            }}
        ]
    }}
    """

    print("Analyzing costs and generating recommendations...")
    report = generate_json(prompt, max_tokens=3000)

    if report:
        save_json("cost_optimization_report.json", report)
        return report
    else:
        print("Failed to generate report.")
        return None