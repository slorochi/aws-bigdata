from textblob import TextBlob

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