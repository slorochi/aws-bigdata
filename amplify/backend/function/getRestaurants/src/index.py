import json
import boto3

dynamodb = boto3.resource('dynamodb')
restaurants_table = dynamodb.Table('restaurants-dev')

def handler(event, context):
    print('received event:')
    print(event)

    try:
        response = restaurants_table.scan()
        restaurants = response.get('Items', [])
        
        if restaurants:
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps(restaurants)
            }
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps({'message': 'No restaurants found'})
            }
    
    except Exception as e:
        print("err")