from rich.console import Console
from rich.table import Table


def generate_report(results):
    console = Console()
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Client", style="dim")
    table.add_column("MRR", justify="right")
    table.add_column("Activity", justify="right")
    table.add_column("Risk", justify="right")
    table.add_column("Recommendation", style="bold")

    for r in results:
        risk = r.get("churn_risk", 0)
        color = "green" if risk < 30 else ("yellow" if risk <= 70 else "red")
        table.add_row(
            r["client"],
            f"${r['mrr']:.2f}",
            str(r.get("activity_score", 0)),
            f"{risk}%",
            r["recommendation"],
            style=color
        )
        
    console.print(table)