import json

def _convert(obj):
    if isinstance(obj, dict):
        return {k: _convert(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_convert(i) for i in obj]
    if hasattr(obj, '__dict__'):
        return {k: _convert(v) for k, v in obj.__dict__.items() if not k.startswith('_')}
    return obj

def export_to_json(subscriptions, mrr, output_path):
    data = {
        'subscriptions': _convert(subscriptions),
        'mrr': mrr
    }
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
