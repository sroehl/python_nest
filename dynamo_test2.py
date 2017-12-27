import boto3
from boto3.dynamodb.conditions import Key, Attr



dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('HomeTempItems')
response = table.query(
    KeyConditionExpression=Key('id').eq(0)
)
items = response['Items']
for item in items:
    print(item)
