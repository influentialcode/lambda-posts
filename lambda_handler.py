import logging
import boto3

from boto3.dynamodb.conditions import Key


logger = logging.getLogger('posts')
logger.setLevel(logging.INFO)


def handler(event, context):
    pass


def get_object(key: str, bucket_name: str) -> dict:
    s3 = boto3.resource('s3')
    return s3.Object(bucket_name, key).get()


def db_contains_post(table, title: str) -> bool:
    response = table.query(
        ProjectionExpression="title",
        KeyConditionExpression=Key('title').eq(title)
    )

    return response['Count'] == 1
