from rich.console import Console
from rich.table import Table

console = Console()

def generate_report(data):
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Client")
    table.add_column("MRR")
    table.add_column("Activity Score")
    table.add_column("Churn Risk")
    table.add_column("Recommendation")

    for row in data:
        risk = row.get("churn_risk", 0)
        style = "green" if risk < 30 else "yellow" if risk < 70 else "red"
        table.add_row(
            str(row.get("client", "")),
            f"${row.get('mrr', 0):.2f}",
            str(row.get("activity_score", 0)),
            str(risk),
            row.get("recommendation", ""),
            style=style
        )
    console.print(table)
