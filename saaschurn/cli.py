import click
import json
from rich.console import Console
from rich.table import Table
from saaschurn import core

@click.command()
@click.option('--dry-run', is_flag=True, help='Run in dry-run mode')
@click.option('--output', type=click.Choice(['json', 'table']), default='table', help='Output format')
def health(dry_run, output):
    """Run health check for SaaS clients."""
    if dry_run:
        click.echo("Dry-run mode enabled.")
        return
    
    try:
        stripe_client = core.get_stripe_client()
        slack_client = core.get_slack_client()
    except ValueError as e:
        click.echo(f"Error: {e}")
        return

    subscriptions = [{'status': 'active', 'plan': {'amount': 10000}}]
    mrr = core.calculate_mrr(subscriptions)
    activity = core.get_slack_activity(slack_client, ['C123'])
    score = core.compute_churn_score([1000, 500], [10, 5])
    
    if output == 'json':
        click.echo(json.dumps({'mrr': mrr, 'churn_score': score}))
    else:
        table = Table()
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("MRR", f"${mrr}")
        table.add_row("Churn Score", f"{score}%")
        console = Console()
        console.print(table)
