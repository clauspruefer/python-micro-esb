.. conf

=============
Configuration
=============

The following subsection describes how to configure / setup the **microesb`s**
backend to process *service call metadata*.

.. note::

    Subsection :ref:`example-test-execution` shows how to use the configuration data finally
    and execute to check a working setup.

.. _class-reference-config:

1. Class Reference
==================

A *Class Reference* (type dictionary) config must be provided to describe the
hierachical *implementation class* setup and its dependencies.

1.1. Root Element
*****************

Dictionary of elements "class_config_element" (recursive),
see :ref:`class-config-element`.

.. code-block:: python

    class_reference = {
       '$class_name1': { ... "class_config_element" dict ... },
       '$class_name2': { ... "class_config_element" dict ... },
       '$class_name3': { ... "class_config_element" dict ... }
       }
    }

The $class_name key **must** point (reference) to an **existing**
*implementation class*.

.. _class-config-element:

1.2. Class Config Element
*************************

The *class_config_element* consists of two properties **property_ref**
and **children**.

.. list-table:: Class Reference - "class_config_element" Properties
    :widths: 15 15 70
    :header-rows: 1

    * - Property
      - Type
      - Description
    * - property_ref
      - str
      - Must map to its own on default usage.
    * -
      -
      - On *virtual class types* usage, map to parent class name.
    * - children
      - dict
      - "class_config_element" (recursive). See :ref:`class-ref-example`.

.. code-block:: python

    class_config_element = {
       'property_ref': '$parent_class_name',
       'children': { ... "class_config_element" dict ... }
    }

.. _class-ref-example:

1.3. Example
************


.. code-block:: python
    :linenos:

    class_reference = {
        'Class1': {
            'property_ref': 'Class1',
            'children': {
                'Class2': {
                    'property_ref': 'Class2',
                    'children': {
                        'Class3': {
                            'property_ref': 'Class3'
                        }
                    }
                }
            }
        }
    }

.. note::

    Section :ref:`examples-global` provides more detailed (working) examples.

1.4. Property Reference
***********************

Property references without mapping to the own hierarchy level only play a role
in combination with *class mapping* / *virtual class types*.

Without enabled *virtual class types* "property_ref" always must contain the
class name from the same hierarchy level / from its own.

.. note::

    Example number 2 describes using *virtual class types* in detail (see :ref:`example-number2`).

.. _service-properties-config:

2. Service Properties
=====================

The *Service Properties* (type dictionary) config maps properties to
*implementation classes*.

Only when a property value is defined inside *Service Properties* config, it is
addressable / referencable from *Service Call Metadata* config.

.. note::

    If a property given in *Service Call Metadata* is not configured in
    *Service Properties* config it will be silently ignored.

2.1. Root Element
*****************

The root level dictionary key **must** be the reference to an existing
*implementation class*.

.. code-block:: python

    service_properties = {
        '$class_name1': { },
        '$class_name2': { },
        '$class_name3': { },
    }

The value is dictionary type with enum key 'properties', 'methods'.

.. code-block:: python

    properties_dict = {
       'properties': {
          '$prop1': { ... "property" dict (1) ... },
          '$prop2': { ... "property" dict (2) ... },
          '$prop3': { ... "property" dict (3) ... },
       },
       'methods': [ ... methods list, see 2.3. ... ]
    }

2.2. Property Element
*********************

Element "property" is `dict` type.

.. list-table:: Service Properties - "property" Element
    :widths: 10 30 10 10 40
    :header-rows: 1

    * - DictKey
      - DictValue Type
      - DictValue Value
      - Opt
      - Description
    * - type
      - enum(Python types)
      - [ 'str', 'int' ]
      - no
      - Usable internal Python types.
    * - default
      - Set in "type" DictKey
      - Dynamic
      - no
      - Default value or None.
    * - required
      - bool
      - True | False
      - no
      - Property is mandatory or not.
    * - description
      - str
      - str
      - yes
      - Property description.

.. code-block:: python

    '$property_name': {
        'type': 'str' || 'int',
        'default': '$value' || None,
        'required': True || False,
        'description': 'Internal property description for autodoc'
    }

2.3. Methods List
*****************

"methods" list item is `methodname (str)` type.

A methodname is the reference to a callable method of a defined
*implementation class*.

.. code-block:: python

    'methods': [ 'method1', 'method2', 'method3' ]

.. warning::

    Currently unused. It only will play a role in *service registry* and
    *service autodoc* feature, which are unimplemented yet.

.. note::

    Method *mapping* only happens if "SYSServiceMethod" property exists in
    *service call metadata* config.

2.4. Full Syntax
****************

.. code-block:: python

    service_properties = {
        '$class_name1': {
            'properties': {
               '$prop1': { ... "property" dict (1) ... },
               '$prop2': { ... "property" dict (2) ... },
               '$prop3': { ... "property" dict (3) ... }
            },
            'methods': [ ... "methodname" list ... ]
        },
        '$class_name2': {
            'properties': {
               '$prop1': { ... "property" dict (1) ... },
               '$prop2': { ... "property" dict (2) ... },
               '$prop3': { ... "property" dict (3) ... }
            },
            'methods': [ ... "methodname" list ... ]
        },
    }

2.5. Example
************

.. code-block:: python
    :linenos:

    service_properties = {
        'User': {
            'properties': {
                'name': {
                    'type': 'str',
                    'default': None,
                    'required': True,
                    'description': 'Textual UserID'
                }
            },
            'methods': [ 'add', 'delete' ]
        },
        'Domain': {
            'properties': {
                'name': {
                    'type': 'str',
                    'default': None,
                    'required': True,
                    'description': 'Domain Name'
                },
                'ending': {
                    'type': 'str',
                    'default': 'de',
                    'required': False,
                    'description': 'Domain Ending'
                }
            },
            'methods': [ 'add', 'update', 'delete' ]
        }

.. _class-mapping-config:

3. Class Mapping
================

The class mapping dictionary is an extension to *class reference config* and
*service properties config*.

It enables *virtual class types*, a feature where mapping multiple *service meta data*
objects to a single class reference config / implementation class is possible.

.. note::

    Without using *virtual class types* each individual class **must** map to its own.

For the given example in section :ref:`class-ref-example` the class mapping
must be defined like the following.

.. code-block:: python

    class_mapping = {
       'Class1': 'Class1',
       'Class2': 'Class2',
       'Class3': 'Class3'
    }

.. _service-call-metadata-config:

4. Service Call Metadata
========================

*Service Call Metadata* is the metadata which will be passed to the backend on
service invocation.

4.1. Root Dictionary
********************

The root dictionary consists of two properties **SYSServiceID** and **data**.

.. list-table:: Service Call Metadata - Root Dictionary
    :widths: 15 10 5 80
    :header-rows: 1

    * - DictKey
      - DictValue Type
      - Opt
      - Description
    * - SYSServiceID
      - str
      - no
      - Backend Service ID,
    * -
      -
      -
      - currently not implemented!
    * - data
      - list of dict (ClassSetupElement)
      - no
      - Provides sending multiple object data
    * -
      -
      -
      - at once.

.. code-block:: python

    root = {
        'SYSServiceID': 'ServiceIdentification',
        'data': [
            { ... ClassSetupElement dict (1) ... },
            { ... ClassSetupElement dict (2) ... }
        ]
    }

4.2. Class Setup Element
************************

The "class_setup_element" dictionary can consist of the following keys.

1. "SYSServiceMethod"

Tells the backend which class method to invoke. If a class method is referenced
which does not exist it will be silently ignored. Can be ommitted in some cases
(e.g. when a class only contains logic inside constructor).

2. "$property_name"

Provide multiple class property values. If property has not been configured in
*Service Properties* config, it will be silently ignored.

3. "$class_name"

*Implementation class* reference. Value must be "class_setup_element" dictionary,
which makes setup recursive. On a non-existent reference an exception will be raised.

.. list-table:: Service Call Metadata - "class_setup_element"
    :widths: 15 10 5 80
    :header-rows: 1

    * - DictKey
      - DictValue Type
      - Opt
      - Description
    * - SYSServiceMethod
      - str
      - yes
      - Backend class method reference.
    * - $property_name
      - Property type dependend
      - yes
      - Class property name.
    * - $class_name
      - dict (ClassSetupElement)
      - yes
      - Implementation class reference.

.. code-block:: python

    {
        'SYSServiceMethod': '$service_method',
        '$property_name1': 'value1',
        '$property_name2': 'value2',
        '$property_name3': 'value3',
        '$class_name':
           { ... 'class_setup_element' dict ... }
    }

4.3. MultiClass Setup List
**************************

Is `list` of `multiclass_setup_element (dict)` type.

.. note::

    If an *implementation class* inherits **microesb.MultiClassHandler** the
    corresponding $class_name dict value in *service call metadata* **must** be
    "multiclass_setup_list" list type not "class_setup_element" dictionary type.

.. code-block:: python

    '$class_name': [
        {
            'SYSServiceMethod': '$service_method',
            '$property_name1': 'value1',
            '$property_name2': 'value2',
            '$property_name3': 'value3'
        },
    ]

4.4. MultiClass Setup Element
*****************************

The "multiclass_setup_element" dictionary can consist of the following keys.

1. "SYSServiceMethod"

Tells the backend which class method to invoke. If a class method is referenced
which does not exist it will be silently ignored. Can be ommitted in some cases
(e.g. when a class only contains logic inside constructor).

2. "$property_name"

Provide multiple class property values. If property has not been configured in
*Service Properties* config, it will be silently ignored.

.. note::

    It may not contain a "$class_name, class_setup_element" key / value pair
    unlike the "class_setup_element" dictionary.

.. list-table:: Service Call Metadata - "multiclass_setup_element"
    :widths: 15 10 5 80
    :header-rows: 1

    * - DictKey
      - DictValue Type
      - Opt
      - Description
    * - SYSServiceMethod
      - str
      - no
      - Backend class method reference.
    * - $property_name
      - Property type dependend
      - yes
      - Class property name.

.. code-block:: python

    {
        'SYSServiceMethod': '$service_method',
        '$property_name1': 'value1',
        '$property_name2': 'value2',
        '$property_name3': 'value3'
    }

4.5. Complete Example
*********************

Example taken from example number 1 (:ref:`example-number1`).

.. literalinclude:: ../../example/01-hosting-use-case/service_call_metadata.py

- Class "User" instance will be setup with property "id", value "testuser1"
- Config "User" does not provide a "SYSServiceMethod", no "User" method called
- Config "Domain" provides "name" and "ending" properties
- Config "Domain" provides a "SYSServiceMethod" property with value "add"
- Class method "Domain".add() will be called using given service properties
- Config Host (1) provides a "SYSServiceMethod" property with value "add"
- Class method "Host".add() will be called using given service properties
- Config Host (2) provides a "SYSServiceMethod" property with value "add"
- Class method "Host".add() will be called using given service properties

5. Implementation Setup
=======================

The last step after setting up *class reference* config, *service properties*
config, *class mapping* config and sample *service call metadata* is to provide
the implementation.

To get the implementation working you need the following.

1. *Implementation classes* containing the python program logic
2. File `esbconfig.py` including *import configuration*

5.1. Implementation Classes
***************************

.. code-block:: python

    from microesb import microesb


    class TestClass1(microesb.ClassHandler):
        def __init__(self):
            super().__init__()

    class TestClass2(microesb.MultiClassHandler):
        def __init__(self):
            super().__init__()

5.2. Import Configuration
*************************

The import configuration **must** be named `esbconfig.py` and reside in the
same folder where the microesb main module import happens.

.. code-block:: python

    import_classes = {
       'test_classes': [
          'TestClass1',
          'TestClass2'
       ]
    }


.. _example-test-execution:

5.3. Test Execution
*******************

Before execution, recheck if all referenced configuration files have been
provided.

1. esbconfig.py (import module and classes)
2. implementation_classes.py (referenced in esbconfig.py)
3. class_reference.py (class reference config)
4. service_properties.py (service properties config)
5. class_mapping.py (class mapping config)
6. service_metadata.py (service call metadata)

.. code-block:: python

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
