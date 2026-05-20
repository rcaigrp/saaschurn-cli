from rich.console import Console
from rich.table import Table

console = Console()

def print_report(results):
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Client")
    table.add_column("MRR")
    table.add_column("Activity Score")
    table.add_column("Churn Risk")
    table.add_column("Recommendation")

    for r in results:
        risk = r.get("churn_risk", 0)
        rec = "Review"
        if risk > 70:
            rec = "High Churn Risk"
        elif risk > 30:
            rec = "Monitor"
        else:
            rec = "Healthy"
        
        color = "green" if risk <= 30 else ("yellow" if risk <= 70 else "red")
        console.print(f"[{color}]{r.get('client')}[/]") # Just for demo
        table.add_row(
            r.get("client", "N/A"),
            f"${r.get('mrr', 0):.2f}",
            str(r.get("activity_score", 0)),
            str(r.get("churn_risk", 0)),
            rec
        )
    console.print(table)
