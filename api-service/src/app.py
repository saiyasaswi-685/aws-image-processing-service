import json
import boto3
from config import *

from flask import Flask, request, jsonify
from PIL import Image
import uuid

app = Flask(__name__)

# AWS S3 Client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# AWS SQS Client
sqs = boto3.client(
    "sqs",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return jsonify({
        "message": "API Service Running"
    })


@app.route("/images/upload", methods=["POST"])
def upload_image():

    # Check image exists
    if "image" not in request.files:
        return jsonify({
            "error": "No image file provided"
        }), 400

    image_file = request.files["image"]

    # Empty filename check
    if image_file.filename == "":
        return jsonify({
            "error": "Empty filename"
        }), 400

    # File extension validation
    if not allowed_file(image_file.filename):
        return jsonify({
            "error": "Invalid image type"
        }), 400

    try:
        # Validate image
        Image.open(image_file)

        # Unique image ID
        image_id = str(uuid.uuid4())

        # File extension
        extension = image_file.filename.rsplit(".", 1)[1].lower()

        # S3 path
        s3_key = f"original/{image_id}.{extension}"

        # Reset file pointer
        image_file.seek(0)

        # Upload original image to S3
        s3.upload_fileobj(
            image_file,
            S3_BUCKET_RAW,
            s3_key
        )

        # Create SQS message
        message = {
            "image_id": image_id,
            "s3_key_raw": s3_key
        }

        # Send message to SQS
        sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(message)
        )

        return jsonify({
            "message": "Image uploaded to S3 and queued for processing",
            "image_id": image_id,
            "s3_key": s3_key
        }), 202

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# GET Processed Image URL
@app.route("/images/<image_id>")
def get_processed_image(image_id):

    processed_image_url = (
        f"https://{S3_BUCKET_PROCESSED}.s3."
        f"{AWS_REGION}.amazonaws.com/"
        f"processed/{image_id}.jpg"
    )

    return jsonify({
        "image_id": image_id,
        "processed_image_url": processed_image_url
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)