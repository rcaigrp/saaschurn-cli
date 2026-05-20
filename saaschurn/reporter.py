from rich.table import Table
from rich.console import Console
from typing import List, Dict

console = Console()


def generate_report(data: List[Dict]) -> str:
    """Generate a rich terminal table with churn data."""
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Client", style="dim")
    table.add_column("MRR", justify="right")
    table.add_column("Activity", justify="right")
    table.add_column("Risk", justify="right")
    table.add_column("Recommendation", style="bold")

    for row in data:
        risk = row.get("risk_level", "MEDIUM")
        if risk == "HIGH":
            style = "red"
        elif risk == "MEDIUM":
            style = "yellow"
        else:
            style = "green"

        table.add_row(
            row["client"],
            f"${row['mrr']:.2f}",
            str(row["activity_score"]),
            risk,
            row["recommendation"],
            style=style
        )

    console.print(table)
    return console.output
