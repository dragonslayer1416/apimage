from src.database.db import get_connection
from src.utils.errors.CustomException import CustomException
from .models.Imagen import Imagen
import base64

class ImagenService:

    @staticmethod
    def upload_image(filename, filedata, filetype):
        """
        Guarda una imagen en la base de datos.
        
        :param filename: Nombre del archivo
        :param filedata: Contenido del archivo codificado en base64
        :param filetype: Tipo de archivo (e.g., 'image/png')
        :raises CustomException: Si ocurre un error durante la operación
        """
        connection = None
        try:
            # Validar tipo de archivo
            if not filetype.startswith("image/"):
                raise CustomException("Invalid file type")

            # Convertir filedata de base64 a binario
            binary_data = base64.b64decode(filedata)

            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO uploads (filename, filedata, filetype) VALUES (%s, %s, %s)",
                    (filename, binary_data, filetype)
                )
            connection.commit()
        except Exception as ex:
            if connection:
                connection.rollback()
            raise CustomException(f"Failed to upload image: {str(ex)}")
        finally:
            if connection:
                connection.close()

    @staticmethod
    def get_images():
        """
        Recupera información de todas las imágenes guardadas en la base de datos.
        
        :return: Una lista de diccionarios con información de las imágenes
        :raises CustomException: Si ocurre un error durante la operación
        """
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
            raise CustomException(f"Failed to retrieve images: {str(ex)}")
        finally:
            if connection:
                connection.close()

    @staticmethod
    def get_image(id):
        """
        Recupera información de una imagen específica por ID.
        
        :param id: ID de la imagen
        :return: Un diccionario con la información de la imagen
        :raises CustomException: Si ocurre un error durante la operación
        """
        connection = None
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, filename, filetype, filedata FROM uploads WHERE id = %s", (id,))
                row = cursor.fetchone()
                if row:
                    # Convertir el contenido binario a base64 para enviar como respuesta
                    encoded_data = base64.b64encode(row[3]).decode('utf-8')
                    image = Imagen(
                        id=row[0],
                        filename=row[1],
                        filetype=row[2],
                        filedata=encoded_data
                    )
                    return image.to_json()
                else:
                    return None
        except Exception as ex:
            raise CustomException(f"Failed to retrieve image: {str(ex)}")
        finally:
            if connection:
                connection.close()

