import os, time, base64, requests
from django.core.cache import cache

EBAY_CLIENT_ID = os.getenv('EBAY_CLIENT_ID')
EBAY_CLIENT_SECRET = os.getenv('EBAY_CLIENT_SECRET')

TOKEN_CACHE_KEY = 'ebay_app_token'
TOKEN_TTL_PADDING = 30  # secs

def get_ebay_app_token():
    token_data = cache.get(TOKEN_CACHE_KEY)
    if token_data:
        return token_data['access_token']

    if not EBAY_CLIENT_ID or not EBAY_CLIENT_SECRET:
        raise RuntimeError("EBAY_CLIENT_ID/SECRET not set in env")

    auth = base64.b64encode(f"{EBAY_CLIENT_ID}:{EBAY_CLIENT_SECRET}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials', 'scope': 'https://api.ebay.com/oauth/api_scope'}
    r = requests.post('https://api.ebay.com/identity/v1/oauth2/token', headers=headers, data=data)
    r.raise_for_status()
    j = r.json()
    token = j['access_token']
    expires_in = int(j.get('expires_in', 7200))
    cache.set(TOKEN_CACHE_KEY, {'access_token': token}, timeout=expires_in - TOKEN_TTL_PADDING)
    return token

def search_ebay(query, limit=5):
    token = get_ebay_app_token()
    params = {'q': query, 'limit': limit}
    headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
    r = requests.get('https://api.ebay.com/buy/browse/v1/item_summary/search', headers=headers, params=params)
    r.raise_for_status()
    j = r.json()
    items = []
    for it in j.get('itemSummaries', []):
        price = None
        if 'price' in it:
            price = float(it['price']['value']) if it['price'].get('value') else None
        items.append({
            'merchant': 'ebay',
            'title': it.get('title'),
            'price': price,
            'currency': it.get('price', {}).get('currency'),
            'url': it.get('itemWebUrl'),
            'image': it.get('image', {}).get('imageUrl') if it.get('image') else None
        })
    return items
