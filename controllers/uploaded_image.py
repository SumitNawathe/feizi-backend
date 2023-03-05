import os
import time

from flask import Blueprint, make_response, jsonify, request

from app import LOG
from models.administration import User, UploadedImage
from repository.setup_sqlalchemy import sql_engine
from repository.uploaded_image import UploadedImageRepository
from repository.user import UserRepository
from utilities.authentication import create_token, auth


image_repo = UploadedImageRepository(sql_engine)
image_routes = Blueprint( 'image', __name__ )

IMAGE_DIR = "/backend/images"
IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@image_routes.route("/images/upload", methods=['POST'])
@auth
def upload_image(user: User):
    try:
        file = request.files['file']
        orig_filename = '.'.join(file.filename.split('.')[:-1])
        orig_extension = file.filename.split('.')[-1]
        if orig_extension not in IMAGE_EXTENSIONS:
            return make_response('invalid filetype', 400)

        timestamp = int(time.time() * 1000)
        filename = orig_filename + "_" + str(timestamp) + "_." + orig_extension
        file.save(os.path.join(IMAGE_DIR, filename))
        image_repo.create(UploadedImage(
            _id=-1,
            user_id=user._id,
            filename=filename
        ))
        return make_response('', 200)
    except Exception as e:
        LOG.info('error')
        LOG.info(e)
        return make_response('', 500)

@image_routes.route("/images/all_filenames", methods=['GET'])
@auth
def all_filenames(user: User):
    try:
        lst = image_repo.get_for_user_id(user._id)
        return jsonify(list(map(lambda img: img.filename, lst)))
    except Exception as e:
        return make_response('', 500)
