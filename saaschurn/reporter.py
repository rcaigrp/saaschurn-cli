from rich.console import Console
from rich.table import Table

console = Console()

def format_report(results):
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Client", style="cyan")
    table.add_column("MRR", style="green")
    table.add_column("Activity", style="yellow")
    table.add_column("Risk", style="red")
    table.add_column("Recommendation", style="blue")
    for r in results:
        risk = r["risk"]
        color = "green" if risk < 30 else ("yellow" if risk <= 70 else "red")
        table.add_row(
            r["client"],
            f"${r['mrr']:.2f}",
            f"{r['activity']}/day",
            str(r["risk"]),
            r["recommendation"],
            style=color
        )
    console.print(table)
