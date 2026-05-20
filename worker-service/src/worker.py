import boto3
import json
import time
import os

from PIL import Image, ImageDraw

from config import *

# AWS SQS Client
sqs = boto3.client(
    "sqs",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# AWS S3 Client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# Local folders
os.makedirs("temp", exist_ok=True)
os.makedirs("processed", exist_ok=True)

print("Worker started...")

while True:

    response = sqs.receive_message(
        QueueUrl=SQS_QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )

    messages = response.get("Messages", [])

    if not messages:
        print("No messages in queue...")
        time.sleep(5)
        continue

    for message in messages:

        try:
            body = json.loads(message["Body"])

            image_id = body["image_id"]
            s3_key_raw = body["s3_key_raw"]

            print(f"Processing image: {image_id}")

            extension = s3_key_raw.split(".")[-1]

            # Original file path
            local_raw_path = f"temp/{image_id}.{extension}"

            # Always processed as JPG
            local_processed_path = f"processed/{image_id}.jpg"

            # Download raw image from S3
            s3.download_file(
                S3_BUCKET_RAW,
                s3_key_raw,
                local_raw_path
            )

            print("Downloaded image from S3")

            # Open image
            image = Image.open(local_raw_path)

            # Convert to RGB
            image = image.convert("RGB")

            # Resize image
            image = image.resize((150, 150))

            # Add watermark
            draw = ImageDraw.Draw(image)

            draw.text(
                (20, 20),
                ""PropelHQ"",
                fill="red"
            )

            # Save processed image locally as JPG
            image.save(local_processed_path, "JPEG")

            print("Processed image saved locally")

            # Processed image S3 key
            processed_s3_key = f"processed/{image_id}.jpg"

            # Upload processed image to S3
            s3.upload_file(
                local_processed_path,
                S3_BUCKET_PROCESSED,
                processed_s3_key
            )

            print("Processed image uploaded to S3")

            receipt_handle = message["ReceiptHandle"]

            # Delete message from queue
            sqs.delete_message(
                QueueUrl=SQS_QUEUE_URL,
                ReceiptHandle=receipt_handle
            )

            print("Message deleted from queue")

        except Exception as e:
            print("Error:", e)