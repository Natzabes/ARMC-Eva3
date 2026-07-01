from fastapi import APIRouter, HTTPException
import re
from app.models.upload_request import UploadRequest
from app.services.s3_service import s3_client
from botocore.exceptions import ClientError
from app.services.dynamodb_service import guardar_archivo
from app.config import (
    BUCKET_NAME,
    MAX_FILE_SIZE,
    ALLOWED_EXTENSIONS,
    AWS_REGION
)

router = APIRouter()

@router.post("/api/upload/presigned-url")
def generate_presigned_url(data: UploadRequest):

    file_name = data.fileName.lower()

    safe_name = re.sub(
        r'[^a-zA-Z0-9._-]',
        '_',
        data.fileName
    )

    if not any(
        file_name.endswith(ext)
        for ext in ALLOWED_EXTENSIONS
    ):
        raise HTTPException(
            status_code=400,
            detail="Tipo de archivo no permitido"
        )

    if data.fileSize > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Archivo excede tamaño máximo"
        )

    key = f"uploads/{safe_name}"

    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": key,
            "ContentType": data.fileType
        },
        ExpiresIn=3600
    )

    public_url = (
        f"https://{BUCKET_NAME}.s3."
        f"{AWS_REGION}.amazonaws.com/{key}"
    )

    guardar_archivo(
        safe_name,
        data.fileType,
        data.fileSize
    )
    
    return {
        "presignedUrl": presigned_url,
        "key": key,
        "publicUrl": public_url
    }

@router.get("/api/files")
def list_files():

    try:

        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix="uploads/"
        )

        files = []

        for obj in response.get("Contents", []):

            file_key = obj["Key"]

            if file_key == "uploads/":
                continue
            
            url = s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": BUCKET_NAME,
                    "Key": obj["Key"]
                },
                ExpiresIn=3600
            )

            files.append({
                "name": obj["Key"].replace("uploads/", ""),
                "size": obj["Size"],
                "lastModified": obj["LastModified"],
                "url": url
            })

        return files

    except ClientError:

        raise HTTPException(
            status_code=500,
            detail="Error al obtener archivos"
        )

@router.delete("/api/files/{key}")
def delete_file(key: str):

    try:

        s3_client.delete_object(
            Bucket=BUCKET_NAME,
            Key=f"uploads/{key}"
        )
        
        return {
            "message": f"{key} eliminado correctamente"
        }

    except ClientError:

        raise HTTPException(
            status_code=500,
            detail="Error al eliminar archivo"
        )