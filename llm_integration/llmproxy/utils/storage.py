import os
import pathlib
from typing import BinaryIO

import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError


def s3_is_configured() -> bool:
    return bool(os.getenv("AWS_S3_BUCKET"))


def upload_file(file_obj: BinaryIO, filename: str) -> str:
    """
    Upload file to S3 if configured; otherwise save under local `files/uploads/`.
    Returns a URL or local path string.
    """
    bucket = os.getenv("AWS_S3_BUCKET")
    region = os.getenv("AWS_S3_REGION", "ap-northeast-2")

    if bucket:
        try:
            s3 = boto3.client(
                "s3",
                region_name=region,
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )
            key = f"uploads/{filename}"
            s3.upload_fileobj(file_obj, bucket, key, ExtraArgs={"ACL": "public-read"})
            return f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
        except (BotoCoreError, NoCredentialsError):
            pass  # fall through to local

    # local fallback
    base = pathlib.Path("files/uploads")
    base.mkdir(parents=True, exist_ok=True)
    dest = base / filename
    # Reset read pointer if necessary
    if hasattr(file_obj, "seek"):
        file_obj.seek(0)
    with open(dest, "wb") as out:
        out.write(file_obj.read())
    return f"/files/uploads/{filename}"

