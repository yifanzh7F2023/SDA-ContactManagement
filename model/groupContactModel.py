from db import groupContact_collection, contacts_collection
import random

def generate_unique_group_id():
    while True:
        group_id = str(random.randint(10000, 99999))
        print(f"Generated group ID: {group_id}")
        if not groupContact_collection.find_one({"group_id": group_id}):
            return group_id

class GroupContactModel:
    def __init__(self):
        self.group_contact_collection = groupContact_collection
        self.all_contacts_collection = contacts_collection

    def create_group_contact(self, name, members, is_pinned=False):
        group_id = generate_unique_group_id()
        group_contact_document = {
            "group_id": group_id,
            "name": name,
            "members": members,
            "is_pinned": is_pinned
        }
        self.group_contact_collection.insert_one(group_contact_document)

        # Update each member's document in contacts_collection
        for member in members:
            member_username = member['name']
            self.all_contacts_collection.update_one(
                {"username": member_username},
                {"$push": {"group_contacts": group_contact_document}},
                upsert=True
            )

        return group_id