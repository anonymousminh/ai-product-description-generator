import json
import logging
import os 
import boto3

from product_generator.services.bedrock_service import BedrockService
from product_generator.utils.description_formatter import DescriptionFormatter

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get the ARN of the StoreDescriptionLambda from environment variables
STORE_DESCRIPTION_LAMBDA_ARN = os.environ.get("STORE_DESCRIPTION_LAMBDA_ARN")

# Initialize Lambda client outside the handler for better performance
lambda_client = boto3.client("lambda")

def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    bedrock_service = BedrockService()
    
    try:
        # Support both API Gateway and direct Lambda console invocation
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event  # For direct Lambda console invocation

        title = body.get("title")
        category = body.get("category")
        features = body.get("features", [])
        audience = body.get("audience")
        format_type = body.get("format", "detailed")
        store_result = body.get("store_result", False)

        if not all([title, category, features, audience]):
            raise ValueError("Missing required product metadata: title, category, features, or audience.")

        features_str = ", ".join(features)
        dynamic_prompt = (
            f"\n\nHuman: Write a product description for a {title} in the {category} category. "
            f"It has the following key features: {features_str}. "
            f"The target audience is {audience}.\n\nAssistant:"
        )

        full_generated_description = bedrock_service.invoke_model(dynamic_prompt)
        logger.info("Full Generated Description: %s", full_generated_description)

        formatter = DescriptionFormatter(full_generated_description)
        
        response_descriptions = {}
        if format_type == "short":
            response_descriptions["short"] = formatter.get_short_description()
        elif format_type == "detailed":
            response_descriptions["detailed"] = formatter.get_detailed_description()
        elif format_type == "social":
            response_descriptions["social"] = formatter.get_social_caption()
        elif format_type == "seo":
            response_descriptions["seo"] = formatter.get_seo_rich_description()
        elif format_type == "all":
            response_descriptions["short"] = formatter.get_short_description()
            response_descriptions["detailed"] = formatter.get_detailed_description()
            response_descriptions["social"] = formatter.get_social_caption()
            response_descriptions["seo"] = formatter.get_seo_rich_description()
            
        else:
            raise ValueError(f"Unsupported format type: {format_type}. Supported: short, detailed, all.")

        # Asynchronously invoke StoreDescriptionLambda
        if store_result and STORE_DESCRIPTION_LAMBDA_ARN:
            try:
                # Prepare payload for StoreDescriptionLambda
                storage_item = {
                    "productId": title.replace(" ", "-").lower(),
                    "timestamp": context.get_remaining_time_in_millis(),
                    "metadata": {
                        "title": title,
                        "category": category,
                        "features": features,
                        "audience": audience
                    },
                    "descriptions": response_descriptions,
                    "formatType": format_type
                }
                # Wrap in 'item' key if that's what StoreDescriptionLambda expects
                storage_payload = {"item": storage_item}

                lambda_client.invoke(
                    FunctionName=STORE_DESCRIPTION_LAMBDA_ARN,
                    InvocationType='Event',
                    Payload=json.dumps(storage_payload)
                )
                logger.info("Asynchronously invoked StoreDescriptionLambda.")
            except Exception as store_e:
                logger.error("Failed to asynchronously invoke StoreDescriptionLambda: %s", store_e)
                

        return {
            'statusCode': 200,
            'body': json.dumps(response_descriptions)
        }
    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body.")
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid JSON in request body.'})
        }
    except ValueError as ve:
        logger.error("Validation Error: %s", ve)
        return {
            'statusCode': 400,
            'body': json.dumps({'message': str(ve)})
        }
    except Exception as e:
        logger.error("Error in Lambda handler: %s", e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Failed to generate description: {e}'
            })
        }

