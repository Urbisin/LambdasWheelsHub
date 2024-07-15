import json
import boto3

def lambda_handler(event, context):
    purchase = json.dumps(event)

    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/066764054672/purchase_queue'

    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=(purchase)
    )

    return {
        'statusCode': 200,
        'response': response
    }