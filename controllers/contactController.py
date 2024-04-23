from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
from db import groupContact_collection, contacts_collection
from model.contactModel import ContactModel
from model.groupContactModel import GroupContactModel
from model.individualContactModel import IndividualContactModel

contact_blueprint = Blueprint('contact', __name__)
contact_model = ContactModel()
group_model = GroupContactModel()
individual_model = IndividualContactModel()

@contact_blueprint.route('/contacts/<username>', methods=['GET'])
# @jwt_required()
def get_contacts_by_user(username):
    contacts = contact_model.get_contacts_by_username(username)
    return jsonify(contacts), 200

@contact_blueprint.route('/group_contact', methods=['POST'])
# @jwt_required()
def create_group_contact():
    # username = get_jwt_identity()
    data = request.json
    name = data.get('name')
    members = data.get('members')
    is_pinned = data.get('is_pinned', False)

    if not name or not members:
        return jsonify({"msg": "Name and members are required"}), 400

    group_id = group_model.create_group_contact(name, members, is_pinned)
    if group_id:
        return jsonify({"msg": "Group contact created successfully", "id": str(group_id)}), 201
    else:
        return jsonify({"msg": "Failed to create group contact"}), 409

@contact_blueprint.route('/individual_contact', methods=['POST'])
# @jwt_required()
def create_individual_contact():
    # username = get_jwt_identity()
    data = request.json
    username = data.get('username')  # Assume username extraction from JWT
    name = data.get('name')
    email = data.get('email')
    is_pinned = data.get('is_pinned', False)

    if not username:
        return jsonify({"msg": "Authentication required"}), 401
    if not name or not email:
        return jsonify({"msg": "Name and email are required"}), 400

    if individual_model.create_individual_contact(username, name, email, is_pinned):
        return jsonify({"msg": "Individual contact created successfully"}), 201
    else:
        return jsonify({"msg": "Failed to create individual contact"}), 409

@contact_blueprint.route('/group_contact/<group_id>', methods=['GET'])
# @jwt_required()
def get_group_contact(group_id):
    group_contact = groupContact_collection.find_one({"group_id": group_id})
    if group_contact:
        group_contact['_id'] = str(group_contact['_id'])  # Convert ObjectId to string for JSON serialization
        return jsonify(group_contact), 200
    else:
        return jsonify({"msg": "Group contact not found"}), 404

@contact_blueprint.route('/group_contacts', methods=['GET'])
# @jwt_required()
def get_all_group_contacts():
    try:
        group_contacts = groupContact_collection.find({})
        group_contacts_list = list(group_contacts)
        for contact in group_contacts_list:
            contact['_id'] = str(contact['_id'])
            
        return jsonify(group_contacts_list), 200
    except Exception as e:
        return jsonify({"msg": "Failed to fetch group contacts", "error": str(e)}), 500
