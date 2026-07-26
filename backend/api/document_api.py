from fastapi import APIRouter, UploadFile, File, HTTPException
from services.cloud_storage import upload_file
from modules.document.repository import save_document_metadata

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

ALLOWED_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain"
]

MAX_FILE_SIZE = 30 * 1024 * 1024   # 30 MB


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    print("Filename:", file.filename)
    print("Content Type:", file.content_type)

    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Only PDF, DOCX and TXT are allowed."
        )

    # Read file to calculate size
    contents = await file.read()
    file_size = len(contents)

    # Validate file size
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds the maximum limit of 30 MB."
        )

    # Reset file pointer before uploading
    file.file.seek(0)

    # Upload to Google Cloud Storage
    try:
        result = upload_file(file)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Cloud upload failed: {str(e)}"
        )

    document_id = save_document_metadata(
    file_name=file.filename,
    file_type=file.content_type,
    file_size=file_size,
    cloud_path=result["blob_name"]
)

    return {
    "success": True,
    "message": "Document uploaded successfully.",
    "document": {
        "id": document_id,
        "name": file.filename,
        "type": file.content_type,
        "size": file_size,
        "status": "Uploaded"
    },
    "storage": {
        "path": result["blob_name"]
    }
}