import requests

def fetch_active_subscriptions(api_key, base_url='https://api.stripe.com/v1/subscriptions'):
    headers = {'Authorization': f'Bearer {api_key}'}
    params = {'status': 'active', 'limit': 100}
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])
    except requests.RequestException:
        return []