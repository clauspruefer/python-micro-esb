# ]*[ --------------------------------------------------------------------- ]*[
#  .                         Micro ESB Python Module                         .
# ]*[ --------------------------------------------------------------------- ]*[
#  .                                                                         .
#  .  Copyright Claus Prüfer (2018)                                          .
#  .                                                                         .
#  .                                                                         .
# ]*[ --------------------------------------------------------------------- ]*[

import abc
import sys
import logging
import importlib

from microesb import esbconfig
from microesb import handler


class BaseHandler(handler.ServiceProcessor):
    """Meta class.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self._SYSProperties = None
        self._SYSParentObject = None
        self._SYSClassNames = []

        super().__init__()

    @abc.abstractmethod
    def _add_class(self):
        """Abstract _add_class() method.
        """

    @abc.abstractmethod
    def set_properties(self):
        """Abstract set_properties() method.
        """

    def iterate(self):
        """ Recursive iterate through hierarchical objects.
        """
        yield self
        for x in self:
            for y in x.iterate():
                yield y

    def add_properties(self, properties, parent_instance):
        self.logger.debug('add properties:{}'.format(properties))
        self._SYSParentObject = parent_instance
        setattr(self, '_SYSProperties', properties)
        for p_key, p_value in properties.items():
            setattr(self, p_key, p_value['default'])

    def _set_property(self, key, value):
        if key in self._SYSProperties:
            setattr(self, key, value)

    @property
    def parent_object(self):
        return self._SYSParentObject

    @property
    def properties(self):
        return self._SYSProperties

    @property
    def class_count(self):
        return len(self._SYSClassNames)

    @property
    def class_name(self):
        return self.__class__.__name__

    def get_value_by_property_id(self, id):
        raise NotImplementedError


class ClassHandler(BaseHandler):
    """Base class.
    """

    def __init__(self):
        super().__init__()
        self._SYSType = 'class_instance'

    def __add__(self, args):
        self._add_class(**args)

    def __iter__(self):
        for class_name in self._SYSClassNames:
            yield getattr(self, class_name)

    def _add_class(self, *, class_name, class_ref):

        self._SYSClassNames.append(class_ref)

        new_class = globals()[class_ref]
        instance = new_class()
        setattr(self, class_name, instance)

    def set_properties(self, item_dict):
        for property_id, value in item_dict.items():
            self._set_property(property_id, value)

    def set_json_dict(self):
        self.logger.debug('self._SYSProperties:{}'.format(self._SYSProperties))
        for property_id in self._SYSProperties:
            self.logger.debug('processing property:{}'.format(property_id))
            self.json_dict[property_id] = getattr(self, property_id)


class MultiClassHandler(BaseHandler):
    """MultiObject handler class.
    """

    def __init__(self):
        super().__init__()
        self._SYSType = 'multiclass_container'
        self._object_container = []

    def __iter__(self):
        for class_instance in self._object_container:
            yield class_instance

    def _add_class(self):
        self.logger.debug('Add class multiclass handler')
        new_class = globals()[self.class_name]
        instance = new_class()
        setattr(instance, '_SYSProperties', getattr(self, '_SYSProperties'))
        setattr(instance, '_SYSType', 'multiclass_instance')
        self._object_container.append(instance)
        return instance

    def set_properties(self, property_list):

        for class_config in property_list:
            instance = self._add_class()
            for var, value in class_config.items():
                instance._set_property(var, value)

    def set_json_dict(self):
        self.logger.debug('Object container:{}'.format(self._object_container))
        class_name = self.class_name
        self.json_dict[class_name] = []
        for class_instance in self:
            self.logger.debug('Loop class instance:{}'.format(dir(class_instance)))
            class_instance.set_instance_json_dict()
            self.json_dict[class_name].append(class_instance.json_dict)
        if len(self.json_dict[class_name]) == 0:
            del self.json_dict[class_name]

    def set_instance_json_dict(self):
        for property_id in self._SYSProperties:
            self.json_dict[property_id] = getattr(self, property_id)


class ClassMapper(ClassHandler):
    """Class Mapper class.
    """

    def __init__(self, *, class_references, class_mappings, class_properties):
        """
        """
        super().__init__()

        self._class_mappings = class_mappings
        self._class_properties = class_properties
        self._class_references = class_references

        root_class = next(iter(class_references))
        root_index = class_references[root_class]

        self._class_hierarchy = {}

        call_dict = {
            'class_name': root_class,
            'children': root_index['children'],
            'property_ref': root_index['property_ref'],
            'parent_instance': self,
        }

        self._map(**call_dict)

    def __repr__(self):
        return 'Class mappings:{} properties:{} references:{}'.format(
            self._class_mappings,
            self._class_properties,
            self._class_references
        )

    def _get_mapping(self, id):
        return self._class_mappings[id]

    def get_references(self):
        return self._class_references

    def _map(
        self,
        *,
        class_name,
        property_ref,
        parent_instance,
        children={}
    ):

        self.logger.debug(
            'class_name:{} property_ref:{} parent_instance:{} children:{}'.format(
                class_name,
                property_ref,
                parent_instance,
                children,
            )
        )

        class_ref = self._get_mapping(class_name)

        self._class_hierarchy[class_name] = parent_instance

        args = {
            'class_name': class_name,
            'class_ref': class_ref
        }

        parent_instance + args

        child_instance = getattr(parent_instance, class_name)

        child_instance.add_properties(
            self._class_properties[property_ref]['properties'],
            parent_instance
        )

        for child_class_name, child_class_config in children.items():
            child_class_config['class_name'] = child_class_name
            child_class_config['parent_instance'] = child_instance
            self._map(**child_class_config)


class ServiceMapper(ClassHandler):
    """Service Mapper class.
    """
    def __init__(self, *, class_mapper, service_data):
        """
        """
        super().__init__()

        self._class_mapper = class_mapper

        class_references = self._class_mapper.get_references()

        root_class = next(iter(class_references))
        root_index = class_references[root_class]

        for item in service_data['data']:
            call_dict = {
                'class_name': root_class,
                'children': root_index['children'],
                'parent_instance': self._class_mapper,
                'hierarchy': item
            }

            self._map(**call_dict)

    def _map(
        self,
        *,
        class_name,
        parent_instance,
        hierarchy,
        children={},
        property_ref=None,
        type=None
    ):

        self.logger.debug(
            'class_name:{} parent_instance:{} children:{} hierarchy:{}'.format(
                class_name,
                parent_instance,
                children,
                hierarchy,
            )
        )

        class_instance = getattr(parent_instance, class_name)

        hierarchy = hierarchy[class_name]
        class_instance.set_properties(hierarchy)

        for child_class_name, child_class_config in children.items():
            child_class_config['class_name'] = child_class_name
            child_class_config['parent_instance'] = class_instance
            child_class_config['hierarchy'] = hierarchy
            self._map(**child_class_config)


# import classes into current namespace
current_mod = sys.modules[__name__]
import_classes = esbconfig.import_classes

for module_name in import_classes:
    mod_ref = importlib.import_module(module_name)
    for class_name in import_classes[module_name]:
        setattr(current_mod, class_name, getattr(mod_ref, class_name))
