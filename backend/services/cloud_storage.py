from fastapi import UploadFile
import uuid
import os
import shutil

# -----------------------------
# Check if Google Cloud is available
# -----------------------------

SERVICE_ACCOUNT_PATH = "config/service-account.json"

USE_GCP = os.path.exists(SERVICE_ACCOUNT_PATH)

if USE_GCP:
    from google.cloud import storage

    client = storage.Client.from_service_account_json(
        SERVICE_ACCOUNT_PATH
    )

    BUCKET_NAME = "ai-doc-intelligence-rhithika-2026"
    bucket = client.bucket(BUCKET_NAME)

# -----------------------------
# Upload Function
# -----------------------------

def upload_file(file: UploadFile):

    extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{extension}"

    # -----------------------------
    # Google Cloud Upload
    # -----------------------------
    if USE_GCP:

        blob_name = f"documents/{unique_filename}"

        blob = bucket.blob(blob_name)

        blob.upload_from_file(
            file.file,
            content_type=file.content_type
        )

        return {
            "storage": "Google Cloud Storage",
            "original_filename": file.filename,
            "blob_name": blob_name,
            "public_url": blob.public_url
        }

    # -----------------------------
    # Local Upload
    # -----------------------------
    else:

        upload_folder = "uploads"

        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, unique_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "storage": "Local Storage",
            "original_filename": file.filename,
            "blob_name": file_path,
            "public_url": None
        }