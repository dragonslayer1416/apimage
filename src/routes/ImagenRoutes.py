import os
from flask import Blueprint, request, jsonify, current_app as app
from werkzeug.utils import secure_filename
import logging
from src.utils.errors.CustomException import CustomException
from src.utils.Security import Security
from src.services.ImagenService import ImagenService
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

main = Blueprint('image_blueprint', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

# Cloudinary configuration
cloudinary.config( 
    cloud_name="dwxj9p9jh", 
    api_key="781316325683796", 
    api_secret="<your_api_secret>", # Replace with your API secret
    secure=True
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/', methods=['POST'])
def upload_image():
    # Verify if the security token is valid
    has_access = Security.verify_token(request.headers)
    if not has_access:
        return jsonify({'message': 'Unauthorized', 'success': False}), 401

    try:
        # Check if there are files in the request
        if 'files[]' not in request.files:
            return jsonify({'message': 'No file part in the request', 'success': False}), 400

        files = request.files.getlist('files[]')
        
        errors = {}
        success = False

        for file in files:
            if file and allowed_file(file.filename):
                # Check the file size
                if file.content_length > MAX_CONTENT_LENGTH:
                    errors[file.filename] = 'File is too large'
                    continue

                filename = secure_filename(file.filename)

                # Upload file to Cloudinary
                upload_result = cloudinary.uploader.upload(file, public_id=filename)

                # Get the URL of the uploaded image
                image_url = upload_result.get('url')

                # Use ImagenService to save the image URL in the database
                ImagenService.upload_image(filename, image_url, file.mimetype)
                success = True
            else:
                errors[file.filename] = 'File type is not allowed'

        if success and errors:
            errors['message'] = 'Files uploaded successfully with some errors'
            resp = jsonify(errors)
            resp.status_code = 206  # Partial Content
            return resp
        if success:
            resp = jsonify({'message': 'Files uploaded successfully', 'success': True})
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


