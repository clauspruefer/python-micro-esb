from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1/')
mongodb = client.get_database('microesb')


def CertGetById(metadata):
    return mongodb.cert.find_one(
        {"id": metadata}
    )

def CertStore(metadata):
    return mongodb.cert.insert_one(metadata)

def KeypairGenerate(metadata):
    return True
