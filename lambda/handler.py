"""
Gallery App – Lambda Handler
Lists objects in the S3 bucket and returns accessible CloudFront URLs.
"""

import json
import os
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")

BUCKET_NAME       = os.environ["BUCKET_NAME"]
CLOUDFRONT_DOMAIN = os.environ["CLOUDFRONT_DOMAIN"]
IMAGE_EXTENSIONS  = tuple(
    f".{ext.strip().lower()}"
    for ext in os.environ.get("IMAGE_EXTENSIONS", "jpg,jpeg,png,gif,webp,svg").split(",")
)

CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
}


def lambda_handler(event, context):
    """Return JSON list of image objects with CloudFront URLs."""
    try:
        images = list_images()
        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps({"images": images, "count": len(images)}),
        }
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        print(f"S3 ClientError [{error_code}]: {exc}")
        return {
            "statusCode": 502,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Failed to retrieve images from storage."}),
        }
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Unexpected error: {exc}")
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Internal server error."}),
        }


def list_images():
    """
    Paginate through the S3 bucket and collect all image keys.
    Returns a list of dicts: {key, url, size, last_modified}.
    """
    images = []
    paginator = s3.get_paginator("list_objects_v2")

    for page in paginator.paginate(Bucket=BUCKET_NAME):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if not key.lower().endswith(IMAGE_EXTENSIONS):
                continue

            images.append({
                "key": key,
                "url": f"https://{CLOUDFRONT_DOMAIN}/{key}",
                "size": obj["Size"],
                "last_modified": obj["LastModified"].isoformat(),
            })

    return images
