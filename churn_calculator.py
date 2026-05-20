def calculate_mrr(subscriptions):
    mrr = 0
    for sub in subscriptions:
        if sub.get('status') == 'active':
            plan = sub.get('plan', {})
            amount = plan.get('amount', 0)
            mrr += amount
    return mrr
