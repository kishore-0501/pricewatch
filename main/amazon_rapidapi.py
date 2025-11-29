import os, requests, urllib.parse

RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST')
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_URL = os.getenv('RAPIDAPI_URL')  # Make sure this is the provider's search endpoint

def fetch_amazon_data(query, limit=5):
    # fallback to mock if not configured
    if not (RAPIDAPI_HOST and RAPIDAPI_KEY and RAPIDAPI_URL):
        # mocked single result so app can continue
        return [{
            'merchant': 'amazon',
            'title': f'Mock Amazon result for {query}',
            'price': 829.00,
            'currency': 'EUR',
            'url': 'https://www.amazon.ie/example',
            'image': None,
        }]
    q = urllib.parse.quote(query)
    # some providers append query string differently; check provider docs
    url = RAPIDAPI_URL if '?' in RAPIDAPI_URL else f"{RAPIDAPI_URL}{q}"
    headers = {
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY,
        'Accept': 'application/json'
    }
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    j = r.json()
    # mapping depends on provider; try common fields
    results = []
    candidates = j.get('items') or j.get('results') or j.get('products') or j.get('data') or []
    for it in candidates[:limit]:
        price = None
        if isinstance(it.get('price'), dict):
            price = it['price'].get('value') or it['price'].get('amount')
        elif it.get('price'):
            try:
                price = float(str(it['price']).replace(',', ''))
            except:
                price = None
        results.append({
            'merchant': 'amazon',
            'title': it.get('title') or it.get('name'),
            'price': float(price) if price else None,
            'currency': it.get('currency') or 'EUR',
            'url': it.get('url') or it.get('link'),
            'image': it.get('image') or None
        })
    # fallback if provider returns a different shape
    if not results and j.get('title'):
        results.append({
            'merchant': 'amazon',
            'title': j.get('title'),
            'price': j.get('price'),
            'currency': j.get('currency') or 'EUR',
            'url': j.get('url'),
            'image': j.get('image'),
        })
    return results
