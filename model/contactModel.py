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