from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Form
)

from services.cloud_storage import upload_file
from modules.document.repository import save_document_metadata
from modules.version.service import (
    create_new_document,
    create_new_version
)

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
    document_name: str = Form(...),
    is_new_document: bool = Form(...),
    document_group_id: int | None = Form(None)
):

    print("\n========== Upload Request ==========")
    print("document_name:", document_name)
    print("is_new_document:", is_new_document)
    print("document_group_id:", document_group_id)
    print("====================================")


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

    # -----------------------------
    # Version Management
    # -----------------------------
    if is_new_document:

        version_info = create_new_document(document_name)

    else:

        if document_group_id is None:
            raise HTTPException(
                status_code=400,
                detail="document_group_id is required for an existing document."
            )

        version_info = create_new_version(document_group_id)

    # -----------------------------
    # Upload to Google Cloud Storage
    # -----------------------------
    try:
        result = upload_file(file)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Cloud upload failed: {str(e)}"
        )

    # -----------------------------
    # Save metadata
    # -----------------------------
    document_id = save_document_metadata(
        file_name=file.filename,
        file_type=file.content_type,
        file_size=file_size,
        cloud_path=result["blob_name"],
        document_group_id=version_info["document_group_id"],
        version_number=version_info["version_number"],
        is_latest=True
    )

    # -----------------------------
    # Response
    # -----------------------------
    return {
        "message": "File uploaded successfully.",
        "document_id": document_id,
        "document_group_id": version_info["document_group_id"],
        "version_number": version_info["version_number"],
        "data": result
    }