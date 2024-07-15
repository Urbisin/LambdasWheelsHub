import boto3

def lambda_handler(event, context):

    tenant_id = event['tenant_id']
    email = event['email']
    password = event['password']

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_users')
    
    response = table.get_item(
        Key = {
            'tenant_id': tenant_id,
            'user_id': email
        }
    )

    if 'Item' not in response:
        return {
            'statusCode': 403,
            'body': 'User not found'
        }
    else:
        password_bd = response['Item']['password']
        if password == password_bd:
            email = response['Item']['user_id']
            wallet = response['Item']['wallet']
            return {
                'statusCode': 200,
                'body': 'User logged in successfully',
                'email': email,
                'wallet': wallet
            }
        else:
            return {
                'statusCode': 403,
                'body': 'Invalid password or email'
            }
    
        
