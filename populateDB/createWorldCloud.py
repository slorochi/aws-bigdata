import boto3
import json
import re
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))

# Configuration AWS DynamoDB
dynamodb = boto3.resource("dynamodb")
REVIEWS_TABLE_NAME = "reviews-dev" 
table = dynamodb.Table(REVIEWS_TABLE_NAME)

def get_reviews():
    """Récupère toutes les reviews depuis DynamoDB."""
    response = table.scan()
    reviews = []
    for item in response.get("Items", []):
        reviews.extend(json.loads(item["reviews"]))
    return reviews

def clean_text(text):
    """Nettoie le texte : suppression des caractères spéciaux, mise en minuscule et suppression des stopwords."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split()
    words = [word for word in words if word not in STOPWORDS] 
    return " ".join(words)

def generate_wordcloud(reviews):
    """Génère et affiche un nuage de mots à partir des reviews."""
    cleaned_text = " ".join([clean_text(review) for review in reviews])
    
    wordcloud = WordCloud(
        width=800, height=400,
        background_color="white",
        colormap="viridis",
        stopwords=STOPWORDS,
        max_words=100
    ).generate(cleaned_text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nuage de mots des reviews")
    plt.show()

    wordcloud.to_file("wordcloud.png") 
if __name__ == "__main__":
    reviews = get_reviews()
    if reviews:
        generate_wordcloud(reviews)
        print("✅ WordCloud généré avec succès !")
    else:
        print("⚠️ Aucune review trouvée dans la base de données.")
