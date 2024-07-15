import boto3

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')

    cars_table = dynamodb.Table('t_cars')

    tenant_id = event['tenant_id']
    
    if tenant_id == "HONDA":
        car_id = "H_" + event['car_id']
    elif tenant_id == "NISSAN":
        car_id = "N_" + event['car_id']
    elif tenant_id == "FORD":
        car_id = "F_" + event['car_id']

    model = event['model']
    price = event['price']
    image_url = event['image_url']
    stock = 10

    car = {
        'tenant_id': tenant_id,
        'car_id': car_id,
        'model': model,
        'price': price,
        'image_url': image_url,
        'stock': stock
    }

    cars_table.put_item(Item=car)

    return {
        'statusCode': 200,
        'message': 'Car added successfully'
    }




    