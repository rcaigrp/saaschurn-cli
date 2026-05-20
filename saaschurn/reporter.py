from rich.console import Console
from rich.table import Table

def generate_report(results):
    console = Console()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Client")
    table.add_column("MRR")
    table.add_column("Activity Score")
    table.add_column("Churn Risk")
    table.add_column("Recommendation")
    for res in results:
        risk = res.get("risk_level")
        style = "green" if risk == "LOW" else ("yellow" if risk == "MEDIUM" else "red")
        table.add_row(
            res["client"],
            f"${res['mrr']:.2f}",
            str(res["activity_score"]),
            f"{res['risk_score']} ({risk})",
            res["recommendation"]
        )
    console.print(table)
