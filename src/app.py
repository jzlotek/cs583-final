import os
import io
import net
import flask
import json
import zipfile
import imageio
import loguru
import uuid
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


@app.route('/zip/<string:name>', methods=['GET', 'DELETE'])
def get_zip(name):
    path = os.path.abspath(os.path.join(os.path.abspath('.'), f'{name}_images.zip'))

    if flask.request.method == 'GET':
        by = None
        try:
            by = zipfile.ZipFile(path, 'r')
        except Exception as e:
            logger.error(e)
            return Response(status=404)

        if by:
            return send_file(by, mimetype='application/zip', attachment_filename='images.zip', as_attachment=True)
        else:
            return Response(status=404)
    else:
        try:
            os.remove(path)
            return Response(status=200)
        except Exception as e:
            logger.error(e)
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
        uniq_name = ""
        if len(images) >= 1:
            mimetype = 'application/zip'
            logger.info('creating zip')
            uniq_name = str(uuid.uuid4())
            zf = zipfile.ZipFile(f'{uniq_name}_images.zip', 'w')

            for i, img in enumerate(images):
                processed_img = net.net(img[1])
                imageio.imwrite(img[0], processed_img)
                zf.write(img[0], img[0])
                logger.info(f'#{i}) removing tmp: {img[0]}')
                os.remove(img[0])

            zf.close()
        else:  # run on single image
            return Response(json.dumps('{msg: "no images", code: 200}'), status=200)

        return Response(json.dumps('{filename: "' + uniq_name + '"}'), status=200)

    else:  # error, return error code 400
        return Response(json.dumps('{photo: [], code: 400}'), status=400)


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT')) if os.environ.get('PORT') else 8080

    app.run(host="0.0.0.0", port=PORT, debug=True)
