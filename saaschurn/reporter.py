import json
from rich.console import Console
from rich.table import Table

console = Console()

def print_table(data):
    """Print formatted rich table with churn risk data."""
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Client", style="dim")
    table.add_column("MRR", style="yellow")
    table.add_column("Activity Score", style="green")
    table.add_column("Churn Risk", style="red")
    table.add_column("Recommendation", style="bright_blue")
    for row in data:
        color = "green" if row["level"] == "LOW" else "yellow" if row["level"] == "MEDIUM" else "red"
        table.add_row(
            row["client"],
            f"${row['mrr']:.2f}",
            str(row["activity"]),
            f"{row['score']}",
            row["recommendation"]
        )
    console.print(table)

def export_json(data):
    """Export results as JSON to stdout."""
    print(json.dumps(data, indent=2))
