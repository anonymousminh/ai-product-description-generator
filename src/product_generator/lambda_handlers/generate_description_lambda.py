import json
import logging
from product_generator.services.bedrock_service import BedrockService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# This is a simple AWS Lambda function that logs a message and returns a JSON response.
def lambda_handler(event, context):
    logger.info("Received event: %s", event)

    bedrock_service = BedrockService()

    simple_prompt = "Write a short product description for a smart coffee maker."

    try:
        response = bedrock_service.invoke_model(simple_prompt)
        logger.info("Model response: %s", response)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Product description generated successfully.",
                "description": response
            })
        }
    except Exception as e:
        logger.error("Error invoking model: %s", e)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Failed to generate product description.",
                "error": str(e)
            })
        }
    
