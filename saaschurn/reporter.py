from rich.console import Console
from rich.table import Table

def generate_report(results):
    console = Console()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Client")
    table.add_column("MRR")
    table.add_column("Activity")
    table.add_column("Risk")
    table.add_column("Recommendation")

    for client in results:
        color = "green" if client["risk_level"] == "LOW" else ("yellow" if client["risk_level"] == "MEDIUM" else "red")
        table.add_row(
            client["client"],
            f"${client['mrr']:.2f}",
            client["activity"],
            f"{client['risk_score']} ({client['risk_level']})",
            f"[{color}] {client['recommendation']}[/]"
        )
    console.print(table)