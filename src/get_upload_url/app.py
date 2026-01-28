import json
import boto3
import os
import logging
from botocore.config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# --- CORRECTIF : ON FORCE L'ENDPOINT ---
# On définit explicitement l'URL du serveur S3 de Stockholm (eu-north-1)
# Cela oblige la Lambda a signer pour CETTE adresse précise.
REGION = "eu-north-1"
ENDPOINT = f"https://s3.{REGION}.amazonaws.com"

s3_client = boto3.client(
    's3', 
    region_name=REGION,
    endpoint_url=ENDPOINT,  # <--- C'est la ligne magique qui résout ton problème
    config=Config(signature_version='s3v4')
)

bucket_name = os.environ.get('BUCKET_NAME')

def handler(event, context):
    event_id = event.get('pathParameters', {}).get('id')
    
    if not event_id:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing event ID"})}

    # On force l'extension .jpg pour correspondre à ton test Postman
    object_key = f"events/{event_id}/image.jpg"

    try:
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_key,
                'ContentType': 'image/jpeg'
            },
            ExpiresIn=300
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "uploadUrl": url, # Cette URL contiendra MAINTENANT 'eu-north-1'
                "key": object_key
            }),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        logger.error(f"Error generating URL: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Could not generate upload URL"})
        }
