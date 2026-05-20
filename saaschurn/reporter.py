from rich.console import Console
from rich.table import Table


def generate_report(results):
    console = Console()
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Client", style="dim")
    table.add_column("MRR", style="green")
    table.add_column("Activity", style="yellow")
    table.add_column("Churn Risk", style="red")
    table.add_column("Recommendation")
    
    for r in results:
        table.add_row(
            r['client'],
            f"${r['mrr']}",
            str(r['activity_score']),
            str(r['churn_risk']),
            r['recommendation']
        )
    console.print(table)
