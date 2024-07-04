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
    has_access = Security.verify_token(request.headers)
    if not has_access:
        return jsonify({'message': 'Unauthorized', 'success': False}), 401

    try:
        # Comprobación de la parte de archivo en la solicitud
        if 'files[]' not in request.files: #files[] es el nombre de la key para poder subir una imagen
            return jsonify({'message': 'No hay parte de archivo en la solicitud', 'success': False}), 400

        files = request.files.getlist('files[]')
        
        errors = {}
        success = False

        # Procesar cada archivo de la solicitud
        for file in files:
            if file and allowed_file(file.filename):
                # Comprobar el tamaño del archivo
                if file.content_length > MAX_CONTENT_LENGTH:
                    errors[file.filename] = 'File is too large'
                    continue

                filename = secure_filename(file.filename)

                # Create uploads folder if it doesn't exist
                upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)

                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                
                # Read and encode the file
                with open(file_path, "rb") as f:
                    filedata = f.read()
                filetype = file.mimetype
                encoded_file = b64encode(filedata).decode('utf-8')

                # Use ImagenService to upload the image to the database
                ImagenService.upload_image(filename, encoded_file, filetype)
                success = True
            else:
                errors[file.filename] = 'El tipo de archivo no está permitido".'

        if success and errors:
            errors['message'] = 'File(s) successfully uploaded with some errors'
            resp = jsonify(errors)
            resp.status_code = 206  # Partial Content
            return resp
        if success:
            resp = jsonify({'message': 'Files successfully uploaded', 'success': True})
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
        logging.error(f"Unhandled exception: {str(e)}")
        return jsonify({'message': 'Internal Server Error', 'success': False}), 500
