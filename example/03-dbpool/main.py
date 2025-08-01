#!/usr/bin/python3

from pgdbpool import pool
from microesb import microesb

from service_properties import service_properties
from class_reference import class_reference
from class_mapping import class_mapping
from service_call_metadata import service_metadata1
from service_call_metadata import service_metadata2
from service_call_metadata import service_metadata3


class_mapper1 = microesb.ClassMapper(
    class_references=class_reference,
    class_mappings=class_mapping,
    class_properties=service_properties
)

class_mapper2 = microesb.ClassMapper(
    class_references=class_reference,
    class_mappings=class_mapping,
    class_properties=service_properties
)

class_mapper3 = microesb.ClassMapper(
    class_references=class_reference,
    class_mappings=class_mapping,
    class_properties=service_properties
)


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


# use pool connection 1
with pool.Handler('hosting') as dbcon:

    service_metadata1['data'][0]['User']['dbcon'] = dbcon

    microesb.ServiceExecuter().execute(
        class_mapper=class_mapper1,
        service_data=service_metadata1
    )

    dbcon.commit()

# use (next) pool connection 2
with pool.Handler('hosting') as dbcon:

    service_metadata2['data'][0]['User']['dbcon'] = dbcon

    microesb.ServiceExecuter().execute(
        class_mapper=class_mapper2,
        service_data=service_metadata2
    )

    dbcon.commit()

# use (next) pool connection 3
with pool.Handler('hosting') as dbcon:

    service_metadata2['data'][0]['User']['dbcon'] = dbcon

    microesb.ServiceExecuter().execute(
        class_mapper=class_mapper3,
        service_data=service_metadata2
    )

    dbcon.commit()
