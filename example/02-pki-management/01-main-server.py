import sys
import logging

from microesb import microesb

from class_reference import class_reference_server as class_reference
from service_properties import service_properties
from class_mapping import class_mapping
from service_call_metadata import service_metadata_server as service_metadata

from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1/')
mongodb = client.get_database('microesb')


logging.getLogger().addHandler(
    logging.StreamHandler(sys.stdout)
)

logging.getLogger().setLevel(
    logging.INFO
)

class_mapper = microesb.ClassMapper(
    class_references=class_reference,
    class_mappings=class_mapping,
    class_properties=service_properties
)

try:
    res = microesb.ServiceExecuter().execute_get_hierarchy(
        class_mapper=class_mapper,
        service_data=service_metadata
    )
except Exception as e:
    print('Service execution error: {}'.format(e))

root_object = res[0]['CertServer']['object_instance']

mongodb.cert_hierarchy.insert_one(root_object.json_dict)
