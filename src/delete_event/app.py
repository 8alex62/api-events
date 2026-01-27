import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def handler(event, context):
    event_id = event.get('pathParameters', {}).get('id')
    
    if not event_id:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing event ID"})}

    try:
        # Suppression de l'item
        # Note: DynamoDB delete_item ne renvoie pas d'erreur si l'item n'existe pas déjà,
        # ce qui est standard pour un DELETE idempotent.
        table.delete_item(Key={'eventId': event_id})
        
        logger.info(f"Event deleted: {event_id}")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Event deleted successfully"}),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        logger.error(f"Internal Error: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"}),
            "headers": {"Content-Type": "application/json"}
        }
