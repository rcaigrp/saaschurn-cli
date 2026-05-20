from rich.console import Console
from rich.table import Table

def generate_report(data):
    console = Console()
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Client", style="dim")
    table.add_column("MRR")
    table.add_column("Churn Risk")
    
    for client, info in data.items():
        risk = info.get('risk_score', 0)
        color = "green" if risk < 30 else ("yellow" if risk < 70 else "red")
        table.add_row(client, f"${info.get('mrr', 0):.2f}", f"{risk}", style=color)
    console.print(table)
