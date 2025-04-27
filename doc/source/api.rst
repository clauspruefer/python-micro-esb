.. api

=================
API Documentation
=================

The following documents the **microesb** internal dependencies. It is not strictly necessary to understand these to implement or configure a working service setup.

.. note::

    You **should** continue reading to gain a better understanding of how internal processing works, especially *Multi-Class Handling*, before proceeding to the example section.

1. Base Handler
===============

The Abstract Base Class (ABC) must be inherited by the following sub-classes:

- ClassHandler
- MultiClassHandler

It provides template functions described in the *Internal Classes / Class Representation* subsection.

It inherits `transformer.JSONTransformer` to enable a generic, recursive dictionary representation of the class instance hierarchy. This feature allows for efficient assertions on complex object hierarchies.

Example test case (`/test/integration/test_base.py`, test: `test_multi_item_object`):

.. code-block:: python

    assert shipment.json_dict == {
        'id': 'testshipment1',
        'SYSServiceMethod': None,
        'Palette': [
            {'id': 1, 'label': 'label1'},
            {'id': 2, 'label': 'label2'}
        ]
    }

2. Class Handler
================

The `ClassHandler` class inherits from the `BaseHandler` class.

It provides template methods for *implementation classes* and the `ClassMapper` sub-class (see :ref:`implementation-classes`).

An *implementation class*, especially the *root class*, **must** inherit the `ClassHandler` class and explicitly call the parent (superclass) `__init__()` method.

Example:

.. code-block:: python

    from microesb import microesb

    class TestClass(microesb.ClassHandler):
        def __init__(self):
            super().__init__()

3. Multi-Class Handler
======================

The `MultiClassHandler` class also inherits from the `BaseHandler` class.

.. warning::

    It does not inherit from `ClassHandler`. Multi-class handling is only possible in *last level classes* or *endpoint classes*.

It *indirectly overloads* the necessary methods from `ClassHandler`. To see the differences, refer to the *Internal Classes / Class Representation* subsection.

Example: Standard `ClassHandler` vs. `MultiClassHandler` implementation:

.. code-block:: python

    from microesb import microesb

    class TestClass1(microesb.ClassHandler):
        def __init__(self):
            super().__init__()

    class TestClass2(microesb.MultiClassHandler):
        def __init__(self):
            super().__init__()

For an example *service call metadata* (Host properties), see Example 1 (:ref:`example-number1`).

4. Implementation Classes
=========================

Implementation classes are defined in the implementation phase and contain the programmed service logic.

.. note::

    Every *implementation class* **must** inherit either `ClassHandler` or `MultiClassHandler`. Only *endpoint classes* **may** inherit `MultiClassHandler`.

4.1. Abstraction
****************

The `ClassMapper` class is responsible for hierarchically mapping and connecting the desired *implementation classes*.

After `ClassMapper` sets up internal class instances, the `ServiceMapper` class populates these class instance properties with values from the provided *service call metadata*.

4.2. Inheritance
****************

An *implementation class* must inherit from either `microesb.ClassHandler` or `microesb.MultiClassHandler`.

Additionally, it **must** include the `super().__init__()` syntax in its constructor to ensure correct instantiation by the `ClassMapper`.

4.3. Class Properties Model
***************************

The `microesb` property model is a flat, OOP-based structure.

Consider two *implementation classes*: **Customer** as the root class and **Domain** as the child class of **Customer**.

- **Customer** properties (defined in the *service properties* config): `"Name"` and `"CustomerID"`.
- **Domain** properties: `"Name"` and `"Ending"` (with a default value of `'de'`).

Both class instances are set up by the `ClassMapper` in Python's global domain space.

Example of class member setup after `ClassMapper` invocation:

.. code-block:: python
    :linenos:

    class Customer(microesb.ClassHandler):
        self.Name = None
        self.CustomerID = None

    class Domain(microesb.ClassHandler):
        self.Name = None
        self.Ending = 'de'

4.4. ParentObject Properties
****************************

Using the example from 4.3, **Customer** is defined as the root class and **Domain** as its child class.

- Add the method `get_customer_dbdata()` as a public member of **Customer**.
- Add the method `do_something()` as a public member of **Domain**.

.. code-block:: python
    :linenos:

    class Customer(microesb.ClassHandler):
        self.Name = None
        self.CustomerID = None

        def get_customer_dbdata(self):
            self.CustomerID = dbquery('customerid_by_name')

    class Domain(microesb.ClassHandler):
        self.Name = None
        self.Ending = 'de'

        def do_something(self):
            print("CustomerID:{}".format(self.parent_object.CustomerID))

Calling `Customer.get_customer_dbdata()` sets `Customer.CustomerID` to a valid customer ID. Printing `self.parent_object.CustomerID` inside `Domain.do_something()` invokes the `BaseHandler.parent_object()` method, returning the `self._SYSParentObject` reference (due to the `@property` decorator).

4.5. Class Import
*****************

All *implementation classes* must be imported into the global Python namespace.

.. code-block:: python

    from microesb import microesb

Importing the main `microesb` module will call `import esbconfig` (see the following code, line 14).

.. code-block:: python
    :linenos:

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

The **microesb** standard installation will include an empty `esbconfig.py` in the global Python dist-packages or in the active Python environment.

.. warning::

    If you do not provide an `esbconfig.py` in your project folder, the default installation file will be used.

The following **esbconfig.py** tells the `microesb` importer to use the file **service_classes.py** and import *implementation classes* `Class1`, `Class2`, and `Class3` into the global namespace. These classes will then be usable by `ClassMapper` and `ServiceMapper` during internal processing.

.. code-block:: python

    import_classes = {
        'service_classes': [
            'Class1',
            'Class2',
            'Class3'
        ]
    }

.. note::

    The Python module containing the implementation classes must also be present in the project folder.

5. Class Mapper
===============

The `ClassMapper` class is responsible for hierarchically mapping and connecting the desired *implementation classes*.

The `ClassMapper` class must be invoked during initialization or before the `ServiceMapper`. It requires the following configuration dictionaries as input parameters:

- **Class Reference Dictionary** (see "Configuration / :ref:`class-reference-config`")
- **Class Mapping Dictionary** (see "Configuration / :ref:`class-mapping-config`")
- **Service Properties Dictionary** (see "Configuration / :ref:`service-properties-config`")

Example:

.. code-block:: python

    class_reference = { ... }
    class_mapping = { ... }
    service_properties = { ... }

    class_mapper = microesb.ClassMapper(
        class_references=class_reference,
        class_mappings=class_mapping,
        class_properties=service_properties
    )

6. Service Mapper
=================

The `ServiceMapper` class is responsible for mapping and populating the existing class instances (created by `ClassMapper`) with the given *service call metadata*.

It requires the following as input parameters:
- A reference to the `ClassMapper` instance
- **Service Call Metadata Dictionary** (see "Configuration / :ref:`service-call-metadata-config`")

Example:

.. code-block:: python

    service_metadata = { ... }

    res = microesb.ServiceMapper(
        class_mapper=class_mapper,
        service_data=service_metadata
    )
