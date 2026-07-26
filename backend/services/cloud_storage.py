from google.cloud import storage
from fastapi import UploadFile
import uuid
import os

# Initialize Google Cloud Storage Client
client = storage.Client.from_service_account_json(
    "config/service-account.json"
)

# Your bucket name
BUCKET_NAME = "ai-doc-intelligence-rhithika-2026"

bucket = client.bucket(BUCKET_NAME)


def upload_file(file: UploadFile):
    """
    Uploads a file to Google Cloud Storage with a unique filename.
    """

    # Get original file extension (.pdf, .docx, .txt)
    extension = os.path.splitext(file.filename)[1]

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{extension}"

    # Store inside 'documents/' folder in the bucket
    blob_name = f"documents/{unique_filename}"

    # Create blob
    blob = bucket.blob(blob_name)

    # Upload file
    blob.upload_from_file(
        file.file,
        content_type=file.content_type
    )

    return {
        "original_filename": file.filename,
        "blob_name": blob_name,
        "public_url": blob.public_url
    }