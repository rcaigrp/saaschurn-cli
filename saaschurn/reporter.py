from rich.console import Console
from rich.table import Table


def generate_report(data):
    console = Console()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Client")
    table.add_column("MRR")
    table.add_column("Activity")
    table.add_column("Risk")
    table.add_column("Recommendation")

    for client_id, info in data.items():
        risk = info["risk"]
        color = "red" if risk > 70 else ("yellow" if risk > 30 else "green")
        recommendation = "Churn Risk" if risk > 70 else ("Monitor" if risk > 30 else "Healthy")
        table.add_row(
            client_id,
            f"${info['mrr']:.2f}",
            f"{info['activity']}",
            f"{risk}%",
            recommendation,
            style=color
        )
    console.print(table)
