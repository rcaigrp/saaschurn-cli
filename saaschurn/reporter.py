from rich import print
from rich.table import Table

def generate_report(data):
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Client")
    table.add_column("MRR")
    table.add_column("Churn Risk")
    table.add_column("Recommendation")
    for item in data:
        table.add_row(item['client'], str(item['mrr']), item['risk'], item['rec'])
    print(table)
