import sys
import logging
import psycopg2

from microesb import microesb

from service_properties import service_properties
from class_reference import class_reference
from class_mapping import class_mapping
from service_call_metadata import service_metadata


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
    dbcon = psycopg2.connect("dbname='hosting-example' user='postgres' host='localdb'")
    dbcon.autocommit = False
except Exception as e:
    print('DB connection error: {}'.format(e))
    exit(0)

service_metadata['data'][0]['User']['dbcon'] = dbcon

#try:
microesb.ServiceExecuter().execute(
    class_mapper=class_mapper,
    service_data=service_metadata
)
#except Exception as e:
#    print('Service execution error: {}'.format(e))

try:
    dbcon.commit()
    dbcon.close()
except Exception as e:
    print('DB close error: {}'.format(e))
