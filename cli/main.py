import argparse
import sys
import json

def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI")
    parser.add_argument("command", choices=["health"])
    parser.add_argument("--dry-run", action="store_true", help="Run in dry-run mode")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    if args.dry_run:
        print("Dry-run mode enabled. Skipping API calls.")
        return

    from cli.health import run_health_check
    results = run_health_check()

    if args.output == "json":
        print(json.dumps(results))
    else:
        from rich.console import Console
        from rich.table import Table
        console = Console()
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Metric", style="dim", width=15)
        table.add_column("Value", style="bright_cyan")
        for key, value in results.items():
            table.add_row(key, str(value))
        console.print(table)

if __name__ == "__main__":
    main()
