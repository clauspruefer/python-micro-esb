# ]*[ --------------------------------------------------------------------- ]*[
#  .                         Micro ESB Python Module                         .
# ]*[ --------------------------------------------------------------------- ]*[
#  .                                                                         .
#  .  Copyright Claus Prüfer (2016 - 2026)                                   .
#  .                                                                         .
#  .                                                                         .
# ]*[ --------------------------------------------------------------------- ]*[

import os
import abc
import sys
import copy
import logging
import importlib

from microesb.router import ServiceRouter
from microesb.transformer import JSONTransformer


try:
    esb_python_path = os.environ['esbpythonpath']
    os.environ['PYTHONPATH'] = esb_python_path
except KeyError as e:
    pass

try:
    esbconf_mod_name = os.environ['esbconfig']
except KeyError as e:
    esbconf_mod_name = 'esbconfig'

esbconf_mod_ref = importlib.import_module(esbconf_mod_name)

logging_enabled = True
try:
    logging_enabled = esbconf_mod_ref.config['logging_enabled']
except AttributeError as e:
    pass

if logging_enabled is False:
    logging.getLogger(__name__).propagate = False


class BaseHandler(JSONTransformer, metaclass=abc.ABCMeta):
    """ Abstract Base Class (ABC) Meta Class.
    """

    def __init__(self):
        """
        :ivar classref logger: logging logger reference
        :ivar dict[SYSProperties] _SYSProperties: internal properties processing dict
        :ivar classref _SYSParentObject: internal (hierarchical) class instance ref
        :ivar list[classname] _SYSClassNames: internal class names dict
        """

        self.logger = logging.getLogger(__name__)

        self._SYSProperties = None
        self._SYSPropertiesRegister = {}
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

        :return: generator yielding class instances in hierarchy
        :rtype: generator
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
        properties.update(self._SYSPropertiesRegister)

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

    def register_property(self, property_id, property_item):
        """ register_property() method.

        :param str property_id: property id (internal class attribute name)
        :param dict property_item: property item to be registered for internal processing only

        Modifying data internally (inside a Service-Implementation) requires setting
        additional properties not defined in Service-Properties, e.g. generated data,
        time-stamps or similar.

        Service-Implementation classes should call this method to register such
        additional internal properties for processing by the Micro ESB framework.        """
        self._SYSPropertiesRegister[property_id] = property_item

    def _set_property(self, property_id, value):
        """ _set_property() method.

        :param str property_id: property dict key
        :param str value: property value

        """
        if property_id in self._SYSProperties:
            setattr(self, property_id, value)

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
    def property_dict(self):
        """ property_dict() method.

        Return all classes self._SYSProperties property_id, value dictionary.

        :return: dictionary of all properties excluding 'SYSServiceMethod'
        :rtype: dict

        Decorated with @property so direct property access possible
        """

        return_dict = {}
        for property_id in self._SYSProperties:
            if property_id != 'SYSServiceMethod':
                return_dict[property_id] = self.get_value_by_property_id(property_id)
        return return_dict

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

    def get_value_by_property_id(self, property_id):
        """ get_value_by_property_id() method.

        :param str property_id: property identifier
        :return: attribute value for given property_id
        :rtype: dynamic
        """
        return getattr(self, property_id)


