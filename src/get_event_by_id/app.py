import json
import boto3
import os
import logging
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def handler(event, context):
    try:
        event_id = event.get('pathParameters', {}).get('id')
        
        if not event_id:
             return {"statusCode": 400, "body": json.dumps({"error": "Missing event ID"})}

        response = table.get_item(Key={'eventId': event_id})
        
        if 'Item' not in response:
            logger.warning(f"Event not found: {event_id}")
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Event not found"}),
                "headers": {"Content-Type": "application/json"}
            }

        item = response['Item']
        logger.info(f"Event retrieved: {event_id}")

        return {
            "statusCode": 200,
            "body": json.dumps(item, cls=DecimalEncoder),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        logger.error(f"Internal Error: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"}),
            "headers": {"Content-Type": "application/json"}
        }
