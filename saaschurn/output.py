import json
import sys
from rich.table import Table
from rich.console import Console

console = Console()

def print_table(data):
    console.print("[bold]SaaS Churn Report[/bold]")
    console.print(f"MRR: ${data.get('mrr', 0)}")
    console.print(f"Churn Score: {data.get('churn_score', 0)}")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="dim", width=15)
    table.add_column("Value", style="bold cyan")
    table.add_row("Subscriptions", str(len(data.get('subscriptions', []))))
    table.add_row("Activity Logs", str(len(data.get('activity', []))))
    console.print(table)

def export_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, default=str)
