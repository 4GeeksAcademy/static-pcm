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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


    # ESTO ME TRAE TODOS LOS MIEMBROS
@app.route('/members', methods=['GET'])
def get_members():

    members = jackson_family.get_all_members()
    response_body = members

    return jsonify(response_body), 200


    # ESTO ME DEJA AGREGAR UN NUEVO MIEMBRO
@app.route('/member', methods=['POST'])
def add_member():
    body = request.get_json()
    new_member = {
        "id": body["id"],
        "first_name": body["first_name"],
        "age": body["age"],
        "lucky_numbers": body["lucky_numbers"]
    }

    member = jackson_family.add_member(new_member)

    response_body = {"msg": "se dio a luz un nuevo miembro"}
    return response_body, 200


    #ESTO ME TRAE UN SOLO MIEMBRO DE LA FAMILIA
@app.route('/member/<int:id>', methods=['GET'])
def get_only_member(id):

    members_id = jackson_family.get_member(id)
    response_body = members_id

    return jsonify(response_body), 200


    #
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member1(id):

    members = jackson_family.delete_member(id)
    response_body = {"done": members}

    return jsonify(response_body), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)