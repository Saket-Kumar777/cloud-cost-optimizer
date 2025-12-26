from .llm_client import generate_json
from .utils import save_json, save_text

def create_profile(user_description):
    """
    Takes a plain text description and converts it into a structured JSON profile.
    """
    
    # 1. Save the raw input first (as per requirements)
    save_text("project_description.txt", user_description)

    # 2. Prepare the prompt for the LLM
    prompt = f"""
    Analyze the following project description and extract the details into a JSON object.
    
    USER DESCRIPTION:
    "{user_description}"
    
    REQUIRED JSON STRUCTURE:
    {{
        "name": "Generate a short, professional project name",
        "budget_inr_per_month": (integer) extract budget or estimate a realistic one if missing,
        "description": "Summarize the user's description professionally",
        "tech_stack": {{
            "frontend": "e.g., React",
            "backend": "e.g., Node.js",
            "database": "e.g., MongoDB",
            "hosting": "e.g., AWS",
            "other": "Any other tools mentioned"
        }},
        "non_functional_requirements": ["list", "of", "requirements", "like", "security", "scalability"]
    }}
    
    If specific details (like budget or tech stack) are missing, infer reasonable defaults based on the project type.
    """

    # 3. Call the AI
    print("Generating project profile...")
    profile_data = generate_json(prompt)

    if profile_data:
        # 4. Save the result
        save_json("project_profile.json", profile_data)
        return profile_data
    else:
        print("Failed to generate profile.")
        return None