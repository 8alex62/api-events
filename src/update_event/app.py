import json
import boto3
import os
import logging
from datetime import datetime
from decimal import Decimal

# Configuration des logs
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
        # 1. Vérification de l'ID
        event_id = event.get('pathParameters', {}).get('id')
        if not event_id:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing event ID"})}

        # 2. Parsing du Body
        body_str = event.get('body', '{}') or '{}'
        body = json.loads(body_str)
        
        # Validation des champs obligatoires
        if not body.get('title') or not body.get('date'):
            return {"statusCode": 400, "body": json.dumps({"error": "Title and date are required"})}

        # 3. Mise à jour DynamoDB avec ALIAS pour 'date' et 'location'
        response = table.update_item(
            Key={'eventId': event_id},
            # Note l'utilisation de #l au lieu de location
            UpdateExpression="SET title = :t, #d = :d, #l = :l, description = :desc, updatedAt = :u",
            ExpressionAttributeNames={
                '#d': 'date',     # 'date' est un mot réservé
                '#l': 'location'  # 'location' est AUSSI un mot réservé
            },
            ExpressionAttributeValues={
                ':t': body['title'],
                ':d': body['date'],
                ':l': body.get('location', ''),
                ':desc': body.get('description', ''),
                ':u': datetime.utcnow().isoformat()
            },
            ReturnValues="ALL_NEW",
            ConditionExpression="attribute_exists(eventId)"
        )

        return {
            "statusCode": 200,
            "body": json.dumps(response['Attributes'], cls=DecimalEncoder),
            "headers": {"Content-Type": "application/json"}
        }

    except boto3.exceptions.botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {"statusCode": 404, "body": json.dumps({"error": "Event not found"})}
        logger.error(f"DynamoDB Error: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
        
    except Exception as e:
        logger.error(f"CRITICAL PYTHON ERROR: {str(e)}", exc_info=True)
        return {
            "statusCode": 500, 
            "body": json.dumps({"error": f"Critical Error: {str(e)}"}) 
        }
