from rich.table import Table
from rich.console import Console


def print_report(data):
    console = Console()
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Client", style="dim")
    table.add_column("MRR", style="green")
    table.add_column("Activity Score", style="yellow")
    table.add_column("Churn Risk", style="red")
    table.add_column("Recommendation", style="bold")

    for row in data:
        risk = row["churn_risk"]
        style = "green" if risk < 30 else ("yellow" if risk < 70 else "red")
        table.add_row(
            row["client"],
            f"${row['mrr']:.2f}",
            str(row["activity_score"]),
            str(risk),
            row["recommendation"]
        )
    console.print(table)
