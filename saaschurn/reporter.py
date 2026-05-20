from rich.table import Table
from rich.console import Console


class Reporter:
    def __init__(self):
        self.console = Console()

    def print_table(self, results):
        table = Table(show_header=True, header_style='bold cyan')
        table.add_column('Client', style='white')
        table.add_column('MRR', style='green')
        table.add_column('Activity Score', style='yellow')
        table.add_column('Churn Risk', style='red')
        table.add_column('Risk Level', style='bold')
        table.add_column('Recommendation', style='cyan')

        for row in results:
            risk_level = row['risk_level']
            risk_style = 'green' if risk_level == 'LOW' else ('yellow' if risk_level == 'MEDIUM' else 'red')

            table.add_row(
                row['client'],
                f"${row['mrr']:.2f}",
                str(row['activity_score']),
                str(row['churn_risk']),
                f'[{risk_style}]',
                row['recommendation']
            )

        self.console.print(table)
