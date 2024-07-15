import boto3

def lambda_handler(event, context):
    try:
        tenant_id = event.get('tenant_id')
        email = event.get('email')
        password = event.get('password')

        if email is not None and password is not None:
            dynamodb = boto3.resource('dynamodb')
            t_users = dynamodb.Table('t_users')

            t_users.put_item(
                Item = {
                    'tenant_id': tenant_id,
                    'user_id': email,
                    'password': password,
                    'wallet': 1000000
                }
            )

            message = {
                'message': 'User registered successfully',
                'email': email
            }
            
            return {
                'statusCode': 200,
                'body': message
            }
        else:
            message = {
                'error': 'Invalid request body: missing email or password'
            }

            return {
                'statusCode': 400,
                'body': message
            }
        
    except Exception as e:
        print("Exception:", str(e))
        message = {
            'error': str(e)
        }
        
        return {
            'statusCode': 500,
            'body': message
        }