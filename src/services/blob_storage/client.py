from warnings import deprecated
import boto3
import io
# from botocore.client import Config

from config import config

# Replace these with your actual Cloudflare R2 details
ACCESS_KEY_ID = config.cf_access_key_id
SECRET_ACCESS_KEY = config.cf_secret_access_key

ENDPOINT_URL = config.cf_endpoint_url
BUCKET_NAME = config.cf_bucket_name

# Create the boto3 S3 client
# Note the use of `config` to specify signature version 's3v4',
# which is required for R2's S3 compatibility.
r2_client = boto3.client(
    service_name="s3",
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    region_name="auto"
)


@deprecated
def upload_file(file_path):
    """Uploads a file from a local path to R2."""
    r2_client.upload_file(file_path, BUCKET_NAME, "test_key")


def upload_file_object(file_bytes):
    """Uploads an in-memory bytes object to R2."""
    r2_client.upload_fileobj(io.BytesIO(file_bytes), BUCKET_NAME, "test_key")
