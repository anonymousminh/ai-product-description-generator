import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# This is a simple AWS Lambda function that logs a message and returns a JSON response.
def lambda_handler(event, context):
    logger.info("Hello from lambda!")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello from lambda!",
            "input": event
        })
    }

if __name__ == '__main__':
    test_event = {"sample": "data"}
    response = lambda_handler(test_event, None)
    print(response)