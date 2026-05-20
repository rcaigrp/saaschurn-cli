from rich.console import Console
from rich.table import Table

def generate_report(data):
    console = Console()
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Client", style="dim")
    table.add_column("MRR ($)", style="bright_blue")
    table.add_column("Activity Score", style="bright_yellow")
    table.add_column("Churn Risk", style="bright_magenta")
    table.add_column("Risk Level", style="bold")
    table.add_column("Recommendation", style="green")
    
    for row in data:
        risk_color = "green" if row['risk_level'] == 'LOW' else ("yellow" if row['risk_level'] == 'MEDIUM' else "red")
        table.add_row(
            str(row['client']),
            f"{row['mrr']:.2f}",
            str(row['activity_score']),
            str(row['churn_risk']),
            row['risk_level'],
            row['recommendation']
        )
    console.print(table)
