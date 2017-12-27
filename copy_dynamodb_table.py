import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('HomeTempItems')
response = table.query(
    KeyConditionExpression=Key('id').eq(0)
)
items = response['Items']
table2 = dynamodb.Table('HomeTempItems2')
for item in items:
    item['date'] = int(item['date'])
    table2.put_item(TableName='HomeTempItems2', Item=item)

