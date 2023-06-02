import json
import random
import string
import boto3
import datetime
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("AccessHistTable")

def post_access(event, context):
    body = json.loads(event.get("body"))
    uri = body.get("uri")
    host = body.get("host")
    uuid = body.get("uuid")

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    id = "".join(random.choices(string.ascii_letters + string.digits, k=12))
    item = {"id": id,
           "uri": uri ,
           "host": host,
           "uuid": uuid,
           "created_at": now,
           }
    table.put_item(Item = item)
    response = {"statusCode": 200 ,
               "body": json.dumps(item)
               }
    return response
