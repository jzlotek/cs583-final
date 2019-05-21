import flask
import json
from flask import send_from_directory

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
            photos = content.get('photo')

            if type(photos) == str:
                photos = [photos]

            # CNN

            # TODO: return CNN output pictures
            return None
        else: # error, return error code 400
            return json.dumps('{photo: [], code: 400}')
    else:
        return json.dumps('{photo: [], code: 400}')

app.run(host="0.0.0.0", port=8080, debug=True)

