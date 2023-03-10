import os
import time

from flask import Blueprint, make_response, jsonify, request, send_file

from app import LOG
from models.administration import User, UploadedImage, Segmentation
from repository.segmentation import SegmentationRepository
from repository.setup_sqlalchemy import sql_engine
from repository.uploaded_image import UploadedImageRepository
from repository.user import UserRepository
from utilities.authentication import create_token, auth
import numpy as np
import skimage
import skimage.io


image_repo = UploadedImageRepository(sql_engine)
image_routes = Blueprint( 'image', __name__ )
segmentation_repo = SegmentationRepository(sql_engine)

IMAGE_DIR = "/backend/images"
IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@image_routes.route("/images/upload/<label>", methods=['POST'])
@auth
def upload_image(user: User, label: str):
    try:
        # check file and extension
        file = request.files['file']
        orig_filename = '.'.join(file.filename.split('.')[:-1])
        orig_extension = file.filename.split('.')[-1]
        if orig_extension not in IMAGE_EXTENSIONS:
            return make_response('invalid filetype', 400)

        # create and save original file
        timestamp = int(time.time() * 1000)
        filename = orig_filename + "_" + str(timestamp) + "_." + orig_extension
        file.save(os.path.join(IMAGE_DIR, filename))
        image_repo.create(UploadedImage(
            _id=-1,
            user_id=user._id,
            filename=filename,
            label=label
        ))

        # create and save with gaussian blur
        image = skimage.io.imread(os.path.join(IMAGE_DIR, filename))
        distorted = skimage.util.random_noise(image, clip=True, var=0.1)
        distorted_filename = orig_filename + "_" + str(timestamp) + "_distorted." + orig_extension
        skimage.io.imsave(os.path.join(IMAGE_DIR, distorted_filename), distorted)
        image_repo.create(UploadedImage(
            _id=-1,
            user_id=user._id,
            filename=distorted_filename,
            label=label
        ))

        return make_response('', 200)
    except Exception as e:
        LOG.info('error')
        LOG.info(e)
        return make_response('', 500)

@image_routes.route("/images/file/<filename>", methods=['GET'])
@auth
def get_file_by_name(user: User, filename: str):
    try:
        image = image_repo.get_by_filename(filename)
        if image is None:
            return make_response('', 404)
        if image.user_id != user._id:
            return make_response('', 401)
        return send_file(os.path.join(IMAGE_DIR, filename))
    except Exception as e:
        return make_response('', 500)

@image_routes.route("/images/label/<filename>", methods=['GET'])
@auth
def get_label_by_name(user: User, filename: str):
    try:
        image = image_repo.get_by_filename(filename)
        if image is None:
            return make_response('', 404)
        if image.user_id != user._id:
            return make_response('', 401)
        return jsonify({'label': image.label})
    except Exception as e:
        return make_response('', 500)

@image_routes.route("/images/segmentation/<filename>", methods=['POST'])
@auth
def store_segmentation(user: User, filename: str):
    try:
        image = image_repo.get_by_filename(filename)
        if image is None:
            return make_response('', 404)
        if image.user_id != user._id:
            return make_response('', 401)

        data = request.get_json(force=True)
        segmentation_repo.create(Segmentation(
            _id=-1,
            image_id=image._id,
            points=data
        ))
        return make_response('', 200)
    except Exception as e:
        return make_response('', 500)

@image_routes.route("/images/all_filenames", methods=['GET'])
@auth
def all_filenames(user: User):
    try:
        lst = image_repo.get_for_user_id(user._id)
        return jsonify(list(map(lambda img: img.filename, lst)))
    except Exception as e:
        return make_response('', 500)
