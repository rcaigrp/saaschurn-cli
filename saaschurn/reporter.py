from rich.table import Table
from rich import print

def generate_report(data):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Client")
    table.add_column("MRR")
    table.add_column("Activity")
    table.add_column("Risk")
    table.add_column("Recommendation")
    for item in data:
        table.add_row(str(item.get("client_id")), str(item.get("mrr")), str(item.get("slack_activity")), str(item.get("churn_risk")), str(item.get("recommendation")))
    print(table)
