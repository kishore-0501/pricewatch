import pandas as pd
from main.models import Product, PriceEntry

def load_mock_data():
    df = pd.read_csv("main/data/sample_prices.csv")

    for _, row in df.iterrows():
        product, _ = Product.objects.get_or_create(name=row["product"])
        PriceEntry.objects.create(
            product=product,
            retailer=row["retailer"],
            price=row["price"],
            date=row["date"]
        )
