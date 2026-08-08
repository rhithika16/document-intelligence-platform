from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Form
)

from services.cloud_storage import upload_file
from modules.document.repository import save_document_metadata
from modules.version.service import get_version_information


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
async def upload_document(
    file: UploadFile = File(...),
    document_name: str = Form(...)
):

    print("\n========== Upload Request ==========")
    print("document_name:", document_name)
    print("filename:", file.filename)
    print("content_type:", file.content_type)
    print("====================================")

    # ---------------------------------
    # Validate file type
    # ---------------------------------

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Only PDF, DOCX and TXT are allowed."
        )

    # ---------------------------------
    # Read file and calculate size
    # ---------------------------------

    contents = await file.read()
    file_size = len(contents)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds the maximum limit of 30 MB."
        )

    # Reset file pointer
    file.file.seek(0)

    # ---------------------------------
    # Version Management
    # ---------------------------------

    try:

        version_info = get_version_information(document_name)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Version management failed: {str(e)}"
        )

    # ---------------------------------
    # Upload file to storage
    # ---------------------------------

    try:

        result = upload_file(file)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"File upload failed: {str(e)}"
        )

    # ---------------------------------
    # Save document metadata
    # ---------------------------------

    try:

        document_id = save_document_metadata(
            file_name=file.filename,
            file_type=file.content_type,
            file_size=file_size,
            cloud_path=result["blob_name"],
            document_group_id=version_info["document_group_id"],
            version_number=version_info["version_number"],
            is_latest=True
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save document metadata: {str(e)}"
        )

    # ---------------------------------
    # Response
    # ---------------------------------

    return {
        "message": "File uploaded successfully.",
        "document_id": document_id,
        "document_name": document_name,
        "document_group_id": version_info["document_group_id"],
        "version_number": version_info["version_number"],
        "is_new_document": version_info["is_new_document"],
        "data": result
    }