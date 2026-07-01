import boto3

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


def guardar_archivo(nombre):

    table.put_item(
        Item={
            "id_tabla": nombre,
            "nombre_proyecto": nombre,
            "descripcion": "Archivo subido a ArchivaCloud"
        }
    )

def eliminar_archivo(nombre):
    table.delete_item(
        Key={
            "id_tabla": nombre,
            "Nombre_proyecto": nombre
        }
    )