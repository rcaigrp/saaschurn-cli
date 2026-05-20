from rich.console import Console
from rich.table import Table

def generate_report(clients):
    console = Console()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Client", style="dim")
    table.add_column("MRR", style="cyan")
    table.add_column("Activity", style="green")
    table.add_column("Risk", style="red")
    table.add_column("Recommendation", style="yellow")

    for client in clients:
        risk = client['churn_risk']
        style = 'green' if risk < 30 else ('yellow' if risk <= 70 else 'red')
        table.add_row(
            client['client'],
            f"${client['mrr']:.2f}",
            str(client['activity_score']),
            style=f"{style} bold",
            style=f"{style} bold"
        )

    console.print(table)
