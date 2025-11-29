from django.core.management.base import BaseCommand
from main.models import Product  # your model
from main.amazon_rapidapi import fetch_amazon_data  # example

class Command(BaseCommand):
    help = "Scrape Amazon/eBay once and save product price"

    def add_arguments(self, parser):
        parser.add_argument("--query", type=str, required=True)

    def handle(self, *args, **options):
        query = options['query']
        self.stdout.write(f"Scraping for: {query}")

        data = fetch_amazon_data(query)
        # process and save data
        self.stdout.write(self.style.SUCCESS("Scraping completed"))
