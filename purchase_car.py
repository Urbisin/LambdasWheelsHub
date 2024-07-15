import json
import boto3
import uuid

def lambda_handler(event, context):
    print(event)

    purchase_json = json.loads(event['Records'][0]['Sns']['Message'])

    dynamodb = boto3.resource('dynamodb')
    purchases_table = dynamodb.Table('t_purchases')
    users_table = dynamodb.Table('t_users')
    cars_table = dynamodb.Table('t_cars')

    user_response = users_table.get_item(Key={'tenant_id' : purchase_json['tenant_id'], 'user_id': purchase_json['user_id']})
    car_response = cars_table.get_item(Key={'tenant_id' : purchase_json['tenant_id'], 'car_id': purchase_json['car_id']})

    user = user_response['Item']
    car = car_response['Item']

    car_cost = car['price']
    user_money = user['wallet']

    new_user_money = user_money - car_cost
    new_car_stock = car['stock'] - 1

    users_table.update_item(
        Key={'tenant_id' : purchase_json['tenant_id'], 'user_id': purchase_json['user_id']},
        UpdateExpression='SET wallet = :val',
        ExpressionAttributeValues={':val': new_user_money}
    )

    cars_table.update_item(
        Key={'tenant_id' : purchase_json['tenant_id'], 'car_id': purchase_json['car_id']},
        UpdateExpression='SET stock = :val',
        ExpressionAttributeValues={':val': new_car_stock}
    )

    random_uuid = str(uuid.uuid4())
    purchase_id = f"{purchase_json['tenant_id']}_{random_uuid}"

    purchase = {
        'tenant_id': purchase_json['tenant_id'],
        'purchase_id': purchase_id,
        'user_id': purchase_json['user_id'],
        'car_id': purchase_json['car_id'],
        'car_cost' : car['price']
    }

    purchases_table.put_item(Item=purchase)


    return {
        'statusCode': 200,
        'message': 'Purchase completed successfully'
    }