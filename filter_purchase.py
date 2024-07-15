import json
import boto3

def lambda_handler(event, context):
    print("Lambda triggered with event: ", event)

    sns = boto3.client('sns')
    sns_topic_arn = 'arn:aws:sns:us-east-1:066764054672:purchase_sns'

    dynamodb = boto3.resource('dynamodb')
    users_table = dynamodb.Table('t_users')
    cars_table = dynamodb.Table('t_cars')

    for record in event['Records']:
        try:
            print("Processing record: ", record)
            purchase = json.loads(record['body'])
            print("Message body: ", purchase)

            tenant_id = purchase.get('tenant_id')
            user_id = purchase.get('user_id')
            car_id = purchase.get('car_id')

            if not tenant_id or not user_id or not car_id:
                print("Message body missing required fields")
                continue

            print(f"Fetching user data for tenant_id: {tenant_id}, user_id: {user_id}")
            user_response = users_table.get_item(
                Key={
                    'tenant_id': tenant_id,
                    'user_id': user_id
                }
            )
            print(f"user_response: {user_response}")

            user_wallet = user_response['Item']['wallet']

            print(f"Fetching car data for tenant_id: {tenant_id}, car_id: {car_id}")
            car_response = cars_table.get_item(
                Key={
                    'tenant_id': tenant_id,
                    'car_id': car_id
                }
            )
            print(f"car_response: {car_response}")

            car_price = car_response['Item']['price']
            car_stock = car_response['Item']['stock']

            if user_wallet >= car_price and car_stock > 0:
                sns_message = {
                    'tenant_id': tenant_id,
                    'user_id': user_id,
                    'car_id': car_id
                }

                sns_message_str = json.dumps(sns_message) 

                try:
                    print(f"Publishing message to SNS: {sns_message_str}")
                    sns_response = sns.publish(
                        TopicArn=sns_topic_arn,
                        Message=sns_message_str,
                        MessageAttributes={
                            'tenant_id': {'Dat  aType': 'String', 'StringValue': tenant_id}
                        },
                        Subject='Car can be purchased'
                    )
                    print(f"Message sent to SNS: {sns_response}")
                except Exception as e:
                    print(f"Error sending message to SNS: {e}")

                receipt_handle = record['receiptHandle']
                try:
                    sqs = boto3.client('sqs')
                    print("Deleting message from SQS")
                    sqs.delete_message(
                        QueueUrl='https://sqs.us-east-1.amazonaws.com/066764054672/purchase_queue',
                        ReceiptHandle=receipt_handle
                    )
                except Exception as e:
                    print(f"Error deleting message from SQS: {e}")
            else:
                print("Insufficient funds or no stock available")
                raise Exception("Purchase cannot be processed due to insufficient funds or lack of stock.")
        
        except Exception as e:
            print(f"Error processing record: {e}")
            continue

    print("Processing completed")
    return {
        'statusCode': 200,
        'body': json.dumps('Processing completed')
    }
