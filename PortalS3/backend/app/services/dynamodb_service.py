import boto3
from datetime import datetime

from app.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_SESSION_TOKEN,
    AWS_REGION,
    DYNAMODB_TABLE
)

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
    region_name=AWS_REGION
)

table = session.resource("dynamodb").Table(DYNAMODB_TABLE)


def guardar_archivo(nombre, tipo, tamano):

    table.put_item(
        Item={
            "archivo": nombre,
            "tipo": tipo,
            "tamano": tamano,
            "fecha_subida": datetime.now().isoformat(),
            "descripcion": "Archivo almacenado en Amazon S3"
        }
    )