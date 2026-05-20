from rich.console import Console
from rich.table import Table


class ReportGenerator:
    """Generates formatted reports using rich."""

    def __init__(self, results):
        self.results = results
        self.console = Console()

    def generate_report(self):
        """Generate and print the report table."""
        table = Table(show_header=True, header_style='bold cyan')
        table.add_column('Client', style='white')
        table.add_column('MRR', style='green')
        table.add_column('Activity Score', style='yellow')
        table.add_column('Churn Risk', style='bold')
        table.add_column('Recommendation', style='blue')

        for result in self.results:
            risk = result.get('churn_risk', 'MEDIUM')
            if risk == 'LOW':
                color = 'green'
            elif risk == 'MEDIUM':
                color = 'yellow'
            else:
                color = 'red'

            table.add_row(
                result.get('client', 'Unknown'),
                f"${result.get('mrr', 0):.2f}",
                str(result.get('activity_score', 0)),
                f'[{color}]{risk}[/]',
                result.get('recommendation', 'N/A')
            )

        self.console.print(table)
