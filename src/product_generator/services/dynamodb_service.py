import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DynamoDBService:
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)

    def put_item(self, item: dict) -> bool:
        try:
            response = self.table.put_item(Item=item)
            logger.info("Successfully put item into DynamoDB: %s", response)
            return True
        except ClientError as e:
            logger.error("Error putting item into DynamoDB: %s", e)
            return False
        except Exception as e:
            logger.error("Unexpected error putting item into DynamoDB: %s", e)
            return False

