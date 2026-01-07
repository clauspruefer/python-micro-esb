from pymongo import MongoClient

client = MongoClient('mongodb://192.168.61.248/')
mongodb = client.get_database('microesb')


def CertGetById(metadata):
    return mongodb.cert.find_one(
        {"id": metadata}
    )

def CertStore(metadata):
    mongodb.cert.insert_one(metadata)

def KeypairGenerate(metadata):
    return True
