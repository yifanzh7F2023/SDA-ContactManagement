from bson import ObjectId
from db import contacts_collection

class ContactModel:
    def __init__(self):
        self.contact_collection = contacts_collection
    def _convert_id(self, doc):
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
        if 'members' in doc:
            for member in doc['members']:
                if '_id' in member:
                    member['_id'] = str(member['_id'])
        return doc
    
    def _convert_objectid(self, document):
        if isinstance(document, list):
            return [self._convert_objectid(item) for item in document]
        if isinstance(document, dict):
            for key, value in document.items():
                if isinstance(value, ObjectId):
                    document[key] = str(value)
                elif isinstance(value, (dict, list)):
                    document[key] = self._convert_objectid(value)
        return document

    def get_contacts_by_username(self, username):
        results = self.contact_collection.find({"username": username})
        contacts_list = []
        for contact in results:
            contact = self._convert_id(contact)
            if 'group_contacts' in contact:
                contact['group_contacts'] = [self._convert_id(gc) for gc in contact['group_contacts']]
            if 'individual_contacts' in contact:
                contact['individual_contacts'] = [self._convert_id(ic) for ic in contact['individual_contacts']]
            contacts_list.append(contact)
        return contacts_list
    
    def get_pinned_contacts(self, username):
        contact_document = self.contact_collection.find_one({"username": username})
        if not contact_document:
            return []

        # Filter for pinned contacts
        individual_contacts = [
            self._convert_objectid(contact) for contact in contact_document.get('individual_contacts', [])
            if contact.get('is_pinned')
        ]
        group_contacts = [
            self._convert_objectid(contact) for contact in contact_document.get('group_contacts', [])
            if contact.get('is_pinned')
        ]

        return {'individual_contacts': individual_contacts, 'group_contacts': group_contacts}
    
    def get_normal_contacts(self, username):
        contact_document = self.contact_collection.find_one({"username": username})
        if not contact_document:
            return []

        # Filter for non-pinned (normal) contacts
        individual_contacts = [
            self._convert_objectid(contact) for contact in contact_document.get('individual_contacts', [])
            if not contact.get('is_pinned')
        ]
        group_contacts = [
            self._convert_objectid(contact) for contact in contact_document.get('group_contacts', [])
            if not contact.get('is_pinned')
        ]

        return {'individual_contacts': individual_contacts, 'group_contacts': group_contacts}
    
    def get_all_contacts(self, username):
        contact_document = self.contact_collection.find_one({"username": username})
        if not contact_document:
            return {
                "pinned": {
                    "individual_contacts": [],
                    "group_contacts": []
                },
                "others": {
                    "individual_contacts": [],
                    "group_contacts": []
                }
            }

        # Separate the contacts based on is_pinned flag
        pinned_individual_contacts = [
            self._convert_objectid(contact) for contact in contact_document.get('individual_contacts', [])
            if contact.get('is_pinned')
        ]
        normal_individual_contacts = [
            self._convert_objectid(contact) for contact in contact_document.get('individual_contacts', [])
            if not contact.get('is_pinned')
        ]
        pinned_group_contacts = [
            self._convert_objectid(contact) for contact in contact_document.get('group_contacts', [])
            if contact.get('is_pinned')
        ]
        normal_group_contacts = [
            self._convert_objectid(contact) for contact in contact_document.get('group_contacts', [])
            if not contact.get('is_pinned')
        ]

        return {
            "pinned": {
                "individual_contacts": pinned_individual_contacts,
                "group_contacts": pinned_group_contacts
            },
            "others": {
                "individual_contacts": normal_individual_contacts,
                "group_contacts": normal_group_contacts
            }
        }

    def toggle_pin_status(self, username, contact_name, contact_type):
        user_contact_document = self.contact_collection.find_one({"username": username})
        
        if not user_contact_document:
            return False, "User not found."

        # Determine the field based on the contact type
        field = 'group_contacts' if contact_type == 'group' else 'individual_contacts'
        
        # Find the contact and toggle its is_pinned status
        contact_to_update = None
        for contact in user_contact_document.get(field, []):
            if contact['name'] == contact_name:
                contact_to_update = contact
                break
        
        if contact_to_update:
            new_status = not contact_to_update.get('is_pinned', False)

            self.contact_collection.update_one(
                {"username": username, f"{field}.name": contact_name},
                {"$pull": {field: {"name": contact_name}}}
            )

            contact_to_update['is_pinned'] = new_status
            self.contact_collection.update_one(
                {"username": username},
                {"$push": {field: contact_to_update}}
            )
            return True, "Contact pin status updated."
        else:
            return False, "Contact not found."