class ClassHandler(BaseHandler):
    """ ClassHandler class. Inherits BaseHandler class.
    """

    def __init__(self):
        """
        :ivar str _SYSType: const internal system type to differentiate handler types
        :ivar classref _ServiceRouter: ServiceRouter instance reference
        """
        super().__init__()
        self._SYSType = 'class_instance'
        self._ServiceRouter = ServiceRouter()

    def __add__(self, args):
        """ overloaded internal __add__() method (+ operator).

        :param dict args: class setup dictionary

        _add_class() "wrapper" primary used for ClassMapper.

        >>> args = {
        >>>     'class_name': class_name,
        >>>     'class_ref': class_ref
        >>> }
        >>> class_instance + args
        """
        self._add_class(**args)

    def __iter__(self):
        """ overloaded internal __iter__() method.

        Overloaded for using iter() on class references.

        :return: generator yielding class instances from _SYSClassNames
        :rtype: generator
        """
        for class_name in self._SYSClassNames:
            yield getattr(self, class_name)

    def _add_class(self, *, class_name, class_ref):
        """ _add_class() method.

        :param dict *: used for passing params as **args dictionary
        :param str class_name: class name
        :param classref class_ref: class instance reference name

        Append class_name to self._SYSClassNames. Setup new class instance
        in global namespace.

        Primary called by overloaded __add__() method.
        """

        self._SYSClassNames.append(class_name)

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

        Propagate self.json_dict with current class instance attribute values (self._SYSProperties)
        and with empty (None) class instance references (processed from JSONTransformer).

        Removes 'SYSServiceMethod' from json_dict and initializes child class references to None.
        """

        for property_id in self._SYSProperties:
            self.logger.debug('processing property:{}'.format(property_id))
            self.json_dict[property_id] = getattr(self, property_id)

        try:
            del self.json_dict['SYSServiceMethod']
        except KeyError as e:
            pass

        self.logger.debug('self._SYSProperties:{}'.format(self._SYSProperties))

        for class_name in self._SYSClassNames:
            self.json_dict[class_name] = None

        self.logger.debug('JSONDict:{}'.format(self.json_dict))


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

        :return: generator yielding class instances from _object_container
        :rtype: generator
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

        Prepare self.json_dict from self._object_container.

        Iterates through all instances in _object_container and appends their
        json_dict to create a list. Removes empty entries.
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

        Prepare self.json_dict from self._SYSProperties (used by JSONTransformer).

        Extracts all property values and populates json_dict, ignoring any errors
        from missing or inaccessible attributes.
        """
        for property_id in self._SYSProperties:
            try:
                self.json_dict[property_id] = getattr(self, property_id)
            except (KeyError, TypeError, AttributeError) as e:
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

        :return: formatted string with class mappings, properties and references
        :rtype: str
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

    def get_class_hierarchy(self):
        """ get_class_hierarchy() method.

        :return: self._class_hierarchy
        :rtype: dict

        Get class hierarchy dictionary.
        """
        return self._class_hierarchy

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
        :param classref parent_instance: object reference
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
                        except (TypeError, AttributeError) as e:
                            pass
        except (KeyError, TypeError, AttributeError) as e:
            self.logger.debug('SYSBackendMethods processing exception:{}'.format(e))

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
            except (TypeError, AttributeError) as e:
                self.logger.debug('SYSServiceMethod get-attribute exception:{}'.format(e))

            for child_class_name, child_class_config in children.items():
                child_class_config['class_name'] = child_class_name
                child_class_config['parent_instance'] = class_instance
                child_class_config['hierarchy'] = hierarchy
                self._map(**child_class_config)

            try:
                for ci in class_instance._object_container:
                    getattr(ci, ci.SYSServiceMethod)()
            except (TypeError, AttributeError) as e:
                self.logger.debug('SYSServiceMethod call exception:{}'.format(e))
        except (KeyError, TypeError, AttributeError) as e:
            self.logger.debug('Class reference in service call metadata not set:{}'.format(e))


