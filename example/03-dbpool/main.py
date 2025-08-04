#!/usr/bin/python3

import copy

from pgdbpool import pool
from microesb import microesb

from service_properties import service_properties
from class_reference import class_reference
from class_mapping import class_mapping
from service_call_metadata import service_metadata1
from service_call_metadata import service_metadata2
from service_call_metadata import service_metadata3


try:
    dbconfig = {
        'db': {
            'host': '127.0.0.1',
            'name': 'hosting-example',
            'user': 'postgres',
            'pass': 'changeme',
            'ssl': 'disable',
            'connect_timeout': 5,
            'connection_retry_sleep': 1,
            'query_timeout': 3000,
            'session_tmp_buffer': 128
        },
        'groups': {
            'hosting': {
                'connection_count': 3,
                'autocommit': False
            }
        }
    }

    pool.Connection.init(dbconfig)

except Exception as e:
    print('DB connection error: {}'.format(e))
    exit(0)


# first pool connection 1

class_mapper_ref = microesb.ClassMapper(
    class_references=copy.deepcopy(class_reference),
    class_mappings=class_mapping,
    class_properties=service_properties
)

with pool.Handler('hosting') as dbcon:

    service_metadata1['data'][0]['User']['dbcon'] = dbcon

    microesb.ServiceExecuter().execute(
        class_mapper=class_mapper_ref,
        service_data=service_metadata1
    )

    dbcon.commit()

# use (next) pool connection 2

class_mapper_ref = microesb.ClassMapper(
    class_references=copy.deepcopy(class_reference),
    class_mappings=class_mapping,
    class_properties=service_properties
)

with pool.Handler('hosting') as dbcon:

    service_metadata2['data'][0]['User']['dbcon'] = dbcon

    microesb.ServiceExecuter().execute(
        class_mapper=class_mapper_ref,
        service_data=service_metadata2
    )

    dbcon.commit()

# use (next) pool connection 3

class_mapper_ref = microesb.ClassMapper(
    class_references=copy.deepcopy(class_reference),
    class_mappings=class_mapping,
    class_properties=service_properties
)

with pool.Handler('hosting') as dbcon:

    service_metadata2['data'][0]['User']['dbcon'] = dbcon

    microesb.ServiceExecuter().execute(
        class_mapper=class_mapper_ref,
        service_data=service_metadata2
    )

    dbcon.commit()
