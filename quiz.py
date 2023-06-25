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
    table = dynamodb.Table("QuizTable_beta")
else:
    table = dynamodb.Table("QuizTable")

def post_quiz(event, context):
    body = json.loads(event.get("body"))
    category = body.get("category")
    code = body.get("code")

    question = body.get("question")
    answers = body.get("answers")
    correct_code = body.get("correct_code")
    info = body.get("info")
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    id = generate_id()
    item = {"id": id,
           "code": code ,
           "category": category,
           "question": question,
           "answers": answers,
           "correct_code": correct_code,
           "info": info,
           "created_at": now,
           }
    table.put_item(Item = item)
    response = {"statusCode": 200 ,
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": '*'
               }
    return response

def generate_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k=12))

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def get_all_quiz(event, context):

    response = table.scan()
    items = response.get("Items")

    response = {"statusCode": 200, "body": json.dumps(items, default=decimal_default)}
    return response

def get_quiz(event, context):
    id = event["pathParameters"]["id"]
    res = table.get_item(Key={"id": id})
    
    item = res.get("Item")
    response = {"statusCode": 200, "body": json.dumps(item)}
    return response

def delete_quiz(event, context):
    id = event["pathParameters"]["id"]
    table.delete_item(Key={"id": id})
    response = {"statusCode": 200, "body": json.dumps({"id": id})}
    return response

def put_quiz(event, context):
    id = event["pathParameters"]["id"]
    body = json.loads(event.get("body"))
    code = body.get("code")
    category = body.get("category")
    
    question = body.get("question")
    answers = body.get("answers")
    correct_code = body.get("correct_code")
    info = body.get("info")
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    item = {
           "category": category,
           "code": code ,
           "question": question,
           "answers": answers,
           "correct_code": correct_code,
           "info": info
           }
    table.update_item(
        Key={"id": id},
        UpdateExpression="set code=:code,question=:question,category=:category,answers=:answers,correct_code=:correct_code,info=:info,updated_at=:updated_at",
        ExpressionAttributeValues={":code": code,":question": question,":category": category, ":answers": answers,  ":correct_code": correct_code,  ":info": info, ":updated_at": now},
    )
    response = {"statusCode": 200, "body": json.dumps(item)}
    return response
