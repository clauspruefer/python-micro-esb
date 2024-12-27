# ]*[ --------------------------------------------------------------------- ]*[
#  .                         Micro ESB Python Module                         .
# ]*[ --------------------------------------------------------------------- ]*[
#  .                                                                         .
#  .  Copyright Claus Prüfer (2016 - 2024)                                   .
#  .                                                                         .
#  .                                                                         .
# ]*[ --------------------------------------------------------------------- ]*[

import abc
import sys
import logging
import importlib
import esbconfig

from microesb.transformer import JSONTransformer


class BaseHandler(JSONTransformer):
    """ Abstract Base Class (ABC) Meta Class.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """
        :ivar classref logger: logging logger reference
        :ivar dict[SYSProperties] _SYSProperties: internal properties processing dict
        :ivar classref _SYSParentObject: internal (hierarchical) class instance ref
        :ivar list[classref] _SYSClassNames: internal class refs dict (should be renamed to _SYSClassRefs)
        """

        self.logger = logging.getLogger(__name__)

        self._SYSProperties = None
        self._SYSParentObject = None
        self._SYSClassNames = []

        super().__init__()

    @abc.abstractmethod
    def _add_class(self):
        """ Abstract _add_class() method.
        """

    @abc.abstractmethod
    def set_properties(self):
        """ Abstract set_properties() method.
        """

    def iterate(self):
        """ Recursive iterate through hierarchical class instances.
        """
        yield self
        for x in self:
            for y in x.iterate():
                yield y

    def add_properties(self, properties, parent_instance):
        """ add_properties() method.

        :param dict properties: system properties dictionary
        :param classref parent_instance: parent class instance reference

        The ClassMapper recursively adds instance properties by calling
        add_properties() method on initialization for each existing class instance.
        """
        properties = self._add_sys_default_properties(properties)
        self.logger.debug('add properties:{}'.format(properties))
        self._SYSParentObject = parent_instance
        setattr(self, '_SYSProperties', properties)
        for p_key, p_value in properties.items():
            setattr(self, p_key, p_value['default'])

    def _add_sys_default_properties(self, properties):
        """ _add_sys_default_properties() method.

        :param dict properties: system properties dictionary

        Enhance (add) system default properties dictionary by properties dict
        defined inside this method.

        Currently 'SYSServiceMethod' is the only system property added.

        :return: properties
        :rtype: dict
        """
        properties['SYSServiceMethod'] = {
            'type': 'str',
            'default': None,
            'required': False,
            'description': 'System Service Method'
        }
        return properties

    def _set_property(self, key, value):
        """ _set_property() method.

        :param str key: property key name
        :param str value: property value

        """
        if key in self._SYSProperties:
            setattr(self, key, value)

    @property
    def parent_object(self):
        """ parent_object() method.

        :return: self._SYSParentObject
        :rtype: classref

        Decorated with @property so direct property access possible
        """
        return self._SYSParentObject

    @property
    def properties(self):
        """ properties() method.

        :return: self._SYSProperties
        :rtype: dict

        Decorated with @property so direct property access possible
        """
        return self._SYSProperties

    @property
    def class_count(self):
        """ class_count() method.

        :return: len(self._SYSClassNames)
        :rtype: int

        Decorated with @property so direct property access possible
        """
        return len(self._SYSClassNames)

    @property
    def class_name(self):
        """ class_name() method.

        :return: self.__class__.__name__
        :rtype: str

        Decorated with @property so direct property access possible
        """
        return self.__class__.__name__

    def get_value_by_property_id(self, id):
        raise NotImplementedError


class ClassHandler(BaseHandler):
    """ ClassHandler class. Inherits BaseHandler class.
    """

    def __init__(self):
        """
        :ivar str _SYSType: const internal system type to differentiate handler types
        """
        super().__init__()
        self._SYSType = 'class_instance'

    def __add__(self, args):
        """ overloaded internal __add__() method (+ operator).

        :param dict args: class setup dictionary

        _add_class() "wrapper" primary used for ClassMapper.

        >>> args = {
        >>>     'class_name': class_name,
        >>>     'class_ref': class_ref
        >>> }
        >>> parent_instance + args
        """
        self._add_class(**args)

    def __iter__(self):
        """ overloaded internal __iter__() method.

        Overloaded for using iter() on class references.
        """
        for class_name in self._SYSClassNames:
            yield getattr(self, class_name)

    def _add_class(self, *, class_name, class_ref):
        """ _add_class() method.

        :param dict *: used for passing params as **args dictionary
        :param str class_name: class name
        :param classref class_ref: class instance reference

        Append class_name to self._SYSClassNames. Setup new class instance
        in global namespace.

        Primary called by overloaded __add__() method.
        """

        self._SYSClassNames.append(class_ref)

        new_class = globals()[class_ref]
        instance = new_class()
        setattr(self, class_name, instance)

    def set_properties(self, item_dict):
        """ set_properties() method.

        :param dict item_dict: properties dictionary

        Iterates over item_dict and calls self._set_property(property_id, value)
        foreach item.
        """
        for property_id, value in item_dict.items():
            self._set_property(property_id, value)

    def set_json_dict(self):
        """ set_json_dict() method.

        Preprare self.json_dict from self._SYSProperties (used by JSONTransformer).
        """
        self.logger.debug('self._SYSProperties:{}'.format(self._SYSProperties))
        for property_id in self._SYSProperties:
            self.logger.debug('processing property:{}'.format(property_id))
            self.json_dict[property_id] = getattr(self, property_id)


class MultiClassHandler(BaseHandler):
    """ MultiObject handler class.
    """

    def __init__(self):
        """
        :ivar str _SYSType: const internal system type to differentiate handler types
        :ivar list[object] _object_container: object instance container
        """
        super().__init__()
        self._SYSType = 'multiclass_container'
        self._object_container = []

    def __iter__(self):
        """ overloaded internal __iter__() method.

        Overloaded for using iter() on class references.
        """
        for class_instance in self._object_container:
            yield class_instance

    def _add_class(self):
        """ _add_class() method.

        :return: instance
        :rtype: object instance

        Setup class instance and append it to self._object_container.
        """
        self.logger.debug('Add class multiclass handler')
        new_class = globals()[self.class_name]
        instance = new_class()
        setattr(instance, '_SYSProperties', getattr(self, '_SYSProperties'))
        setattr(instance, '_SYSParentObject', getattr(self, '_SYSParentObject'))
        setattr(instance, '_SYSType', 'multiclass_instance')

        self._object_container.append(instance)
        return instance

    def set_properties(self, property_list):
        """ set_properties() method.

        :param list property_list: properties dictionary

        Setup class instance and append it to self._object_container.
        """
        for class_config in property_list:
            instance = self._add_class()
            for var, value in class_config.items():
                instance._set_property(var, value)

    def set_json_dict(self):
        """ set_json_dict() method.

        Preprare self.json_dict from self (self._object_container)).
        """
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
        """ set_instance_json_dict() method.

        Preprare self.json_dict from self._SYSProperties (used by JSONTransformer).
        """
        for property_id in self._SYSProperties:
            try:
                self.json_dict[property_id] = getattr(self, property_id)
            except Exception as e:
                pass


class ClassMapper(ClassHandler):
    """ Class Mapper class.
    """

    def __init__(self, *, class_references, class_mappings, class_properties):
        """
        :param dict *: used for passing params as **args dictionary
        :param dict class_references: class references dictionary
        :param dict class_mappings: class mappings dictionary
        :param dict class_properties: class properties dictionary

        :ivar dict _class_mappings: set from class_mappings param
        :ivar dict _class_properties: set from class_properties param
        :ivar dict _class_references: set from class_references param
        :ivar dict _class_hierarchy: internally used to map parent instances
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
        """ overloaded __repr__() method.

        Print out class mappings, properties and references.
        """
        return 'Class mappings:{} properties:{} references:{}'.format(
            self._class_mappings,
            self._class_properties,
            self._class_references
        )

    def _get_mapping(self, class_name):
        """ _get_mapping() method.

        :param str class_name: mapping class_name
        :return: self._class_mappings[class_name]
        :rtype: str

        Get class name from class_mappings dictionary by class_name.
        """
        return self._class_mappings[class_name]

    def get_references(self):
        """ get_references() method.

        :return: self._class_references
        :rtype: dict

        Get class references dictionary.
        """
        return self._class_references

    def _map(
        self,
        *,
        class_name,
        property_ref,
        parent_instance,
        children={}
    ):
        """ _map() method.

        :param dict *: used for passing params as **args dictionary
        :param str class_name: (root) class name
        :param dict property_ref: property reference dictionary
        :param classref parent_instance: property reference dictionary
        :param dict children: children definition dictionary

        Recursive map class hierarchy / class instances.
        """

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
    """ Service Mapper class.
    """

    def __init__(self, *, class_mapper, service_call_data):
        """
        :param dict *: used for passing params as **args dictionary
        :param classref class_mapper: class mapper instance reference
        :param dict service_call_data: service call metadata dictionary

        :ivar classref _class_mapper: set from class_mapper param
        """
        super().__init__()

        self._class_mapper = class_mapper

        class_references = self._class_mapper.get_references()

        root_class = next(iter(class_references))
        root_index = class_references[root_class]

        call_dict = {
            'class_name': root_class,
            'children': root_index['children'],
            'parent_instance': self._class_mapper,
            'hierarchy': service_call_data
        }

        self._map(**call_dict)

        try:
            for class_ref, class_props in class_references.items():
                for method_def in class_mapper._class_properties['SYSBackendMethods']:
                    if method_def[1] == 'on_recursion_finish':
                        self.logger.debug('SYSBackendMethod:{}'.format(method_def[0]))
                        try:
                            getattr(getattr(self._class_mapper, class_ref), method_def[0])()
                        except Exception as e:
                            pass
        except Exception as e:
            self.logger.debug('SYSBackendMethods preocessing exception:{}'.format(e))

    def _map(
        self,
        *,
        class_name,
        parent_instance,
        hierarchy,
        children={},
        property_ref=None
    ):
        """ _map() method.

        :param dict *: used for passing params as **args dictionary
        :param str class_name: (root) class name
        :param classref parent_instance: property reference dictionary
        :param dict hierarchy: (root) class setup item
        :param dict children: children definition dictionary
        :param dict property_ref: property reference dictionary

        Recursive process class hierarchy / service properties mapping.
        """

        self.logger.debug(
            'class_name:{} parent_instance:{} children:{} hierarchy:{}'.format(
                class_name,
                parent_instance,
                children,
                hierarchy
            )
        )

        class_instance = getattr(parent_instance, class_name)

        try:
            hierarchy = hierarchy[class_name]
            class_instance.set_properties(hierarchy)

            try:
                getattr(class_instance, class_instance.SYSServiceMethod)()
            except Exception as e:
                self.logger.debug('SYSServiceMethod call exception:{}'.format(e))

            for child_class_name, child_class_config in children.items():
                child_class_config['class_name'] = child_class_name
                child_class_config['parent_instance'] = class_instance
                child_class_config['hierarchy'] = hierarchy
                self._map(**child_class_config)

            try:
                for ci in class_instance._object_container:
                    getattr(ci, ci.SYSServiceMethod)()
            except Exception as e:
                self.logger.debug('SYSServiceMethod call exception:{}'.format(e))
        except Exception as e:
            self.logger.debug('Class reference in service call metadata not set:{}'.format(e))
            pass


class ServiceExecuter(object):
    """ Service Executer class.
    """

    def __init__(self):
        pass

    def execute(self, class_mapper, service_data):
        """
        :param classref class_mapper: class mapper instance reference
        :param list service_data: list of service call metadata dictionary items
        """

        rlist = []
        for item in service_data['data']:
            res = ServiceMapper(
                class_mapper=class_mapper,
                service_call_data=item
            )
            rlist.append(res)
        return rlist


# import classes into current namespace
current_mod = sys.modules[__name__]
import_classes = esbconfig.import_classes

for module_name in import_classes:
    mod_ref = importlib.import_module(module_name)
    for class_name in import_classes[module_name]:
        setattr(current_mod, class_name, getattr(mod_ref, class_name))
