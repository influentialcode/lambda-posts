from moto import mock_dynamodb2
from moto import mock_s3
import boto3
from lambda_handler import db_contains_post
from lambda_handler import get_object

REGION_NAME = 'us-east-1'


@mock_dynamodb2
def test_contains_post():
    dynamodb = boto3.resource('dynamodb', region_name=REGION_NAME)

    table = dynamodb.create_table(
        TableName='posts',
        KeySchema=[
            {
                'AttributeName': 'title',
                'KeyType': 'HASH'  # primary key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.put_item(
        Item={
            'title': 'The Best Post in the World',
            'tags': [
                'dogs',
                'cats',
                'horses',
            ],
            'text': 'This is how you write the best post in the world...'
        }
    )

    table.put_item(
        Item={
            'title': 'The Best Post in the World Part 2',
            'tags': [
                'dogs',
                'cats',
                'horses',
                'unicorns',
            ],
            'text': 'This is also how you write the best post in the world...'
        }
    )

    table.put_item(
        Item={
            'title': 'The Best Post in the World Part 3',
            'tags': [
                'horses',
                'unicorns',
            ],
            'text': 'This is also how you write the best post in the world...'
        }
    )

    assert not db_contains_post(table, 'Some other post title')
    assert db_contains_post(table, 'The Best Post in the World Part 2')


@mock_s3
def test_get_object():
    s3 = boto3.resource('s3')
    bucket_name = 'input.influentialcode.com'
    bucket = s3.create_bucket(Bucket=bucket_name)
    key = '/posts/2018/some-title-here.html'
    bucket.put_object(
        Key=key,
        Body=b'The post body.'
    )

    retrieved_object = get_object(key, bucket_name)
    assert retrieved_object is not None
    assert retrieved_object['Body'].read().decode('utf-8') == 'The post body.'
