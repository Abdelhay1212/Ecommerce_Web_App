import os
import secrets
from PIL import Image
from ecommerceApp import app


def save_image(image_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(image_file.filename)

    filename = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/images/users_images', filename)

    output_size = (125, 125)
    image = Image.open(image_file)
    image.thumbnail(output_size)
    image.save(image_path)

    return filename


def delete_image(image_file):
    def is_image_exists(image_file):
        image_path = os.path.join(app.root_path, 'static/images/users_images', image_file)
        return os.path.exists(image_path)
    
    if is_image_exists(image_file):
        image_path = os.path.join(app.root_path, 'static/images/users_images', image_file)
        os.remove(image_path)
