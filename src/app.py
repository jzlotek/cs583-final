import os
import io
import flask
import json
import zipfile
from flask import send_from_directory, send_file

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return send_from_directory('src/static', 'index.html')


# Correct photo with CNN and return result as JPG, PNG, etc
@app.route('/correct', methods=['POST'])
def correct_photo():
    content = flask.request.args.get('json')

    if content:
        if content.get('photo') and content.get('photo') != '':
            mimetype = 'image/jpg'
            photos = content.get('photo')

            if type(photos) == str:
                photos = [photos]

            # CNN

            # TODO: return CNN output pictures

            if len(photos) > 1:
                mimetype='application/zip'
                zip_io = io.BytesIO() 

                zf = zipfile.ZipFile(zip_io, 'w')

                for img, i in enumerate(photos):
                    zf.write(i, img)

                zf.close()

                return send_file(zip_io, mimetype=mimetype)


            #'application/zip'
            return send_file(None, mimetype=mimetype)
        else: # error, return error code 400
            return json.dumps('{photo: [], code: 400}')
    else:
        return json.dumps('{photo: [], code: 400}')

env = os.environ
PORT = env.get('PORT') if env.get('PORT') else 8080

app.run(host="0.0.0.0", port=PORT, debug=True)

