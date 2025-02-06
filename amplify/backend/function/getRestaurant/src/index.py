import json
import boto3
from botocore.exceptions import ClientError
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
from io import BytesIO
import base64

def generate_wordcloud(reviews):
    text = ' '.join([review['review_text'] for review in reviews])
    
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    
    img = BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    
    return img_base64

def analyze_sentiments(reviews):
    sentiment_scores = {'positive': 0, 'negative': 0, 'neutral': 0}
    
    for review in reviews:
        blob = TextBlob(review['review_text'])
        sentiment = blob.sentiment.polarity  
        
        if sentiment > 0:
            sentiment_scores['positive'] += 1
        elif sentiment < 0:
            sentiment_scores['negative'] += 1
        else:
            sentiment_scores['neutral'] += 1
    
    # Calculer la répartition des sentiments
    total_reviews = len(reviews)
    sentiment_distribution = {key: value / total_reviews for key, value in sentiment_scores.items()}
    
    return sentiment_distribution

def handler(event, context):
    restaurant_id = event['pathParameters']['restaurant_id']
    
    dynamodb = boto3.resource('dynamodb')
    reviews_table = dynamodb.Table('reviews-dev')
    
    try:
        response = reviews_table.query(
            KeyConditionExpression="restaurant_id = :restaurant_id",
            ExpressionAttributeValues={":restaurant_id": restaurant_id}
        )
        
        reviews = response['Items']
        
        if reviews:
            wordcloud_base64 = generate_wordcloud(reviews)
            sentiment_distribution = analyze_sentiments(reviews)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps({
                    'wordcloud': wordcloud_base64,
                    'sentiment_distribution': sentiment_distribution
                })
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'No reviews found for this restaurant'})
            }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
