import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_cars') 

    tenant_id = event.get('tenant_id', None)

    if tenant_id:
        response = table.query(
            KeyConditionExpression=Key('tenant_id').eq(tenant_id)
        )
        items = response.get('Items', [])
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'tenant_id is required'})
        }
    
    return {
        'statusCode': 200,
        'body': items
    }
