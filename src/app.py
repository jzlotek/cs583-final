import os
import io
import flask
import json
import zipfile
import imageio
import loguru
from pydash import is_empty
from flask import send_from_directory, send_file, Response

logger = loguru.logger

app = flask.Flask(
    __name__,
    static_folder='static'
)


@app.route('/', methods=['GET'])
def home():
    return send_from_directory('../static', 'index.html')


@app.route('/<path:filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory('../static', filename)

def cleanup():
    pass

# @app.after_request(cleanup)
@app.route('/zip/<string:name>', methods=['GET'])
def get_zip(name):
    by = None
    try:
        path = os.path.abspath('.')
        by = zipfile.ZipFile(os.path.abspath(os.path.join(path, f'{name}.zip')), 'r')
        by.close()
    except Exception as e:
        logger.error(e)
        return Response(status=404)

    if by:
        return send_file(by, mimetype='application/zip', attachment_filename='images.zip', as_attachment=True)
    else:
        return Response(status=404)

# Correct photo with CNN and return result as JPG, PNG, etc
@app.route('/photo', methods=['POST'])
def correct_photo():
    files = flask.request.files
    images = []

    for name, value in files.items():
        ext = str(name).split('.')[-1]
        if ext in ['jpg', 'jpeg', 'png']:
            value.save(name)
            img = imageio.imread(name)
            images.append((name, img))
            logger.info(f'removing: {name}')
            os.remove(name)

    logger.info(f'processing {len(images)} images')

    if not is_empty(images):

        # TODO: CNN
        if len(images) >= 1:
            mimetype = 'application/zip'
            logger.info('creating zip')
            zf = zipfile.ZipFile('images.zip', 'w')

            for i, img in enumerate(images):
                imageio.imwrite(img[0], img[1])
                zf.write(img[0], img[0])
                logger.info(f'removing tmp: {img[0]}')
                os.remove(img[0])

            zf.close()
        else:  # run on single image
            return Response(json.dumps('{msg: "no images", code: 200}'), status=200)

        return Response(status=200)

    else:  # error, return error code 400
        return Response(json.dumps('{photo: [], code: 400}'), status=400)


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT')) if os.environ.get('PORT') else 8080

    app.run(host="0.0.0.0", port=PORT, debug=True)
