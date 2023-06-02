import json
import random
import string
import boto3
import datetime
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("InqueryHistTable")

def post_inquery(event, context):
    body = json.loads(event.get("body"))
    name = body.get("name")
    message = body.get("message")
    email = body.get("email")

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    id = "".join(random.choices(string.ascii_letters + string.digits, k=12))
    item = {"id": id,
           "name": name,
           "email": email, 
           "message": message,
           "created_at": now,
           }
    table.put_item(Item = item)
    response = {"statusCode": 200 ,
               "body": json.dumps(item)
               }
    return response
