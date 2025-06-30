import json
import logging
import os
import csv
from io import StringIO
from datetime import datetime

from product_generator.services.dynamodb_service import DynamoDBService
from product_generator.services.s3_service import S3Service

logger = logging.getLogger()
logger.setLevel(logging.INFO)

PRODUCT_DESCRIPTIONS_TABLE = os.environ.get("PRODUCT_DESCRIPTIONS_TABLE")
EXPORTS_S3_BUCKET = os.environ.get("EXPORTS_S3_BUCKET")

def lambda_handler(event, context):
    logger.info("Received event for CSV export: %s", json.dumps(event))

    if not PRODUCT_DESCRIPTIONS_TABLE or not EXPORTS_S3_BUCKET:
        logger.error("Environment variables for DynamoDB table or S3 bucket not set.")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Configuration error: DynamoDB table or S3 bucket not set.'})
        }

    dynamodb_service = DynamoDBService(PRODUCT_DESCRIPTIONS_TABLE)
    s3_service = S3Service()

    try:
        # Fetch all items from DynamoDB (for simplicity; for large tables, use pagination)
        # Note: This is a full table scan, which can be expensive for large tables.
        # In a real application, you might filter by a specific productId or use a query.
        response = dynamodb_service.table.scan() # Accessing table directly for scan
        items = response.get('Items', [])
        logger.info("Fetched %d items from DynamoDB.", len(items))

        if not items:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'No descriptions found to export.'})
            }

        # Prepare CSV data
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)

        # Define CSV headers - adjust based on what you want in your CSV
        # This example flattens the 'descriptions' dictionary
        headers = ["productId", "timestamp", "title", "category", "features", "audience", "short_description", "detailed_description", "social_caption", "seo_description"]
        csv_writer.writerow(headers)

        for item in items:
            row = [
                item.get("productId", ""),
                item.get("timestamp", ""),
                item.get("metadata", {}).get("title", ""),
                item.get("metadata", {}).get("category", ""),
                ", ".join(item.get("metadata", {}).get("features", [])),
                item.get("metadata", {}).get("audience", ""),
                item.get("descriptions", {}).get("short", ""),
                item.get("descriptions", {}).get("detailed", ""),
                item.get("descriptions", {}).get("social", ""),
                item.get("descriptions", {}).get("seo", "")
            ]
            csv_writer.writerow(row)

        csv_content = csv_buffer.getvalue()
        
        # Define S3 object key
        timestamp_str = datetime.now().strftime("%Y%m%d-%H%M%S")
        object_key = f"product_descriptions_export_{timestamp_str}.csv"

        # Upload to S3
        success = s3_service.upload_file(csv_content, EXPORTS_S3_BUCKET, object_key)

        if success:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'CSV exported successfully to S3.',
                    'bucket': EXPORTS_S3_BUCKET,
                    'key': object_key,
                    'url': f"https://{EXPORTS_S3_BUCKET}.s3.amazonaws.com/{object_key}"
                } )
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Failed to upload CSV to S3.'})
            }

    except Exception as e:
        logger.error("Error in ExportDescriptionLambda handler: %s", e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Failed to perform CSV export: {e}'
            })
        }

