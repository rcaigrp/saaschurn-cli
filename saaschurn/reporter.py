from rich.console import Console
from rich.table import Table

console = Console()

def print_report(data):
    table = Table(show_header=True, header_style='bold magenta')
    table.add_column('Client', style='dim')
    table.add_column('MRR', style='green')
    table.add_column('Activity', style='yellow')
    table.add_column('Risk', style='red')
    table.add_column('Recommendation', style='bold')
    for client, info in data.items():
        risk = info['risk']
        style = 'green' if risk == 'LOW' else ('yellow' if risk == 'MEDIUM' else 'red')
        table.add_row(
            client,
            f"${info['mrr']:.2f}",
            f"{info['activity']}",
            f"{info['score']} ({risk})",
            info['recommendation']
        )
    console.print(table)
