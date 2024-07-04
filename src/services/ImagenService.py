from src.database.db import get_connection
from src.utils.errors.CustomException import CustomException
from .models.Imagen import Imagen

class ImagenService:

    @staticmethod
    def upload_image(filename, filedata, filetype):
        connection = None
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO uploads (filename, filedata, filetype) VALUES (%s, %s, %s)",
                    (filename, filedata, filetype)
                )
            connection.commit()
        except Exception as ex:
            if connection:
                connection.rollback()
            raise CustomException("Failed to upload image")
        finally:
            if connection:
                connection.close()

    @staticmethod
    def get_images():
        connection = None
        try:
            connection = get_connection()
            images = []
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, filename, filetype FROM uploads")
                resultset = cursor.fetchall()
                for row in resultset:
                    image = Imagen(
                        id=row[0],
                        filename=row[1],
                        filetype=row[2],
                        filedata=None  # No se incluye el contenido del archivo aquí
                    )
                    images.append(image.to_json())
            return images
        except Exception as ex:
            raise CustomException("Failed to retrieve images")
        finally:
            if connection:
                connection.close()

    @staticmethod
    def get_image(id):
        connection = None
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, filename, filetype, filedata FROM uploads WHERE id = %s", (id,))
                row = cursor.fetchone()
                if row:
                    image = Imagen(
                        id=row[0],
                        filename=row[1],
                        filetype=row[2],
                        filedata=row[3]
                    )
                    return image.to_json() if image else None
        except Exception as ex:
            raise CustomException("Failed to retrieve image")
        finally:
            if connection:
                connection.close()
