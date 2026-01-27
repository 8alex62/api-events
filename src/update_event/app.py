import json
import boto3
import os
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def handler(event, context):
    # 1. Récupération de l'ID
    event_id = event.get('pathParameters', {}).get('id')
    if not event_id:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing event ID"})}

    try:
        # 2. Parsing et Validation
        body = json.loads(event.get('body', '{}'))
        
        # On impose la présence des champs principaux pour la mise à jour
        if not body.get('title') or not body.get('date'):
            return {"statusCode": 400, "body": json.dumps({"error": "Title and date are required"})}

        # 3. Mise à jour DynamoDB
        # On met à jour title, date, location, description et updatedAt
        # On ne touche PAS à eventId, createdAt ni imageKey
        response = table.update_item(
            Key={'eventId': event_id},
            UpdateExpression="SET title = :t, #d = :d, location = :l, description = :desc, updatedAt = :u",
            ExpressionAttributeNames={
                '#d': 'date'  # 'date' est un mot réservé DynamoDB
            },
            ExpressionAttributeValues={
                ':t': body['title'],
                ':d': body['date'],
                ':l': body.get('location', ''),
                ':desc': body.get('description', ''),
                ':u': datetime.utcnow().isoformat()
            },
            ReturnValues="ALL_NEW", # On retourne l'objet modifié
            ConditionExpression="attribute_exists(eventId)" # Échoue si l'ID n'existe pas
        )

        logger.info(f"Event updated: {event_id}")

        return {
            "statusCode": 200,
            "body": json.dumps(response['Attributes'], default=str),
            "headers": {"Content-Type": "application/json"}
        }

    except boto3.exceptions.botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {"statusCode": 404, "body": json.dumps({"error": "Event not found"})}
        logger.error(str(e))
        return {"statusCode": 500, "body": json.dumps({"error": "Internal Error"})}
