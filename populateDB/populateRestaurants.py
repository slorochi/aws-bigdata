import boto3
from decimal import Decimal
import requests
from dotenv import load_dotenv
import os

load_dotenv()


def get_table_name():
    """Get the full table name including Amplify environment prefix"""
    dynamodb = boto3.client('dynamodb')
    tables = dynamodb.list_tables()['TableNames']

    restaurant_table = [t for t in tables if 'restaurants' in t.lower()]
    if restaurant_table:
        return restaurant_table[0]
    return None

YELP_API_KEY = os.getenv("YELP_API_KEY")

if not YELP_API_KEY:
    raise ValueError("ERREUR: La variable d'environnement YELP_API_KEY n'est pas définie.")
YELP_SEARCH_URL = "https://api.yelp.com/v3/businesses/search"

def get_yelp_data():
    """Fetch restaurants data from Yelp API"""
    headers = {
        "Authorization": f"Bearer {YELP_API_KEY}"
    }
    params = {
        "location": "Paris",
        "term": "restaurant",
        "limit": 10
    }
    
    response = requests.get(YELP_SEARCH_URL, headers=headers, params=params)
    return response.json()

def insert_restaurants():
    table_name = get_table_name()
    if not table_name:
        print("Couldntt find the restaurants table. run 'amplify push'")
        return
    
    print(f"✅ Found table: {table_name}")
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    data = get_yelp_data()
    
    # Insert data
    with table.batch_writer() as batch:
        for business in data.get("businesses", []):
            restaurant = {
                "id": business["id"],
                "name": business["name"],
                "rating": Decimal(str(business["rating"])),
                "price": Decimal(str(len(business.get("price", "$")))),
                "address": business.get("location", {}).get("address1", ""),
                "city": business.get("location", {}).get("city", ""),
                "zip_code": business.get("location", {}).get("zip_code", ""),
                "phone": business.get("phone", ""),
                "image_url": business.get("image_url", ""),
                "url": business.get("url", "")
            }
            print(f"Adding restaurant: {restaurant['name']}")
            print(business["id"])
            print(f"Inserting item: {restaurant}")

            batch.put_item(Item=restaurant)
            
if __name__ == "__main__":
    insert_restaurants()
