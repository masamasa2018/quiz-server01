import json
import random
import string
import boto3
import datetime
from decimal import Decimal
from boto3.dynamodb.conditions import Key
import os

#DB、テーブルの定義
dynamodb = boto3.resource("dynamodb")
stage = os.environ.get("stage")
if stage == "beta" :
    table = dynamodb.Table("QuizLike" + "_beta")
else:
    table = dynamodb.Table("QuizLike")

#LIKEのinsert API
def post_like(event, context):
    body = json.loads(event.get("body"))
    category = body.get("category")
    code = body.get("code")
    uid = body.get("uid")

    rec = _get_like_by_uid(category,code,uid)
    
    if len(rec) == 0:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        id = generate_id()
        item = {"id": id,
            "code": code ,
            "category": category,
            "uid": uid ,
            "created_at": now,
            }
        table.put_item(Item = item)
        response = {"statusCode": 200 ,
                "body": json.dumps(item)
                }
        return response

#LIKEの削除API
def delete_like(event, context):
    body = json.loads(event.get("body"))
    category = body.get("category")
    code = body.get("code")
    uid = body.get("uid")
    result = _get_like_by_uid(category, code, uid)
    first_id = result[0]['id']
    result = table.delete_item(Key={"id": first_id})
    return result

#ID生成
def generate_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k=12))

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

#LIKEのcategory,code,UIDごとのカウント数取得処理
def _get_like_by_uid(category, code, uid):
    response = table.scan(
        FilterExpression='category=:category and code=:code and uid=:uid',
        ExpressionAttributeValues={
            ':category': int(category),
            ':code': int(code),
            ':uid': uid,
        }
    )
    items = response['Items']
    return items

#LIKEの category,code カウント数取得処理
def _get_like(category, code):
    response = table.scan(
        FilterExpression='category=:category and code=:code',
        ExpressionAttributeValues={
            ':category': int(category),
            ':code': int(code),
        }
    )
    items = response['Items']
    return len(items)

#LIKEのカウント数取得
def get_like_count(event, context):
    category = event["pathParameters"]["category"]
    code = event["pathParameters"]["code"]
    result = _get_like(category, code)
    return result

#LIKEのuidごとのカウント数取得
def get_like_count_by_uid(event, context):
    category = event["pathParameters"]["category"]
    code = event["pathParameters"]["code"]
    uid = event["pathParameters"]["uid"]
    result = _get_like_by_uid(category, code , uid)
    isExist = False
    if(len(result) > 0) :
        isExist = True
    print(isExist)
    return isExist

#LIKEの取得API（category、IDごとのカウント数）
def get_like(event, context):
    category = event["pathParameters"]["category"]
    code = event["pathParameters"]["code"]
    uid = event["pathParameters"]["uid"]
    result = _get_like_by_uid(category, code, uid)

    return result


def put_quiz(event, context):
    id = event["pathParameters"]["id"]
    body = json.loads(event.get("body"))
    category = body.get("category")
    code = body.get("code")
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