class ServiceExecuter():
    """ Service Executer class.
    """

    def __init__(self):
        """
        :ivar classref logger: logging logger reference
        :ivar classref _cm_ref: class mapper reference
        :ivar dict _con_ref_dict: connection reference dictionary
        :ivar dict _class_hierarchy: class hierarchy dictionary
        :ivar list _class_hierarchy_list: list of class hierarchy items
        :ivar int _hierarchy_level: current hierarchy level counter
        :ivar int _map_hierarchy_level: mapping hierarchy level counter
        :ivar dict _class_hierarchy_comp: class hierarchy comparison dictionary
        :ivar int _hierarchy_level_comp: hierarchy level comparison counter
        """

        self.logger = logging.getLogger(__name__)

        self._cm_ref = None
        self._con_ref_dict = None
        self._class_hierarchy = None
        self._class_hierarchy_list = None
        self._hierarchy_level = None
        self._map_hierarchy_level = None
        self._class_hierarchy_comp = None
        self._hierarchy_level_comp = None

    def execute(self, class_mapper, service_data):
        """ execute() method.

        Execute service calls by creating ServiceMapper instances for each data item.

        :param classref class_mapper: class mapper instance reference
        :param dict service_data: data dictionary with 'data' key containing list of items
        :return: list of ServiceMapper instances
        :rtype: list
        """

        rlist = []
        for item in service_data['data']:
            class_mapper_copy = copy.deepcopy(class_mapper)
            sm_ref = ServiceMapper(
                class_mapper=class_mapper_copy,
                service_call_data=item
            )
            rlist.append(sm_ref)
        return rlist

    def execute_get_hierarchy(self, class_mapper, service_data):
        """ execute_get_hierarchy() method.

        Execute service calls and return connected class hierarchies with json_dicts.

        :param classref class_mapper: class mapper instance reference
        :param dict service_data: data dictionary with 'data' key containing list of items
        :return: list of connected class hierarchy dictionaries
        :rtype: list
        """

        rlist = []
        for item in service_data['data']:
            class_mapper_copy = copy.deepcopy(class_mapper)
            ServiceMapper(
                class_mapper=class_mapper_copy,
                service_call_data=item
            )
            rlist.append(
                self._connect_hierarchy(class_mapper_copy)
            )
        return rlist

    def _connect_hierarchy(self, class_mapper_ref):
        """ _connect_hierarchy() method.

        Init method for connecting all generated json_dicts.

        :param classref class_mapper_ref: class mapper instance reference
        :return: connected class hierarchy reference dictionary
        :rtype: dict
        """

        self._cm_ref = class_mapper_ref
        cm_ref_dict = self._cm_ref.get_references()

        self.logger.debug('Processing class_mapper references dict:{}'.format(cm_ref_dict))
        self.logger.debug('Mapping parent_object instances to child instances')

        self._map_hierarchy_level = -1
        self._map_object_instances(cm_ref_dict)

        sum_children = ChildCounter().get_sum_child_count(cm_ref_dict)
        self.logger.debug('Sum children:{}'.format(sum_children))

        while sum_children > 0:

            self._hierarchy_level = -1
            self._class_hierarchy = {}
            self._class_hierarchy_list = []

            self._connect_hierarchy_recursive(cm_ref_dict)

            self.logger.debug('Class hierarchy list:{}'.format(
                self._class_hierarchy_list)
            )

            for class_hierarchy_item in self._class_hierarchy_list:

                self._class_hierarchy_comp = {}
                self._hierarchy_level_comp = -1

                self._class_hierarchy = class_hierarchy_item

                self._rename_dict_key(cm_ref_dict)
                self.logger.debug('Renamed children dict:{}'.format(cm_ref_dict))

            sum_children = ChildCounter().get_sum_child_count(cm_ref_dict)
            self.logger.debug('Sum children:{}'.format(sum_children))

        return cm_ref_dict

    def _map_object_instances(self, ref_dict):
        """ _map_object_instances() method.

        Recursively map object instances to reference dictionary and perform JSON transform on root.

        :param dict ref_dict: reference dictionary to process
        """

        for class_name, class_props in ref_dict.items():

            if 'children' in class_props:

                child_dict = class_props['children']
                key_first = next(iter(child_dict))
                elm_first = child_dict[key_first]
                ref_dict[class_name]['object_instance'] = elm_first['parent_instance']

                self._map_hierarchy_level += 1
                self._map_object_instances(class_props['children'])
                self._map_hierarchy_level -= 1

            if self._map_hierarchy_level == -1:
                self.logger.debug('Root object JSON transform:{}'.format(class_name))
                class_props['object_instance'].json_transform()

    def _connect_hierarchy_recursive(self, reference_dict, parent_class=None, parent_dict=None):
        """ _connect_hierarchy_recursive() method.

        Recursively connect all generated json_dicts to their parents.

        :param dict reference_dict: reference dictionary to process
        :param str parent_class: parent class name (optional)
        :param dict parent_dict: parent dictionary reference (optional)
        """

        self.logger.debug('Parent dict:{}'.format(parent_dict))

        if parent_class is not None:
            self._class_hierarchy[self._hierarchy_level] = parent_class

        for class_name, class_properties in reference_dict.items():

            if 'children' in class_properties:
                self._hierarchy_level += 1
                self._connect_hierarchy_recursive(
                    class_properties['children'],
                    class_name,
                    reference_dict
                )
                del self._class_hierarchy[self._hierarchy_level]
                self._hierarchy_level -= 1
            else:
                parent_instance = class_properties['parent_instance']
                parent_class_name = parent_instance.class_name
                src_instance = getattr(parent_instance, class_name)
                parent_instance.json_dict[class_name] = src_instance.json_dict

                self.logger.debug('Mapping class_name:{} parent_class_name:{}'.format(
                    class_name,
                    parent_class_name))

                self._class_hierarchy_list.append(
                    copy.deepcopy(self._class_hierarchy)
                )

    def _rename_dict_key(self, rename_dict, parent_dict=None, parent_class=None):
        """ _rename_dict_key() method.

        Recursively rename 'children' keys to 'children_processed' when hierarchy matches.

        :param dict rename_dict: dictionary to process
        :param dict parent_dict: parent dictionary reference (optional)
        :param str parent_class: parent class name (optional)
        """

        self.logger.debug('Parent class:{}'.format(parent_class))
        self.logger.debug('RenameDict:{}'.format(rename_dict))

        if parent_class is not None:
            self._class_hierarchy_comp[self._hierarchy_level_comp] = parent_class

        if self._class_hierarchy == self._class_hierarchy_comp:
            self.logger.debug('Match rename_dict:{}'.format(rename_dict))

            # only remove when all 'children' keys have been altered to 'children_processed'
            if ChildCounter().get_sum_child_count(dict(rename_dict)) == 0:
                self.logger.debug('Parent dict:{}'.format(parent_dict))
                set_dict = parent_dict[parent_class].pop('children')
                parent_dict[parent_class]['children_processed'] = set_dict

        for class_name, class_properties in rename_dict.items():
            if 'children' in class_properties:
                self._hierarchy_level_comp += 1
                self._rename_dict_key(
                    class_properties['children'],
                    rename_dict,
                    class_name
                )
                del self._class_hierarchy_comp[self._hierarchy_level_comp]
                self._hierarchy_level_comp -= 1


class ChildCounter():
    """ Child node counter class.
    """

    def __init__(self):
        """
        :ivar int _children_occurrences: counter for children node occurrences
        :ivar classref logger: logging logger reference
        """
        self._children_occurrences = 0
        self.logger = logging.getLogger(__name__)

    def get_sum_child_count(self, reference_dict):
        """ get_sum_child_count() method.

        Count children nodes recursively and return sum.

        :param dict reference_dict: reference dictionary to process
        :return: total count of 'children' keys in hierarchy
        :rtype: int
        """

        self.logger.debug('Sum count ref-dict:{}'.format(reference_dict))

        for class_name, class_properties in reference_dict.items():
            if 'children' in class_properties:
                self._children_occurrences += 1
                self.get_sum_child_count(class_properties['children'])

        return self._children_occurrences


# import classes into current namespace
current_mod = sys.modules[__name__]
import_classes = esbconf_mod_ref.import_classes

for module_name in import_classes:
    mod_ref = importlib.import_module(module_name)
    for class_name in import_classes[module_name]:
        setattr(current_mod, class_name, getattr(mod_ref, class_name))
