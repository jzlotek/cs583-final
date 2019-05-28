import os
import io
import flask
import json
import zipfile
import imageio
import base64
from flask import send_from_directory, send_file, Response

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
        photos[i] = base64.b64decode(photos[i])
        photos[i] = imageio.imread(io.BytesIO(photos[i]))

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
    content = flask.request.get_json()
    print(content)
    if content:
        if content.get('photo') and content.get('photo') != '':
            mimetype = 'image/jpg'
            photos = content.get('photo')

            photos = b64_to_img(photos)

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
    else:
        return Response(json.dumps('{photo: [], code: 400}'), status=400)


env = os.environ
PORT = int(env.get('PORT')) if env.get('PORT') else 8080

app.run(host="0.0.0.0", port=PORT, debug=True)
