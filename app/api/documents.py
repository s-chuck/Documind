import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Query, status
from sqlalchemy.orm import Session
import filetype 
from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.user import User
from app.schema.document import DocumentListResponse, DocumentResponse, DocumentStatusUpdate
from app.services.chunk_service import save_chunks
from app.services.chunker import chunk_text
from app.services.document_processor import extract_text
from io import BytesIO
from zipfile import ZipFile, BadZipFile
from app.schema.document import DocumentSearchRequest
from app.services.search_service import search_similar_chunks

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)
#Path is relative to from where we are starting our application from , not where we are defineing our Path()
#so the directory will get created at root uvicorn app.main:app --reload
BASE_DIR = Path(__file__).resolve().parents[2]
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(exist_ok=True)

#a .docx file is a zipped file so when we do if extension == detected_extension it will return false that's 
#why this additional step of recognising an .docx file.
def is_valid_docx(contents: bytes) -> bool:
    try:
        with ZipFile(BytesIO(contents)) as zip_file:
            names = set(zip_file.namelist())

            return (
                "[Content_Types].xml" in names
                and "word/document.xml" in names
            )

    except BadZipFile:
        return False


@router.get("/",response_model=DocumentListResponse)
def get_document(
    page: int = Query(1, ge=1), #page >= 1 ge(greater than equal to default value is 1 if client doesn't provide one)
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = (db.query(Document).filter(Document.user_id == current_user.id))
    total = query.count()
    offset = (page-1) * limit

    documents = (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return {
        "items": documents,
        "page": page,
        "limit": limit,
        "total": total,
    }

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == current_user.id,
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return document


# @router.post("/")
# def upload_document(
#     file: UploadFile = File(...),
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     extension = Path(file.filename).suffix.lower()

#     if extension not in ALLOWED_EXTENSIONS:
#         raise HTTPException(
#             status_code=400,
#             detail="Unsupported file type"
#         )
#     #Here see we are not directly storing the value we are first putting uuid in it 
#     #it's because for safety suppose if any malicious user came and put some malicious code in place of filename
#     #That's why it's important to get the storage_key and using it store the file.
#     storage_key = f"{uuid.uuid4()}_{file.filename}"

#     file_path = STORAGE_DIR / storage_key

#     with file_path.open("wb") as buffer:
#         buffer.write(file.file.read())

#     now = datetime.now(timezone.utc)

#     document = Document(
#         user_id=current_user.id,
#         name=file.filename,
#         storage_key=storage_key,
#         status="PROCESSING",
#         created_at=now,
#         updated_at=now,
#     )

#     db.add(document)
#     db.commit()
#     db.refresh(document)

#     return {
#         "id": document.id,
#         "name": document.name,
#         "status": document.status,
#     }

@router.post("/")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    # 1. Check that a filename exists
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )
    # 2. Check the filename extension
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )
    # 3. Read the actual file contents
    contents = await file.read()
    # 4. Detect the actual file type from its bytes
    if extension == ".docx":

        if not is_valid_docx(contents):
            raise HTTPException(
                status_code=400,
                detail="File extension does not match file contents"
            )
    else:
        kind = filetype.guess(contents)
        # filetype could not identify the file
        if kind is None:

            # TXT files often don't have a distinctive
            # binary signature, so handle them separately.
            if extension == ".txt":
                detected_extension = ".txt"
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Could not determine file type"
                )

        else:
            detected_extension = f".{kind.extension}"
        # 5. Make sure filename matches actual contents
        if detected_extension != extension:
            raise HTTPException(
                status_code=400,
                detail="File extension does not match file contents"
            )
    # 6. Make sure our file pointer is back at the start
    await file.seek(0)
    # 7. Generate a unique storage name
    storage_key = f"{uuid.uuid4()}{extension}"

    file_path = STORAGE_DIR / storage_key
    # 8. Save the file
    await file.seek(0)

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty",
        )

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    saved_size = file_path.stat().st_size

    print(
        f"Uploaded size: {len(contents)} bytes | "
        f"Saved size: {saved_size} bytes"
    )

    if saved_size != len(contents):
        raise HTTPException(
            status_code=500,
            detail="File was not saved correctly",
        )
    # 9. Create database record
    document = Document(
        user_id=current_user.id,
        name=file.filename,
        storage_key=storage_key,
        status="PROCESSING",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    try:
        print("FILE PATH:", file_path)
        print("FILE EXTENSION:", Path(file_path).suffix.lower())
        text = extract_text(str(file_path))
        print("=" * 80)
        print("EXTRACTED DOCUMENT")
        print("=" * 80)
        print(text)

        print("\nTOTAL CHARACTERS:", len(text))
        print("TOTAL WORDS:", len(text.split()))
        if not text.strip():
            raise ValueError("No text could be extracted from document")
        #in save_chunks we are passing the same db session and when we do db.add() we are telling sqlalchemy 
        #to track in the session memory then when we do db.commit() all the iteration gets commited in db of one session.
        # we can create a new db session for save_chunks and do db.commit() inside that method but it's more useful as we 
        # can rollback this entire tranaction at once. 
        save_chunks(
            db=db,
            document_id=document.id,
            text=text,
        )

        document.status = "READY"
        document.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(document)

    except Exception as exc:
        db.rollback()

        document = (
            db.query(Document)
            .filter(Document.id == document.id)
            .first()
        )

        if document:
            document.status = "FAILED"
            document.updated_at = datetime.now(timezone.utc)
            db.commit()

        print("\n========== DOCUMENT PROCESSING ERROR ==========")
        print(f"Type: {type(exc).__name__}")
        print(f"Error: {exc}")
        print("===============================================\n")

        raise
    return {
        "id": document.id,
        "name": document.name,
        "status": document.status,
    }


@router.patch("/{document_id}", response_model=DocumentStatusUpdate)
def update_document(
    document_id: int,
    data: DocumentStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == current_user.id,
        )
        .first()  
    )
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    document.status = data.status
    document.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(document)

    return document


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == current_user.id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # Delete physical file
    file_path = STORAGE_DIR / document.storage_key

    if file_path.exists():
        file_path.unlink()

    # Delete database record
    db.delete(document)
    db.commit()

    return {"message": "Document deleted successfully"}

@router.post("/search")
def search_documents(
    data: DocumentSearchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    results = search_similar_chunks(
        db=db,
        user_id=current_user.id,
        query=data.query,
        document_id=data.document_id,
        limit=data.limit,
    )

    return [
        {
            "document_id": chunk.document_id,
            "chunk_id": chunk.id,
            "chunk_index": chunk.chunk_index,
            "distance": distance,
            "content": chunk.content,
        }
        for chunk, distance in results
    ]