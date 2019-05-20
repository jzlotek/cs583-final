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
    content = request.get('json')

    if content:
        if content.get('photo') and content.get('photo') != '':
            # CNN
            pass
        else: # error, return error code 400
            return json.dumps('{photo: "", code: 400}')
    else:
        return json.dumps('{photo: "", code: 400}')

app.run(host="0.0.0.0", port=8080, debug=True)

