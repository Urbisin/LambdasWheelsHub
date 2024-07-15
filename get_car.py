import json
import boto3
from decimal import Decimal

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_cars')

    tenant_id = event.get('tenant_id', None)
    car_id = event.get('car_id', None)

    if not tenant_id or not car_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Both tenant_id and car_id are required'})
        }

    response = table.get_item(
        Key={
            'tenant_id': tenant_id,
            'car_id': car_id
        }
    )
    item = response.get('Item', None)

    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Car not found'})
        }

    return {
        'statusCode': 200,
        'body': item
    }