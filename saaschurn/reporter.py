from rich.console import Console
from rich.table import Table

console = Console()

def generate_report(results):
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Client", style="dim")
    table.add_column("MRR", style="green")
    table.add_column("Activity", style="cyan")
    table.add_column("Risk", style="yellow")
    table.add_column("Rec", style="bold")
    
    for client in results:
        risk = client.get('risk', 0)
        style = "green" if risk < 30 else "yellow" if risk <= 70 else "red"
        table.add_row(
            str(client.get('client')),
            f"${client.get('mrr'):.2f}",
            str(client.get('activity')),
            str(risk),
            client.get('recommendation', 'Monitor')
        )
    console.print(table)