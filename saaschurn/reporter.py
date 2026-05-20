from rich.console import Console
from rich.table import Table

console = Console()

def generate_report(clients_data):
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Client", style="dim")
    table.add_column("MRR", style="green")
    table.add_column("Activity", style="yellow")
    table.add_column("Risk", style="red")
    table.add_column("Recommendation", style="blue")

    for client, data in clients_data.items():
        mrr = data["mrr"]
        activity = data["activity"]
        risk = data["risk"]
        risk_level = data["risk_level"]
        rec = data["recommendation"]
        table.add_row(
            client,
            f"${mrr:.2f}",
            str(activity),
            risk_level,
            rec
        )
    console.print(table)
