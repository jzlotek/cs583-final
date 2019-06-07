import os
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
    logger.info(flask.request.method)
    logger.info(path)
    if flask.request.method == 'GET':
        try:
            return send_file(path, mimetype='application/zip', attachment_filename='images.zip', as_attachment=True)
        except Exception as e:
            logger.error(e)
            return Response(status=404)
    else:
        try:
            os.remove(path)
            return Response(status=200)
        except Exception as e:
            logger.error(e)
            return Response(status=404)


# Correct photo with CNN and return result as JPG, PNG, etc
@logger.catch
@app.route('/photo', methods=['POST'])
def correct_photo():
    files = flask.request.files
    images = []

    mimetype = 'application/zip'

    uniq_name = str(uuid.uuid4())
    zf = zipfile.ZipFile(f'{uniq_name}_images.zip', 'w')

    for name, value in files.items():
        ext = str(name).split('.')[-1]
        if ext.lower() in ['jpg', 'jpeg', 'png']:
            value.save(name)
            images.append((name, ))
            processed_img = net.net(name)
            imageio.imwrite(name, processed_img)
            zf.write(name, name)
            logger.info(f'removing tmp: {name}')
            os.remove(name)
        elif ext.lower() in ['arw', 'dng']:
            value.save(name)
            images.append((name,))
            processed_img = net.net(name)
            name = name.split('.')[0] + '.png'
            imageio.imwrite(name, processed_img)
            zf.write(name, name)
            logger.info(f'removing tmp: {name}')
            os.remove(name)
            os.remove(name.split('.')[0] + '.' + ext)

    logger.info(f'processing {len(images)} images')
    zf.close()

    if not is_empty(images):
        return Response(json.loads(json.dumps('{"filename": "' + uniq_name + '"}')), status=200, mimetype=mimetype)
    else:  # error, return error code 400
        return Response(json.dumps('{msg: "no images", code: 400}'), status=400, mimetype='application/json')


@logger.catch
def main():
    PORT = int(os.environ.get('PORT')) if os.environ.get('PORT') else 8080

    app.run(host="0.0.0.0", port=PORT, debug=True)


if __name__ == '__main__':
    main()
