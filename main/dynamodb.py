import boto3
from boto3.dynamodb.conditions import Key

# dynamodb = boto3.client('dynamodb', region_name='us-east-1')

# # Create Products table
# try:
#     response = dynamodb.create_table(
#         TableName='Products',
#         KeySchema=[
#             {'AttributeName': 'product_id', 'KeyType': 'HASH'}  # Partition key
#         ],
#         AttributeDefinitions=[
#             {'AttributeName': 'product_id', 'AttributeType': 'S'}  # String type
#         ],
#         ProvisionedThroughput={
#             'ReadCapacityUnits': 5,
#             'WriteCapacityUnits': 5
#         }
#     )
#     print("Products table created successfully!")
# except dynamodb.exceptions.ResourceInUseException:
#     print("Products table already exists!")
    

# # Create Prices table
# try:
#     response = dynamodb.create_table(
#         TableName='Prices',
#         KeySchema=[
#             {'AttributeName': 'product_id', 'KeyType': 'HASH'},  # Partition key
#             {'AttributeName': 'vendor', 'KeyType': 'RANGE'}     # Sort key
#         ],
#         AttributeDefinitions=[
#             {'AttributeName': 'product_id', 'AttributeType': 'S'},  # String
#             {'AttributeName': 'vendor', 'AttributeType': 'S'}       # String
#         ],
#         ProvisionedThroughput={
#             'ReadCapacityUnits': 5,
#             'WriteCapacityUnits': 5
#         }
#     )
#     print("Prices table created successfully!")
# except dynamodb.exceptions.ResourceInUseException:
#     print("Prices table already exists!")


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
# product_table = dynamodb.Table('Products')

# # Dummy products
# products = [
#     {
#         'product_id': '1',
#         'name': 'iPhone 17 Pro',
#         'description': 'Latest Apple iPhone model',
#         'image': 'iphone17pro.jpg'
#     },
#     {
#         'product_id': '2',
#         'name': 'Samsung Galaxy S23',
#         'description': 'Flagship Samsung phone',
#         'image': 'galaxys23.jpg'
#     }
# ]

# # Insert products
# for product in products:
#     product_table.put_item(Item=product)

# print("Products inserted successfully!")





# price_table = dynamodb.Table('Prices')

# # Dummy prices for vendors
# prices = [
#     {
#         'product_id': '1',
#         'vendor': 'Amazon',
#         'price': 1299,
#         'currency': 'USD',
#         'url': 'https://www.amazon.com/iphone17pro'
#     },
#     {
#         'product_id': '1',
#         'vendor': 'eBay',
#         'price': 1249,
#         'currency': 'USD',
#         'url': 'https://www.ebay.com/iphone17pro'
#     },
#     {
#         'product_id': '2',
#         'vendor': 'Amazon',
#         'price': 999,
#         'currency': 'USD',
#         'url': 'https://www.amazon.com/galaxys23'
#     },
#     {
#         'product_id': '2',
#         'vendor': 'BestBuy',
#         'price': 1049,
#         'currency': 'USD',
#         'url': 'https://www.bestbuy.com/galaxys23'
#     }
# ]

# # Insert prices
# for price in prices:
#     price_table.put_item(Item=price)

# print("Prices inserted successfully!")

price_table = dynamodb.Table('Prices')
price_response = price_table.query(
    KeyConditionExpression=Key('product_id').eq('1')
)
print(price_response.get('Items', []))