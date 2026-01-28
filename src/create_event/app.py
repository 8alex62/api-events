import json
import boto3
import os
import uuid
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
      
        if not body.get('title') or not body.get('date'):
            logger.warning(f"Validation Error: Missing title or date. Body: {body}")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Fields 'title' and 'date' are required."}),
                "headers": {"Content-Type": "application/json"}
            }

        item = {
            'eventId': str(uuid.uuid4()),
            'title': body['title'],
            'date': body['date'],
            'location': body.get('location', ''),
            'description': body.get('description', ''),
            'createdAt': datetime.utcnow().isoformat(),
            'updatedAt': datetime.utcnow().isoformat()
        }

        table.put_item(Item=item)
        logger.info(f"Event created successfully: {item['eventId']}")

        return {
            "statusCode": 201,
            "body": json.dumps(item),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        logger.error(f"Internal Error: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"}),
            "headers": {"Content-Type": "application/json"}
        }
