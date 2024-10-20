import logging
import os
from datetime import datetime
from S3requesthandler import S3RequestHandler
from Dynamodbrequesthandler import DynamoDBRequestHandler
import argparse

log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'
log_file_path = os.path.join(log_dir, log_filename)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
                    handlers=[
                        logging.FileHandler(log_file_path),  # Log to the file with today's date
                        logging.StreamHandler()  # Also log to console
                    ])

parser = argparse.ArgumentParser(description="Process source and target S3 bucket names and DynamoDB table name.")
parser.add_argument('-ss', '--storage', type=str, required=True, help="Storage Strategy (S3 or DynamoDB).")
parser.add_argument('-rb', '--source', type=str, required=True, help="The name of the request S3 bucket.")
parser.add_argument('-wb', '--target', type=str, default=None, required=False, help="The name of the widgets S3 bucket.")
parser.add_argument('-dt', '--dynamodb', type=str, default=None, required=False, help="The name of the DynamoDB table.")
args = parser.parse_args()

storage = args.storage
request_bucket = args.source
widget_bucket = args.target
table_name = args.dynamodb

def main():
    if storage == "S3":
        if widget_bucket:
            logging.info(f"Processing S3 requests with widget bucket: {widget_bucket}")
            s3_handler = S3RequestHandler(widget_bucket)
            s3_handler.process_requests(request_bucket)
        else:
            logging.error("Widget Bucket name is required for S3 storage")
    elif storage == "DynamoDB":
        if table_name:
            logging.info(f"Processing DynamoDB requests with table: {table_name}")
            dynamodb_handler = DynamoDBRequestHandler(table_name)
            dynamodb_handler.process_requests(request_bucket)
        else:
            logging.error("DynamoDB table name is required for DynamoDB storage")
    else:
        logging.error("Invalid storage strategy. Please provide either 'S3' or 'DynamoDB'.")

if __name__ == "__main__":
    main()
