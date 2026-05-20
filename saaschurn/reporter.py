from rich.table import Table
from rich.console import Console

class Reporter:
    def __init__(self):
        self.console = Console()

    def print_report(self, data, json_output=False):
        if json_output:
            import json
            print(json.dumps(data))
        else:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Client", style="dim")
            table.add_column("MRR", style="green")
            table.add_column("Activity", style="cyan")
            table.add_column("Risk", style="red")
            table.add_column("Recommendation")
            
            for item in data:
                risk = item.get("risk_score", 0)
                color = "red" if risk > 70 else ("yellow" if risk > 30 else "green")
                table.add_row(
                    item.get("client", "N/A"),
                    f"${item.get('mrr', 0)}",
                    str(item.get("activity", 0)),
                    str(risk),
                    item.get("recommendation", "N/A")
                )
            self.console.print(table)
