import json
import boto3
import os
import uuid
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

bucket_name = os.environ['BUCKET_NAME']
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def handler(event, context):
    event_id = event.get('pathParameters', {}).get('id')
    
    if not event_id:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing event ID"})}

    # 1. Génération d'une clé unique pour l'image
    # Format: events/{event_id}/{random}.jpg
    image_key = f"events/{event_id}/{uuid.uuid4()}.jpg"

    try:
        # 2. Génération de l'URL Présignée (Presigned URL)
        # Expiration: 300 secondes (5 min) comme demandé dans le TP
        upload_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket_name,
                'Key': image_key,
                'ContentType': 'image/jpeg' # On force le type pour simplifier
            },
            ExpiresIn=300
        )

        # 3. Mise à jour de l'événement en base pour lier l'image
        # On utilise update_item pour ne pas écraser tout l'objet
        table.update_item(
            Key={'eventId': event_id},
            UpdateExpression="set imageKey = :k, updatedAt = :t",
            ExpressionAttributeValues={
                ':k': image_key,
                ':t': str(uuid.uuid4()) # Placeholder date, ou datetime.utcnow().isoformat()
            },
            ConditionExpression="attribute_exists(eventId)" # Vérifie que l'event existe
        )

        logger.info(f"Presigned URL generated for event {event_id}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "uploadUrl": upload_url,
                "imageKey": image_key
            }),
            "headers": {"Content-Type": "application/json"}
        }

    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
             return {"statusCode": 404, "body": json.dumps({"error": "Event not found"})}
        
        logger.error(f"Error: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": "Internal Server Error"})}
