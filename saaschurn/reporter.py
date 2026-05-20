from typing import List
from rich.console import Console
from rich.table import Table

console = Console()


def print_report(report: List[dict]):
    """Print formatted churn report using rich tables.
    
    Args:
        report: List of churn report data.
    """
    table = Table(title="SaaS Churn Risk Report")
    table.add_column("Client", style="cyan")
    table.add_column("MRR", style="green")
    table.add_column("Activity Score", style="yellow")
    table.add_column("Churn Risk", style="red")
    table.add_column("Recommendation", style="magenta")
    
    for entry in report:
        risk_level = entry.get("risk_level", "")
        risk_score = entry.get("churn_risk", 0)
        
        # Color-code rows by risk level
        if risk_level == "LOW":
            style = "green"
        elif risk_level == "MEDIUM":
            style = "yellow"
        else:
            style = "red"
        
        table.add_row(
            entry.get("client", ""),
            f"${entry.get('mrr', 0):,.2f}",
            f"{entry.get('activity_score', 0):.1f} msgs/day",
            f"{risk_score}/100",
            entry.get("recommendation", "")
        )
    
    console.print(table)
