import json
import logging
from product_generator.services.bedrock_service import BedrockService
from product_generator.utils.description_formatter import DescriptionFormatter

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    bedrock_service = BedrockService()

    try:
        body = json.loads(event["body"])
        
        title = body.get("title")
        category = body.get("category")
        features = body.get("features", [])
        audience = body.get("audience")
        format_type = body.get("format", "detailed") # Default to detailed if not specified

        if not all([title, category, features, audience]):
            raise ValueError("Missing required product metadata: title, category, features, or audience.")

        features_str = ", ".join(features)
        dynamic_prompt = (
            f"\n\nHuman: Write a product description for a {title} in the {category} category. "
            f"It has the following key features: {features_str}. "
            f"The target audience is {audience}.\n\nAssistant:"
        )

        full_generated_description = bedrock_service.invoke_claude(dynamic_prompt)
        logger.info("Full Generated Description: %s", full_generated_description)

        formatter = DescriptionFormatter(full_generated_description)
        
        response_descriptions = {}
        if format_type == "short":
            response_descriptions["short"] = formatter.get_short_description()
        elif format_type == "detailed":
            response_descriptions["detailed"] = formatter.get_detailed_description()
        elif format_type == "all": # Option to generate all formats
            response_descriptions["short"] = formatter.get_short_description()
            response_descriptions["detailed"] = formatter.get_detailed_description()
            # Add social and SEO here on Day 10
        else:
            raise ValueError(f"Unsupported format type: {format_type}. Supported: short, detailed, all.")

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

