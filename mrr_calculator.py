def calculate_mrr(subscriptions):
    total_mrr = 0
    for sub in subscriptions:
        try:
            if 'lines' in sub and 'data' in sub['lines']:
                for line in sub['lines']['data']:
                    if 'plan' in line and 'amount' in line['plan']:
                        total_mrr += line['plan']['amount']
        except (KeyError, TypeError):
            continue
    return total_mrr / 100