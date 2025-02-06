import boto3
import json

PROFILE_NAME = "bigdataf90580da" 
session = boto3.Session(profile_name=PROFILE_NAME)
s3 = session.client("s3")
dynamodb = session.resource("dynamodb")

TABLE_NAME = "restaurants-dev"
BUCKET_NAME = "yelp-reviews-bucket"

table = dynamodb.Table(TABLE_NAME)

response = table.scan()
restaurants_data = response.get("Items", [])

data_restaurants_json = json.dumps(restaurants_data, ensure_ascii=False).encode("utf-8")

DATA_JSON_PATH = "data/restaurants.json"
MANIFEST_PATH = "data/datasource.manifest"

s3.put_object(Bucket=BUCKET_NAME, Body=data_restaurants_json, Key=DATA_JSON_PATH)

manifest_template = json.dumps({
    "fileLocations": [{"URIs": [f"s3://{BUCKET_NAME}/{DATA_JSON_PATH}"]}],
    "globalUploadSettings": {"format": "JSON"}
})

s3.put_object(Bucket=BUCKET_NAME, Body=manifest_template, Key=MANIFEST_PATH)

print("Données envoyées avec dans le S3 !")
