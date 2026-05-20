from rich.table import Table
from rich.console import Console


class Reporter:
    def __init__(self):
        self.console = Console()

    def print_table(self, data):
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Client")
        table.add_column("MRR")
        table.add_column("Activity Score")
        table.add_column("Churn Risk")
        table.add_column("Recommendation")
        for row in data:
            risk = row["risk"]
            color = "green" if risk < 30 else "yellow" if risk < 70 else "red"
            table.add_row(
                row["client"],
                f"${row['mrr']:.2f}",
                str(row["activity"]),
                str(risk),
                row["recommendation"],
                style=color,
            )
        self.console.print(table)