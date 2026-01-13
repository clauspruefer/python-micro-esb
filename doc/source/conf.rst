.. conf

=============
Configuration
=============

This document describes how to configure and set up the **microesb** backend to process *Service Call Metadata*.

.. note::

    Refer to subsection :ref:`example-test-execution` to see how to use the configuration data and execute a working setup.

.. _class-reference-config:

1. Class Reference
==================

A *Class Reference Config* dictionary must be provided to describe the *Hierarchical Implementation Class Setup* and its dependencies.

1.1. Root Element
*****************

The root dictionary consists of elements `"class_config_element"` (recursive). See :ref:`class-config-element`.

.. code-block:: python

    class_reference = {
        '$class_name1': { ... "class_config_element" dict ... },
        '$class_name2': { ... "class_config_element" dict ... },
        '$class_name3': { ... "class_config_element" dict ... }
    }

.. note::

    The `$class_name` key **must** reference an **existing** *Implementation Class*.

.. _class-config-element:

1.2. Class Config Element
*************************

The *class_config_element* consists of two properties: **property_ref** and **children**.

.. list-table:: Class Reference - "class_config_element" Properties
    :widths: 15 15 70
    :header-rows: 1

    * - Property
      - Type
      - Description
    * - property_ref
      - str
      - Maps the class to properties defined in the *Service Property Config*.
    * - children
      - dict
      - "class_config_element" (recursive). See :ref:`class-ref-example`.

.. code-block:: python

    class_config_element = {
        'property_ref': '$service_property_ref',
        'children': { ... "class_config_element" dict ... }
    }

.. warning::

    A *class_config_element* must only contain a **single** root element.

.. note::

    A dictionary structure like `{ 'root_element': { ... } }` is valid.
    However, multiple root elements (e.g., `{ 'root_element1': { ... }, 'root_element2': { ... } }`) will cause dependency issues.

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

    Section :ref:`examples-global` provides detailed and working examples.

1.4. Property Reference
***********************

The `property_ref` defines which properties (defined in the *Service Property Config*) will be **mapped** to the dictionary key (class name).

.. _service-properties-config:

2. Service Properties
=====================

The *Service Property Config* dictionary maps properties to *Implementation Classes*.

Only properties defined inside the *Service Property Config* are addressable and referenceable from the *Service Call Metadata Config*.

.. note::

    If a property mentioned in the *Service Call Metadata* is not configured in the *Service Property Config*, it will be silently ignored.

2.1. Root Element
*****************

The root-level dictionary key **must** reference an existing *Implementation Class*.

.. code-block:: python

    service_properties = {
        '$class_name1': { },
        '$class_name2': { },
        '$class_name3': { },
    }

The values are dictionaries with allowed keys `properties` and `methods`.

2.2. SYSBackendMethods
**********************

The **SYSBackendMethods** property is a system property that triggers *Service Method Invocation* from the backend. This is different from **SYSServiceMethod(s)**, which is only defined in the *Service Call Metadata*.

The type is a list of 2-element tuples: `[ (Element1, Element2) ]`.

- **Element1**: A string that specifies the backend class method.
- **Element2**: A string that specifies the trigger type.

.. note::

    Currently, the only allowed trigger type for **Element2** is `'on_recursion_finish'`.

Example:

.. code-block:: python

    properties_dict = {
        'SYSBackendMethods': [
            ('gen_cert', 'on_recursion_finish')
        ],
        'properties': { ... }
    }

2.3. Property Element
*********************

The "property" element is of `dict` type.

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
      - DictValue defined in "type"
      - Dynamic
      - no
      - Default value or `None`.
    * - required
      - bool
      - True | False
      - no
      - Indicates whether the property is mandatory.
    * - description
      - str
      - str
      - yes
      - Provides a description of the property.

Example:

.. code-block:: python

    '$property_name': {
        'type': 'str' || 'int',
        'default': '$value' || None,
        'required': True || False,
        'description': 'Internal property description for autodoc'
    }

