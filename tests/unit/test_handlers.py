import json
import os
import boto3
import pytest
from moto import mock_dynamodb

os.environ['TABLE_NAME'] = 'Events-Test'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

from src.create_event import app as create_app
from src.get_events import app as list_app
from src.get_event_by_id import app as get_one_app

@pytest.fixture
def dynamodb_table():
    """Simule DynamoDB en mémoire (gratuit et rapide)"""
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.create_table(
            TableName='Events-Test',
            KeySchema=[{'AttributeName': 'eventId', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'eventId', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        yield table

# --- Test 1: Création (Success) ---
def test_create_event_success(dynamodb_table):
    payload = {"title": "Test Event", "date": "2026-01-01"}
    event = {"body": json.dumps(payload)}
    response = create_app.handler(event, {})
    assert response['statusCode'] == 201
    assert "eventId" in json.loads(response['body'])

# --- Test 2: Validation Erreur (400) ---
def test_create_event_invalid_payload(dynamodb_table):
    payload = {"description": "Missing title and date"}
    event = {"body": json.dumps(payload)}
    response = create_app.handler(event, {})
    assert response['statusCode'] == 400

# --- Test 3: Get All (Success) ---
def test_get_events(dynamodb_table):
    dynamodb_table.put_item(Item={'eventId': '1', 'title': 'A', 'date': '2026'})
    response = list_app.handler({}, {})
    assert response['statusCode'] == 200
    assert len(json.loads(response['body'])) == 1

# --- Test 4: Get One (Success) ---
def test_get_event_by_id_success(dynamodb_table):
    dynamodb_table.put_item(Item={'eventId': '123', 'title': 'Target', 'date': '2026'})
    event = {"pathParameters": {"id": "123"}}
    response = get_one_app.handler(event, {})
    assert response['statusCode'] == 200
    assert json.loads(response['body'])['title'] == 'Target'

# --- Test 5: Get One Not Found (404) ---
def test_get_event_not_found(dynamodb_table):
    event = {"pathParameters": {"id": "999"}}
    response = get_one_app.handler(event, {})
    assert response['statusCode'] == 404
