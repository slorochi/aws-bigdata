import random
import string
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb", region_name="us-east-1") 

restaurants_table = dynamodb.Table("restaurants-dev")
reviews_table = dynamodb.Table("reviews-dev")

def generate_review(restaurant_id):
    review_texts = [
        "Excellent food, highly recommend!",
        "The service was a bit slow, but the meal was great.",
        "Not worth the price, very disappointed.",
        "Amazing ambiance, perfect for a dinner date.",
        "The staff were very friendly and helpful.",
        "I had a great experience, will definitely come back!",
        "The food was cold when it arrived, but it tasted good.",
        "A bit too salty for my taste, but overall okay.",
        "I love this place! The food is always fresh and delicious.",
        "Terrible experience, won’t return.",
        "Nice variety on the menu, something for everyone.",
        "Food was delicious, but the wait time was long.",
        "Great value for the price, I’ll be back soon.",
        "Good portion sizes, I left feeling full and happy.",
        "One of the best meals I've had in a long time!",
        "Fantastic meal! The grilled salmon was cooked to perfection, and the dessert was delightful.",
        "I had high expectations, but the food didn't meet them. The steak was overcooked.",
        "Great place for a casual dinner with friends. The staff was attentive and welcoming.",
        "I will never come back. The food was bland, and the service was terrible.",
        "The ambiance here is amazing! Perfect spot for a romantic evening.",
        "I loved the pasta dish, but the wine selection could be better.",
        "A hidden gem! The food was incredible, and the prices are very reasonable.",
        "Not impressed with the sushi. I expected it to be fresher."
    ]
    
    review = random.choice(review_texts)
    rating = random.randint(1, 5)
    review_date = f"2025-01-{random.randint(1, 31):02d}"
    review_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    return {
        'id': review_id,
        'restaurant_id': restaurant_id,
        'review_text': review,
        'rating': rating,
        'date': review_date
    }

def add_reviews_for_restaurant(restaurant_id, number_of_reviews):
    """Ajoute un certain nombre d'avis à un restaurant"""
    for _ in range(number_of_reviews):
        review = generate_review(restaurant_id)
        try:
            # Ajouter l'avis à la table Reviews
            response = reviews_table.put_item(Item=review)
            print(f"Avis ajouté pour restaurant {restaurant_id}: {review['review_text']}")
        except ClientError as e:
            print(f"Erreur lors de l'ajout de l'avis: {e.response['Error']['Message']}")

def get_all_restaurants():
    response = restaurants_table.scan()
    return response.get("Items", [])

restaurants = get_all_restaurants()
for restaurant in restaurants:
    restaurant_id = restaurant["id"]
    if(restaurant_id):
        add_reviews_for_restaurant(restaurant_id, 15)
    else:
        print(f" Pas d'id pour le restaurant {restaurant['id']}")