2.4. Methods List
*****************

The "methods" list contains `methodname (str)` items.

Each method name references a callable method of a defined *Implementation Class*.

Example:

.. code-block:: python

    'methods': [ 'method1', 'method2', 'method3' ]

.. warning::

    This feature is currently unused. It will play a role in the *Service Registry* and *Service Autodoc* features, which are not yet implemented.

.. note::

    *Method Mapping* occurs only if the "SYSServiceMethod" property exists in the *Service Call Metadata Config*.

2.5. Full Syntax
****************

Example of the complete syntax for the *Service Property Config*:

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

2.6. Example
************

Example configuration:

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
    }

3. Class Mappings
=================

The *Class Mapping Config* dictionary defines the mapping between class names used in the *Class Reference Config* and the actual *Implementation Classes*.

3.1. Dictionary Format
**********************

The *Class Mapping Config* is a simple dictionary where each key represents a class name used in the configuration, and each value represents the corresponding *Implementation Class* name.

.. code-block:: python

    class_mapping = {
        '$config_class_name1': '$implementation_class_name1',
        '$config_class_name2': '$implementation_class_name2',
        '$config_class_name3': '$implementation_class_name3'
    }

3.2. Flat Mappings
******************

In most cases, a "flat" mapping is used where each class name maps directly to itself. This is a 1:1 mapping without any aliasing.

.. note::

    All examples in this documentation use flat mappings without aliasing.

Example from :ref:`example-number1`:

.. literalinclude:: ../../example/01-hosting-use-case/class_mapping.py
    :linenos:

Example from :ref:`example-number2`:

.. literalinclude:: ../../example/02-pki-management/class_mapping.py
    :linenos:

3.3. Aliasing
*************

**Aliasing** is a more advanced technique that **must** be used when adding multiple classes with the same name as child classes to a parent class.

With aliasing, multiple different configuration class names can map to the same *Implementation Class*. This allows you to instantiate the same class type multiple times with different property values in a hierarchical structure.

.. warning::

    Aliasing is only necessary when you need multiple child instances of the same class type under a single parent. For simple hierarchies, use flat mappings.

3.4. Aliasing Example
*********************

The integration test `TestMapping.test_class_mapping` in `/test/integration/test_base.py` demonstrates the use of aliasing:

.. code-block:: python

    class_mapping = {
        'CertCA': 'CertCA',
        'SmartcardCA': 'Smartcard',
        'SmartcardREQ': 'Smartcard',
        'SmartcardContainer': 'SmartcardContainer'
    }

In this example:

- `SmartcardCA` and `SmartcardREQ` are aliases that both map to the `Smartcard` implementation class.
- This allows the `CertCA` parent class to have two separate child instances of the `Smartcard` class with different configurations.
- Each alias can be referenced independently in the *Class Reference Config* and *Service Call Metadata*.

The corresponding *Class Reference Config* shows how these aliases are used:

.. code-block:: python

    class_reference = {
        'CertCA': {
            'property_ref': 'Cert',
            'children': {
                'SmartcardCA': {
                    'property_ref': 'Smartcard',
                    'children': {
                        'SmartcardContainer': {'property_ref': 'SmartcardContainer'}
                    }
                },
                'SmartcardREQ': {
                    'property_ref': 'Smartcard',
                    'children': {
                        'SmartcardContainer': {'property_ref': 'SmartcardContainer'}
                    }
                }
            }
        }
    }

.. note::

    For more information on aliasing in practical use, see :ref:`example-number3` in the Examples documentation.

5.3. Test Execution
*******************

Before executing the configuration, ensure all referenced files are correctly provided:

1. `esbconfig.py` (import module and classes)
2. `implementation_classes.py` (referenced in `esbconfig.py`)
3. `class_reference.py` (class reference configuration)
4. `service_properties.py` (service properties configuration)
5. `class_mapping.py` (class mapping configuration)
6. `service_metadata.py` (service call metadata)

Example execution:

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
