import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client("s3")

    def upload_file(self, file_content: str, bucket_name: str, object_key: str, content_type: str = "text/csv") -> bool:
        try:
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=object_key,
                Body=file_content,
                ContentType=content_type
            )
            logger.info("Successfully uploaded %s to s3://%s/%s", object_key, bucket_name, object_key)
            return True
        except ClientError as e:
            logger.error("Error uploading file to S3: %s", e)
            return False
        except Exception as e:
            logger.error("Unexpected error uploading file to S3: %s", e)
            return False

