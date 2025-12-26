import sys
import os

# Ensure we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.profile_extractor import create_profile
from src.billing_generator import generate_mock_billing
from src.cost_analyzer import analyze_costs
from src.utils import load_json

def print_header():
    print("\n" + "="*50)
    print("   AI-POWERED CLOUD COST OPTIMIZER")
    print("="*50 + "\n")

def menu():
    while True:
        print_header()
        print("1. Enter New Project Description")
        print("2. Run Full Cost Analysis (Profile -> Billing -> Report)")
        print("3. View Recommendations")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == '1':
            desc = input("\nEnter your project description:\n> ")
            if desc:
                create_profile(desc)
                print("\nProfile created successfully!")
            
        elif choice == '2':
            # Check if description exists, if not ask for it
            if not os.path.exists("data/project_description.txt"):
                print("\nNo project description found.")
                desc = input("Enter your project description:\n> ")
                create_profile(desc)

            print("\nStarting Full Analysis Pipeline...")
            
            # Step 1: Ensure Profile exists (it should by now)
            if not os.path.exists("data/project_profile.json"):
                print("Step 1: Generating Profile...")
                create_profile(load_json("project_description.txt"))
            
            # Step 2: Generate Billing
            print("Step 2: Generating Synthetic Billing Data...")
            generate_mock_billing()
            
            # Step 3: Analyze
            print("Step 3: Analyzing Costs & Recommendations...")
            analyze_costs()
            
            print("\nAnalysis Complete! Check 'data/cost_optimization_report.json'")

        elif choice == '3':
            report = load_json("cost_optimization_report.json")
            if report:
                print("\n--- OPTIMIZATION REPORT ---")
                print(f"Project: {report.get('project_name')}")
                print(f"Total Cost: {report['analysis']['total_monthly_cost']}")
                print(f"Budget: {report['analysis']['budget']}")
                print("\nTop Recommendations:")
                for i, rec in enumerate(report.get('recommendations', []), 1):
                    print(f"{i}. {rec['title']} (Save {rec.get('potential_savings', 0)})")
            else:
                print("\nNo report found. Run Option 2 first.")

        elif choice == '4':
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid option, please try again.")
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    menu()