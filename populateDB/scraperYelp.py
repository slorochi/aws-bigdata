import requests
from bs4 import BeautifulSoup
import time
import boto3
import time
import requests
from bs4 import BeautifulSoup
import time
from random import randint
from datetime import datetime

dynamodb = boto3.resource("dynamodb", region_name="us-east-1") 
restaurants_table = dynamodb.Table("restaurants-dev")
reviews_table = dynamodb.Table("reviews-dev")

def save_reviews_to_dynamodb(restaurant_id, reviews):
    """Enregistre les reviews dans la table reviews-dev"""
    with reviews_table.batch_writer() as batch:
        for review_text in reviews:
            review_item = {
                "restaurant_id": restaurant_id,  
                "review_id": str(time.time()),
                "text": review_text
            }
            batch.put_item(Item=review_item)
            print(f"✅ Review ajoutée : {review_text[:50]}...")


def scrape_restaurant_reviews(restaurant_url, restaurant_id):
    """
    Scrape up to 15 reviews from a restaurant's Yelp page.
    
    Args:
        restaurant_url (str): The Yelp URL of the restaurant
        
    Returns:
        list: List of dictionaries containing review data
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    reviews = []
    
    try:
        time.sleep(randint(1, 3))
        
        response = requests.get(restaurant_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch URL: {response.status_code}")
            return reviews
            
        soup = BeautifulSoup(response.text, 'html.parser')
        review_elements = soup.find_all('p', {'class': 'comment__09f24__D0cxf'})[:15]
        
        for review in review_elements:
            try:
                review_data = {
                    'text': review.get_text().strip(),
                    'scraped_at': datetime.now().isoformat()
                }
                
                reviews.append(review_data)
                
            except Exception as e:
                print(f"Error processing review: {str(e)}")
                continue
    except Exception as e:
        print(f"Error scraping reviews: {str(e)}")

    print(reviews)
    save_reviews_to_dynamodb(restaurant_id, reviews)

def get_all_restaurants():
    response = restaurants_table.scan()
    return response.get("Items", [])

restaurants = get_all_restaurants()

for restaurant in restaurants:
    restaurant_id = restaurant["id"]
    yelp_url = restaurant.get("url", "") 
    if yelp_url:
        print(yelp_url)
        scrape_restaurant_reviews(yelp_url, restaurant_id)
    else:
        print(f" Pas d'URL Yelp pour le restaurant {restaurant['name']}")
