from flask import Flask, request
from get_audio import add_description, validate_description, get_CAPTCHA
import json

api = Flask(__name__)

@api.route('/newCAPTCHA', methods=['POST'])
#Input ID of the track used for this captcha, non-labeled
def new_CAPTCHA():
    track_id = request.json['track_id']
    description = request.json['description']
    correct_answer = request.json['correct_answer']

    success = add_description(description, track_id, correct_answer=correct_answer)
    if success:
        return {}, 200
    else:
        return {}, 400

@api.route('/validateCAPTCHA', methods=['POST'])
#Input ID of the track used for this captcha, already-labeled
def validate_CAPTCHA():
    track_id = request.json['track_id']
    description = request.json['description']

    multiple_choice = validate_description(description, track_id)
    return multiple_choice, 200

@api.route('/generateCAPTCHA', methods=['POST'])
#Randomly select new captcha
def generate_CAPTCHA():
    url, id, isMultipleChoice, multipleChoice, correctAnswer = get_CAPTCHA()
    data = {
        'url': url, 
        'id': id,
        'isMultipleChoice': isMultipleChoice,
        'multiple_choice': multipleChoice,
        'correctAnswer': correctAnswer,
        }
    data = json.dumps(data)
    return data, 200

@api.route('/')
def swag():
    return "<h1 style='color:blue'>Wassup</h1>"

if __name__ == "__main__":
    api.run(host='0.0.0.0', debug=True, port=5000)
