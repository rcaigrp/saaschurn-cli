from rich.console import Console
from rich.table import Table

console = Console()

def print_report(risk_data):
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Client")
    table.add_column("MRR ($)")
    table.add_column("Activity")
    table.add_column("Risk Level")
    table.add_column("Score")
    table.add_column("Recommendation")

    for client, data in risk_data.items():
        level = data["level"]
        color = "green" if level == "LOW" else "yellow" if level == "MEDIUM" else "red"
        table.add_row(
            client,
            f"{data['mrr']:.2f}",
            str(data['activity']),
            f"[{color}]{level}[/{color}]",
            str(data['score']),
            data['recommendation']
        )
    console.print(table)
