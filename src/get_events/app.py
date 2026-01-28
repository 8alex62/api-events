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
        response = table.scan()
        items = response.get('Items', [])
        
        logger.info(f"Retrieved {len(items)} events")

        return {
            "statusCode": 200,
            "body": json.dumps(items, cls=DecimalEncoder),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        logger.error(f"Internal Error: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"}),
            "headers": {"Content-Type": "application/json"}
        }

