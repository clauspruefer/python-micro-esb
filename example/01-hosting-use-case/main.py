from microesb import microesb

from service_properties import service_properties
from class_reference import class_reference
from class_mapping import class_mapping
from service_call_metadata import service_metadata


class_mapper = microesb.ClassMapper(
    class_references=class_reference,
    class_mappings=class_mapping,
    class_properties=service_properties
)

res = microesb.ServiceMapper(
    class_mapper=class_mapper,
    service_data=service_metadata
)
