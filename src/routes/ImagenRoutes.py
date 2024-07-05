import os
from flask import Blueprint, request, jsonify, current_app as app
from werkzeug.utils import secure_filename
from base64 import b64encode
import logging
from src.utils.errors.CustomException import CustomException
from src.utils.Security import Security
from src.services.ImagenService import ImagenService

main = Blueprint('image_blueprint', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/', methods=['POST'])
def upload_image():
    # Verificar si el token de seguridad es válido
    has_access = Security.verify_token(request.headers)
    if not has_access:
        return jsonify({'message': 'Unauthorized', 'success': False}), 401

    try:
        # Verificar si hay archivos en la solicitud
        if 'files[]' not in request.files:
            return jsonify({'message': 'No hay parte de archivo en la solicitud', 'success': False}), 400

        files = request.files.getlist('files[]')
        
        errors = {}
        success = False

        for file in files:
            if file and allowed_file(file.filename):
                # Comprobar el tamaño del archivo
                if file.content_length > MAX_CONTENT_LENGTH:
                    errors[file.filename] = 'El archivo es demasiado grande'
                    continue

                filename = secure_filename(file.filename)

                # Crear la carpeta de subidas si no existe
                upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)

                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                
                # Leer y codificar el archivo en base64
                with open(file_path, "rb") as f:
                    filedata = f.read()
                filetype = file.mimetype
                encoded_file = b64encode(filedata).decode('utf-8')

                # Usar el servicio ImagenService para subir la imagen a la base de datos
                ImagenService.upload_image(filename, encoded_file, filetype)
                success = True
            else:
                errors[file.filename] = 'El tipo de archivo no está permitido'

        if success and errors:
            errors['message'] = 'Archivos subidos exitosamente con algunos errores'
            resp = jsonify(errors)
            resp.status_code = 206  # Contenido Parcial
            return resp
        if success:
            resp = jsonify({'message': 'Archivos subidos exitosamente', 'success': True})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify(errors)
            resp.status_code = 400
            return resp

    except CustomException as e:
        logging.error(f"CustomException: {str(e)}")
        return jsonify({'message': str(e), 'success': False}), 500
    except Exception as e:
        logging.error(f"Excepción no controlada: {str(e)}")
        return jsonify({'message': 'Error Interno del Servidor', 'success': False}), 500


