import json
import logging
from product_generator.services.bedrock_service import BedrockService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# This is a simple AWS Lambda function that logs a message and returns a JSON response.
def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    bedrock_service = BedrockService()

    simple_prompt = "Write a short product description for a smart coffee maker."

    try:
        body = json.loads(event["body"])

        title = body.get("title")
        category = body.get("category")
        features = body.get("features", [])
        audience = body.get("audience")

        if not title or not category or not features or not audience:
            raise ValueError("Missing required fields: title, category, features or audience.")
        
        # Construct the dynamic prompt
        prompt = (
            f"Write a product description for a {category} called {title}. "
            f"It is designed for {audience} and has the following features: {', '.join(features)}."
        )

        # Invoke the Bedrock service to generate the description
        generated_description = bedrock_service.invoke_model(prompt)
        logger.info("Generated description: %s", generated_description)

        # Return the generated description in the response
        return {
            "statusCode": 200,
            "body": json.dumps({
                "description": generated_description
            })
        }
    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body.")
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid JSON in request body."}),
        }
    except ValueError as ve:
        logger.error("Validation Error: %s", str(ve))
        return {
            "statusCode": 400,
            "body": json.dumps({"message": str(ve)}),
        }
    except Exception as e:
        logger.error("Error in Lambda handler: %s", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Failed to generate product description."}),
        }
