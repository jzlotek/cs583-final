import os
import io
import flask
import json
import zipfile
from PIL import Image
import loguru
from pydash import is_empty
from pydash.objects import get
from flask import send_from_directory, send_file, Response

logger = loguru.logger

app = flask.Flask(
    __name__,
    static_folder='static'
)


def b64_to_img(photos):
    if photos is None:
        return []

    if type(photos) == str:
        photos = [photos]

    for i in range(len(photos)):
        b = io.StringIO(photos[i])
        b.seek(0)
        photos[i] = Image.open(b)

    return photos


@app.route('/', methods=['GET'])
def home():
    return send_from_directory('../static', 'index.html')


@app.route('/<path:filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory('../static', filename)


# Correct photo with CNN and return result as JPG, PNG, etc
@app.route('/photo', methods=['POST'])
def correct_photo():
    # files = flask.request.form.get('files')
    files = flask.request.files
    # l = files.get('files')
    logger.info(files)

    for f in files:
        logger.info(f)
        logger.info(dir(f))
        ext = str(f).split('.')[-1]
        logger.info('ext:', str(ext))
        if ext in ['jpg', 'jpeg', 'png']:
            files.get(f).save(f)

    # logger.info(l)

    # content = flask.request.get_json(force=True)
    images = []
    by = io.BytesIO()

    logger.info(dir(files))
    # logger.info(f'{i}, {upload}')
    # logger.info(dir(upload))
    # logger.info(f'Uploaded filename: {name}, {i}')
    files.save('./test.jpg')
    by.seek(0)



    images.append(
        Image.open(by)
    )

    logger.info(images)

    if not is_empty(images):
        mimetype = 'image/jpg'

        photos = b64_to_img(images)

        # TODO: CNN
        if len(photos) > 1:
            mimetype = 'application/zip'
            zip_io = io.BytesIO()

            zf = zipfile.ZipFile(zip_io, 'w')

            for img, i in enumerate(photos):
                zf.write(i, img)

            zf.close()
            f = zf
        else:  # run on single image
            f = 1
            pass

        return Response(send_file(f, mimetype=mimetype), status=201)

    else:  # error, return error code 400
        return Response(json.dumps('{photo: [], code: 400}'), status=400)


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT')) if os.environ.get('PORT') else 8080

    app.run(host="0.0.0.0", port=PORT, debug=True)

