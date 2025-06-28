import json
import logging
import os
from product_generator.services.dynamodb_service import DynamoDBService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get table name from environment variables (set in template.yaml)
PRODUCT_DESCRIPTIONS_TABLE = os.environ.get("PRODUCT_DESCRIPTIONS_TABLE")

def lambda_handler(event, context):
    logger.info("Received event for storing description: %s", json.dumps(event))

    if not PRODUCT_DESCRIPTIONS_TABLE:
        logger.error("PRODUCT_DESCRIPTIONS_TABLE environment variable not set.")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'DynamoDB table name not configured.'})
        }

    dynamodb_service = DynamoDBService(PRODUCT_DESCRIPTIONS_TABLE)

    try:
        # Assuming the event directly contains the item to be stored
        # For example: {"productId": "P123", "formatType": "detailed", "description": "..."}
        item_to_store = event # In a real scenario, you'd parse and validate this event

        if not all(k in item_to_store for k in ["productId", "formatType", "description"]):
            logger.error("Invalid item structure for storage: %s", item_to_store)
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid item structure. Requires productId, formatType, description.'})
            }

        success = dynamodb_service.put_item(item_to_store)

        if success:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Description stored successfully.'})
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Failed to store description.'})
            }
    except Exception as e:
        logger.error("Error in StoreDescriptionLambda handler: %s", e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Failed to process storage request: {e}'
            })
        }

