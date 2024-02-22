from google.cloud import firestore
from google.cloud import pubsub_v1

PROJECT_ID = 'exam-240222'
publisher = pubsub_v1.PublisherClient()

topic_path = publisher.topic_path(PROJECT_ID, "NUOVO-CANTIERE")

class UaaS(object):
    def __init__(self):
        self.db = firestore.Client()
    
    def clean_db(self):
        ref = self.db.collection('cantieri')
        ref2 = self.db.collection('umarell')
        try:
            for doc in ref.list_documents():
                doc.delete()
            for doc in ref2.list_documents():
                doc.delete()
        except Exception as e:
            print("Exception cought in clean_db(): {" + str(e) + "}")
    
    def insert_cantiere(self, cantiere:dict, id:str) -> dict:
        ref = self.db.collection('cantieri')
        try:
            ref.document(id).set(cantiere)
            msg = str(cantiere['indirizzo'] + " " + str(cantiere['cap']))
            publisher.publish(topic_path, msg.encode('utf-8')).result()
            return cantiere
        except Exception as e:
            print("Exception cought in insert_cantiere(): {" + str(e) + "}")
            return None

    def get_cantiere(self, id:str) -> dict:
        ref = self.db.collection('cantieri')
        try:
            doc = ref.document(id).get()
            cantiere = doc.to_dict() if doc.exists else None
            return cantiere
        except Exception as e:
            print("Exception cought in get_cantiere(): {" + str(e) + "}")
            return None
        
    def insert_umarell(self, umarell:dict, id:str) -> dict:
        ref = self.db.collection('umarell')
        try:
            ref.document(id).set(umarell)
            return umarell
        except Exception as e:
            print("Exception cought in insert_umarell(): {" + str(e) + "}")
            return None

    def get_umarell(self, id:str) -> dict:
        ref = self.db.collection('umarell')
        try:
            doc = ref.document(id).get()
            umarell = doc.to_dict() if doc.exists else None
            return umarell
        except Exception as e:
            print("Exception cought in get_umarell(): {" + str(e) + "}")
            return None
        
    def dump_db(self):
        cantieri = self.db.collection('cantieri')
        umarell = self.db.collection('umarell')

        try:
            umarels = []
            cantiers = []
            for doc in cantieri.stream():
                c = doc.to_dict()
                cantiers.append(c)
            for doc in umarell.stream():
                u = doc.to_dict()
                umarels.append(u)
            return cantiers, umarels
        except Exception as e:
            print("Exception cought in dump_db(): {" + str(e) + "}")
            return None, None
