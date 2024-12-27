from microesb import microesb

from class_reference import class_reference_client as class_reference
from service_properties import service_properties
from class_mapping import class_mapping
from service_call_metadata import service_metadata_client as service_metadata


class_mapper = microesb.ClassMapper(
    class_references=class_reference,
    class_mappings=class_mapping,
    class_properties=service_properties
)

try:
    res = microesb.ServiceExecuter().execute(
        class_mapper=class_mapper,
        service_data=service_metadata
    )
except Exception as e:
    print('Service execution error: {}'.format(e))
