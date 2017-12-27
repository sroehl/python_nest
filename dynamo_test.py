from datetime import datetime
from dynamodb_mapper.model import DynamoDBModel, utc_tz
from boto.dynamodb.condition import *

class HomeTempItemsModel(DynamoDBModel):
    __table__ = u"HomeTempItems"

data_generator = HomeTempItemModel.query()

for data in data_generator:
    print(data)
