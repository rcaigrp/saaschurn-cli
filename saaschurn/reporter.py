from rich.console import Console
from rich.table import Table
import json

console = Console()


def generate_report(data, dry_run=False, output_format="table"):
    if output_format == "json":
        print(json.dumps(data, indent=2))
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Client")
    table.add_column("MRR")
    table.add_column("Activity")
    table.add_column("Risk")
    table.add_column("Recommendation")

    for item in data:
        risk_style = "green" if item["risk_level"] == "LOW" else ("yellow" if item["risk_level"] == "MEDIUM" else "red")
        table.add_row(
            str(item["customer_id"]),
            f"${item['mrr']}",
            str(item["activity_score"]),
            f"{item['risk_score']:.1f} ({item['risk_level']})",
            item["recommendation"]
        )

    console.print(table)
    if dry_run:
        console.print("[yellow]Dry-run mode enabled. Skipping API calls.[/yellow]")
