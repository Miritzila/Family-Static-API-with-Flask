"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({
    "id": jackson_family._generateId(),
    "first_name": "John Jackson",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})

jackson_family.add_member({
    "id": 0,
    "first_name": "Jane Jackson",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})

jackson_family.add_member({
    "id": 0,
    "first_name": "Jimmy Jackson",
    "age": 5,
    "lucky_numbers": [1]
})

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET','DELETE'])
def handle_member(member_id):

    if request.method == "GET":
        member = jackson_family.get_member(member_id)
        response_body = member
        return jsonify(response_body), 200
    
    if request.method == "DELETE":
        jackson_family.delete_member(member_id)
        return jsonify({'done':True}), 200

@app.route('/member/', methods=['POST'])
def handle_add_member():

    member = request.json
    print(member)
    jackson_family.add_member(member)
    return jsonify("Ha sido agregado con éxito"), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
