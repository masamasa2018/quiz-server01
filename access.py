import json
import random
import string
import boto3
import datetime
from decimal import Decimal
import os

dynamodb = boto3.resource("dynamodb")
stage = os.environ.get("stage")
if stage == "beta" :
    table = dynamodb.Table("AccessHistTable_beta")
else:
    table = dynamodb.Table("AccessHistTable")

def post_access(event, context):
    body = json.loads(event.get("body"))
    uri = body.get("uri")
    host = body.get("host")
    uid = body.get("uid")

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    id = "".join(random.choices(string.ascii_letters + string.digits, k=12))
    item = {"id": id,
           "uri": uri ,
           "host": host,
           "uid": uid,
           "created_at": now,
           }
    table.put_item(Item = item)
    response = {"statusCode": 200 ,
               "body": json.dumps(item)
               }
    return response
