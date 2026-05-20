from rich.console import Console
from rich.table import Table

class Reporter:
    def __init__(self):
        self.console = Console()

    def print_table(self, results):
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Client")
        table.add_column("MRR")
        table.add_column("Activity Score")
        table.add_column("Churn Risk")
        table.add_column("Recommendation")

        for res in results:
            risk_style = "green" if res.risk_score < 30 else "yellow" if res.risk_score <= 70 else "red"
            table.add_row(
                res.client_name,
                str(res.mrr),
                str(res.activity_score),
                res.recommendation,
                style=risk_style
            )
        self.console.print(table)
