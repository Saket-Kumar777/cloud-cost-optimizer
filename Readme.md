<!-- AI-Powered Cloud Cost Optimizer (LLM-Driven) -->

# AI-Powered Cloud Cost Optimizer (LLM-Driven)

This Python CLI toolkit simulates cloud billing, extracts structured project profiles from plain-English descriptions, and produces actionable cost-optimization recommendations using an LLM-assisted pipeline. It's designed to be deterministic where it matters (parsing, validation, report format) and to leverage LLMs for profile extraction and realistic billing synthesis.

## Key Features

- **AI-Driven Profile Extraction**: Uses `meta-llama/Llama-3.1-8B-Instruct` (via the Hugging Face API) to interpret natural language project descriptions and generate a structured `project_profile.json`.
- **Realistic Billing Simulation**: Generates 12–20 realistic billing line items tailored to the project's tech stack and budget (supports AWS/Azure/GCP semantics; defaults to AWS when unspecified).
- **Cost Optimization Engine**: Analyzes billing records and produces 6–10 prioritized, actionable recommendations (rightsizing, spot/low-cost options, storage tiering, monitoring cost reductions).
- **Strict Output Constraints**: Enforces deterministic formatting and numeric validation for `mock_billing.json` and `cost_optimization_report.json` so downstream tools can parse reliably.
- **Robust Fallbacks**: Local mock models and deterministic generators are used if the Hugging Face API is unavailable or times out.

---

## Installation & Setup

### 1. Prerequisites

- Python 3.10+
- A Hugging Face API token (create one at https://huggingface.co/settings/tokens)

### 2. Install dependencies

```bash
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install the essentials:

```bash
pip install requests python-dotenv
```

### 3. Configure API Key
Create a `.env` file in the project root with your HF token:

```env
HF_API_KEY=hf_your_actual_api_key_here
HF_MODEL=meta-llama/Llama-3.1-8B-Instruct
```

### 4. Run the Tool

```bash
python main.py
```

By default `main.py` will read `data/project_description.txt` (if present) or prompt for a description, then produce `data/project_profile.json`, `data/mock_billing.json`, and `data/cost_optimization_report.json`.

---

## Example Walkthrough

The following example demonstrates the input → profile → billing → recommendations flow.

### Step 1: User Input

Example input provided to the CLI or `data/project_description.txt`:

> "We are building a food delivery app for 10,000 users per month. Budget: ₹50,000 per month. Tech stack: Node.js backend, PostgreSQL database, object storage for images, monitoring, and basic analytics. Non-functional requirements: scalability, cost efficiency, uptime monitoring."

---

### Step 2: Generated Profile (`data/project_profile.json`)

The LLM-backed extractor normalizes the description into structured JSON, for example:

```json
{
  "name": "Food Delivery App",
  "budget_inr_per_month": 50000,
  "description": "We are building a food delivery app for 10,000 users per month",
  "tech_stack": {
    "backend": "Node.js",
    "database": "PostgreSQL",
    "storage": "object storage",
    "monitoring": "CloudWatch/Cloud-native",
    "analytics": "basic analytics"
  },
  "non_functional_requirements": [
    "Uptime Monitoring",
    "Scalability",
    "Cost Efficiency"
  ]
}
```

---

### Step 3: Mock Billing Data (`data/mock_billing.json`)

The billing simulator produces 12–20 line items matching the profile and budget. Example snippet:

```json
[
  {
    "month": "2025-09",
    "service": "RDS",
    "resource_id": "db-prod-replica-01",
    "region": "ap-south-1",
    "usage_type": "PostgreSQL (provisioned)",
    "usage_quantity": 720,
    "unit": "hours",
    "cost_inr": 38497,
    "desc": "Production database replica"
  },
  {
    "month": "2025-09",
    "service": "S3",
    "resource_id": "bucket-food-delivery-prod",
    "region": "ap-south-1",
    "usage_type": "Standard Storage",
    "usage_quantity": 100,
    "unit": "GB",
    "cost_inr": 1069,
    "desc": "Production bucket for food delivery app"
  }
]
```

All items are validated for numeric types and totals before the analyzer runs.

---

### Step 4: Optimization Report (`data/cost_optimization_report.json`)

The analyzer summarizes costs and returns 6–10 prioritized recommendations. Example:

```json
{
  "project_name": "Food Delivery App",
  "analysis": {
    "total_monthly_cost": 49902.25,
    "budget": 50000,
    "budget_variance": -97.75,
    "service_costs": {
      "RDS": 41339.0,
      "S3": 1502.0,
      "CloudWatch": 3448.5,
      "EC2": 1382.75,
      "EBS": 2230.0
    },
    "high_cost_services": ["RDS", "CloudWatch", "EBS"],
    "is_over_budget": false
  },
  "recommendations": [
    {
      "title": "Migrate to PostgreSQL Free Tier",
      "service": "RDS",
      "current_cost": 41339,
      "potential_savings": 8226,
      "recommendation_type": "free_tier",
      "description": "Migrate development and staging databases to free-tier offerings where feasible.",
      "implementation_effort": "medium",
      "risk_level": "medium",
      "steps": [
        "Assess RDS usage and identify non-production instances",
        "Export and import schema into free-tier-compatible instances",
        "Reconfigure backups and monitoring for free tier"
      ],
      "cloud_providers": ["AWS", "Azure", "GCP"]
    }
  ]
}
```

---

## Project Structure (this repo)

| File | Description |
| :--- | :--- |
| `main.py` | CLI orchestrator and entrypoint. |
| `requirements.txt` | Python dependencies; used by the quick start. |
| `data/` | Inputs and outputs (`project_description.txt`, `project_profile.json`, `mock_billing.json`, `cost_optimization_report.json`). |
| `src/billing_generator.py` | Generates synthetic billing line items from a `project_profile`. |
| `src/cost_analyzer.py` | Validates billing, computes totals, and produces optimization recommendations. |
| `src/llm_client.py` | Hugging Face API wrapper and fallback mocks. |
| `src/profile_extractor.py` | LLM-backed text -> structured profile extractor. |
| `src/utils.py` | Helpers: validation, currency conversion, and file I/O. |

---

## AI Usage Declaration

This project uses LLMs to assist with profile extraction and synthetic data generation. Core validation, numeric calculations, constraint enforcement, and final report formatting are implemented in deterministic Python code so results remain reproducible and auditable. If Hugging Face API access is unavailable, the repository provides deterministic mock generators to maintain functionality.


