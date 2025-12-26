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

The tool launches an interactive CLI menu with four options:
1. **Enter New Project Description** — Input a plain-English project description (e.g., tech stack, budget, requirements).
2. **Run Full Cost Analysis** — Generate profile → billing → recommendations automatically.
3. **View Recommendations** — Display the optimization report and top savings opportunities.
4. **Exit** — Close the tool.

**Note on Special Characters**: Use UTF-8 encoding when entering descriptions with currency symbols (₹, €, etc.). The tool will save results to `data/project_profile.json`, `data/mock_billing.json`, and `data/cost_optimization_report.json`.

---

## Interactive CLI Walkthrough

The following example demonstrates the full interactive menu-driven flow.

### Step 1: Launch & Select Option 1

```
==================================================
   AI-POWERED CLOUD COST OPTIMIZER
==================================================

1. Enter New Project Description
2. Run Full Cost Analysis (Profile -> Billing -> Report)
3. View Recommendations
4. Exit

Select an option (1-4): 1
```

**Enter your project description:**

> "We are building a food delivery app for 10,000 users per month. Budget: ₹50,000 per month. Tech stack: Node.js backend, PostgreSQL database, object storage for images, monitoring, and basic analytics. Non-functional requirements: scalability, cost efficiency, uptime monitoring."

**Output:**
```
Generating project profile...
⏳ Asking AI (meta-llama/Llama-3.1-8B-Instruct)...
Saved: project_profile.json

Profile created successfully!
```

---

### Step 2: Generated Profile (`data/project_profile.json`)

The LLM-backed extractor normalizes the description into structured JSON. The generated profile is then saved and the menu returns for the next step.

### Step 3: Run Full Analysis (Option 2)

Select **Option 2** from the menu to run the complete pipeline:

```
Starting Full Analysis Pipeline...
Step 2: Generating Synthetic Billing Data...
Generating mock billing data...
⏳ Asking AI (meta-llama/Llama-3.1-8B-Instruct)...
Saved: mock_billing.json

Step 3: Analyzing Costs & Recommendations...
Analyzing costs and generating recommendations...
⏳ Asking AI (meta-llama/Llama-3.1-8B-Instruct)...
Saved: cost_optimization_report.json

Analysis Complete! Check 'data/cost_optimization_report.json'
```

The `mock_billing.json` contains 12–20 realistic line items tailored to the tech stack and budget. The `cost_optimization_report.json` contains the full analysis with cost breakdowns and actionable recommendations.

### Step 4: View Recommendations (Option 3)

Select **Option 3** to display the final optimization report:

```
--- OPTIMIZATION REPORT ---
Project: Food Delivery App
Total Cost: 16500
Budget: 50000

Top Recommendations:
1. Use Spot Instances for EC2 (Save 500)
2. Switch to Open Source Database (Save 500)
3. Optimize CloudStorage Usage (Save 1000)
4. Use CloudWatch Free Tier (Save 1000)
5. Use Route 53 Alias Records (Save 200)
6. Use API Gateway REST API (Save 1000)
7. Use Lambda Function Concurrency (Save 500)
8. Use S3 Transfer Acceleration (Save 200)
```

Each recommendation includes the service, savings amount, and quick implementation insight. The full detailed report is available in `data/cost_optimization_report.json` for further analysis.

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


