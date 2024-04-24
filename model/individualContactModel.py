from db import individualContact_collection, contacts_collection

class IndividualContactModel:
    def __init__(self):
        self.contact_collection = individualContact_collection
        self.all_contacts_collection = contacts_collection

    def create_individual_contact(self, username, name, email, is_pinned=False):
        contact_document = {
            "username": username,
            "name": name,
            "email": email,
            "is_pinned": is_pinned
        }

        individual_contact_document = {
        "name": name,
        "email": email,
        "is_pinned": is_pinned
        }
    
        result = self.contact_collection.insert_one(contact_document)
        if result.inserted_id:
            self.all_contacts_collection.update_one(
                {"username": username},
                {"$push": {"individual_contacts": individual_contact_document}},
                upsert=True
            )

            # Update contact list bidirectionally
            self.all_contacts_collection.update_one(
                {"username": name},
                {"$push": {"individual": {
                    "name": username,
                    "email": "creator's email",
                    "is_pinned": False 
                }}},
                upsert=True
            )
            return result.inserted_id
        else:
            return None
        
    def delete_individual_contact(self, username, contact_name):
        delete_result = self.contact_collection.delete_one({
            "username": username,
            "name": contact_name
        })

        if delete_result.deleted_count == 1:
            self.all_contacts_collection.update_one(
                {"username": username},
                {"$pull": {"individual_contacts": {"name": contact_name}}}
            )
            
            # Also remove this user from the deleted contact's list
            self.all_contacts_collection.update_one(
                {"username": contact_name},
                {"$pull": {"individual": {"name": username}}}
            )

            return True
        return False