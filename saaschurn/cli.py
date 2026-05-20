import argparse
import json
import sys
from dotenv import load_dotenv
from saaschurn.fetchers import fetch_data
from saaschurn.calculators import calculate_risk
from saaschurn.reporter import generate_report

def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI")
    parser.add_argument("--dry-run", action="store_true", help="Use mock data")
    parser.add_argument("--output", choices=["json"], help="Output format")
    args = parser.parse_args()

    # Env loading
    load_dotenv()
    
    # Fetch
    data = fetch_data(dry_run=args.dry_run)
    
    # Calc
    results = calculate_risk(data)
    
    # Report
    if args.output == "json":
        print(json.dumps(results, indent=2))
    else:
        generate_report(results)

if __name__ == "__main__":
    main()
