from flask import Flask, request
from get_audio import add_description, validate_description, get_CAPTCHA

api = Flask(__name__)

@api.route('/newCAPTCHA', methods=['POST'])
#Input ID of the track used for this captcha, non-labeled
def new_CAPTCHA():
    track_id = request.json['track_id']
    description = request.json['description']

    add_description(description, track_id)
    return {}, 200

@api.route('/validateCAPTCHA', methods=['POST'])
#Input ID of the track used for this captcha, already-labeled
def validate_CAPTCHA():
    track_id = request.json['track_id']
    description = request.json['description']

    validate_description(description, track_id)
    return {}, 200

@api.route('/generateCAPTCHA', methods=['POST'])
#Randomly select new captcha
def generate_CAPTCHA():
    url, id, isNew = get_CAPTCHA()
    data = {'url': url, 'id': id,'isNew': isNew}
    return data, 200
