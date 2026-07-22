import os
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

bucket_name = os.getenv("GCS_BUCKET_NAME")

client = storage.Client()
bucket = client.bucket(bucket_name)


def upload_file(file):
    """
    Upload a file to Google Cloud Storage.
    """

    blob = bucket.blob(file.filename)

    blob.upload_from_file(
        file.file,
        content_type=file.content_type
    )

    return {
        "file_name": file.filename,
        "blob_name": blob.name,
        "bucket": bucket.name
    }