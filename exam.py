from google.cloud import firestore

class Name_of_class(object):
    def __init__(self):
        self.db = firestore.Client()
    
    def clean_db(self):
        ref = self.db.collection('name_of_collection')
        try:
            for doc in ref.list_documents():
                doc.delete()
        except Exception as e:
            print("Exception cought in clean_db(): {" + str(e) + "}")
    