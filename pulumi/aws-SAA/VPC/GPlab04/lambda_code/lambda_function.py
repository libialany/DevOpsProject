import json
import boto3
from botocore.exceptions import ClientError

# Inicializa el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = 'test'  # Reemplaza con el nombre de tu tabla
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    http_method = event['httpMethod']
    if http_method == 'GET':
        if 'queryStringParameters' in event and 'id' in event['queryStringParameters']:
            return get_item(event['queryStringParameters']['id'])
        else:
            return get_all_items()
    elif http_method == 'POST':
        return create_item(json.loads(event['body']))
    elif http_method == 'PUT':
        return update_item(json.loads(event['body']))
    elif http_method == 'DELETE':
        if 'queryStringParameters' in event and 'id' in event['queryStringParameters']:
            return delete_item(event['queryStringParameters']['id'])
        else:
            return response(400, 'Falta el parámetro id en la solicitud DELETE')
    else:
        return response(405, f'Método HTTP {http_method} no permitido')

def get_item(item_id):
    try:
        result = table.get_item(Key={'id': item_id})
        if 'Item' in result:
            return response(200, result['Item'])
        else:
            return response(404, f'Elemento con id {item_id} no encontrado')
    except ClientError as e:
        return response(500, e.response['Error']['Message'])

def get_all_items():
    try:
        result = table.scan()
        return response(200, result.get('Items', []))
    except ClientError as e:
        return response(500, e.response['Error']['Message'])

def create_item(data):
    try:
        table.put_item(Item=data)
        return response(201, 'Elemento creado exitosamente')
    except ClientError as e:
        return response(500, e.response['Error']['Message'])

def update_item(data):
    try:
        table.update_item(
            Key={'id': data['id']},
            UpdateExpression="set info=:i",
            ExpressionAttributeValues={':i': data['info']},
            ReturnValues="UPDATED_NEW"
        )
        return response(200, 'Elemento actualizado exitosamente')
    except ClientError as e:
        return response(500, e.response['Error']['Message'])

def delete_item(item_id):
    try:
        table.delete_item(Key={'id': item_id})
        return response(200, 'Elemento eliminado exitosamente')
    except ClientError as e:
        return response(500, e.response['Error']['Message'])

def response(status_code, message):
    return {
        'statusCode': status_code,
        'body': json.dumps({'message': message}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
