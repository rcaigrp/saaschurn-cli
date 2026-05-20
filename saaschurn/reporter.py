"""Rich terminal report generation."""

from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich.text import Text


class Reporter:
    """Generates formatted terminal reports."""

    def __init__(self):
        self.console = Console()

    def generate_report(self, results: List[Dict]) -> str:
        """Generate a rich table report of churn analysis results."""
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Client", style="white")
        table.add_column("MRR", justify="right", style="yellow")
        table.add_column("Activity", justify="right", style="green")
        table.add_column("Risk Score", justify="right", style="magenta")
        table.add_column("Risk Level", style="bold")
        table.add_column("Recommendation", style="dim")

        for result in results:
            risk_level = result.get("risk_level", "MEDIUM")

            # Color coding based on risk level
            if risk_level == "LOW":
                risk_style = "green bold"
            elif risk_level == "MEDIUM":
                risk_style = "yellow bold"
            else:
                risk_style = "red bold"

            table.add_row(
                result.get("client", "Unknown"),
                f"${result.get('mrr', 0):.2f}",
                f"{result.get('activity_score', 0):.1f}",
                f"{result.get('score', 0):.1f}",
                Text(risk_level, style=risk_style),
                result.get("recommendation", "")
            )

        return self.console.export_table(table)

    def print_table(self, results: List[Dict]):
        """Print the table to console."""
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Client", style="white")
        table.add_column("MRR", justify="right", style="yellow")
        table.add_column("Activity", justify="right", style="green")
        table.add_column("Risk Score", justify="right", style="magenta")
        table.add_column("Risk Level", style="bold")
        table.add_column("Recommendation", style="dim")

        for result in results:
            risk_level = result.get("risk_level", "MEDIUM")

            # Color coding based on risk level
            if risk_level == "LOW":
                risk_style = "green bold"
            elif risk_level == "MEDIUM":
                risk_style = "yellow bold"
            else:
                risk_style = "red bold"

            table.add_row(
                result.get("client", "Unknown"),
                f"${result.get('mrr', 0):.2f}",
                f"{result.get('activity_score', 0):.1f}",
                f"{result.get('score', 0):.1f}",
                result.get("risk_level", "MEDIUM"),
                result.get("recommendation", "")
            )

        self.console.print(table)

    def output_json(self, results: List[Dict]) -> str:
        """Output results as JSON."""
        import json
        return json.dumps(results, indent=2)
