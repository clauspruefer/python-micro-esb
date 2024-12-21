.. api

=================
API Documentation
=================

The following documents the **microesb`s** internal dependencies, it is not
strictly neccessary to understand how to implement / configure a working service
setup.

.. note::

    **As a tip**, you *should* read further to get a better understanding how
    internal processing works, especially *Multi Class Handling* before you continue
    to the example section.

1. Base Handler
===============

Abstract Base Class (ABC) which must be inherited by the following sub-classes.

- ClassHandler
- MultiClassHandler

It provides template functions described in *Internal Classes / Class
Representation* subsection.

It inherits transformer.JSONTransformer to enable a generic, recursive dict
representation of the class instance hierarchy.

Which in turn enables a smart way to do asserts on complex object hierarchy-

See /test/integration/test_base.py, test "test_multi_item_object".

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

The ClassHandler class inherits the BaseHandler Class.

The ClassHandler class provides template methods for *implementation classes*
and the ClassMapper sub-class (see :ref:`implementation-classes`).

An *implementation class*, especially the *root class* **must** inherit the
ClassHandler class and explicitely call the parents (super class) __init__()
method.

.. code-block:: python

    from microesb import microesb


    class TestClass(microesb.ClassHandler):
        def __init__(self):
            super().__init__()

3. Multi Class Handler
======================

The MultiClassHandler class inherits the BaseHandler Class.

.. warning::

    It does not inherit from ClassHandler. MultiClass handling is only possible
    in *last level classes* / *endpoint classes*.

It *indirectly overloads* the necessary methods from ClassHandler, to see the
differences take a closer look at *Internal Classes / Class Representation*
subsection.

The following shows how to implement a TestClass1 with standard *ClassHandling*
and TestClass2 with *MultiClassHandling*.

.. code-block:: python

    from microesb import microesb


    class TestClass1(microesb.ClassHandler):
        def __init__(self):
            super().__init__()

    class TestClass2(microesb.MultiClassHandler):
        def __init__(self):
            super().__init__()

See Example number 1 (:ref:`example-number1`) for an example
*service call metadata* (Host properties).

.. _implementation-classes:

4. Implementation Classes
=========================

Implementation classes are the classes defined in the implementation part.
They contain the programmed service logic.

.. note::

    Each *implementation class* **must** inherit either ClassHandler or MultiClassHandler,
    only *endpoint classes* **may** inherit MultiClassHandler.

4.1. Abstraction
****************

The ClassMapper class is responsible to hierarchical map / connect the desired
*implementation classes*.

After the ClassMapper has setup internal class instances, the ServiceMapper
class fills these class instance properties with values from the provided
*service call metadata*.

4.2. Inheritance
****************

An *implementation class* must inherit from either **microesb.ClassHandler** or
**microesb.MultiClassHandler**.

Also it **must** contain the class syntax `super().__init__()` in its constructor,
so that ClassMapper is able to instantiate correctly on processing.

4.3. Class Properties Model
***************************

The microesb`s propety model is a flat OOP based one.

Take two *implementation classes*, **Customer** as root class and **Domain**
as Customers child class.

Customer properities defined in *service properties* config are "Name" and
"CustomerID". Domain properties are "Name" and "Ending". Domain.Ending has a
defined default value of 'de'.

Both class instances are setup by *ClassMapper* in Pythons global domain space.

To illustrate it in a better way how the class instances members have been setup
after *ClassMapper* invocation, a slightly modified Python syntax has been used.

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

Take the example from 4.2. **Customer** is defined as root class and **Domain**
as Customers child class.

The method get_customer_dbdata() has been added as public Customer member, the
method do_something() as public member to Domain.

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

After calling Customer.get_customer_dbdata() Customer.CustomerID will be a valid
customer id.

Now printing self.parent_object.CustomerID inside Domain.do_something()
automagically will invoke BaseHandler.parent_object() method which returns the
self._SYSParentObject reference (due to @property decorator), so finally the
CustomerID property can be accessed.

4.5. Class Import
*****************

All *implementation classes* must be imported into the global python namespace.

.. code-block:: python

    from microesb import microesb

Importing the main microesb module will call `import esbconfig` (see following code
line 14).

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

The microesb`s standard installation will install an empty esbconfig.py in the
global Pythons distpackages or in the environment you are using.

.. warning::

    If you will not provide an esbconfig.py in your projects folder, the default
    installation one will be used.

The following **esbconfig.py** tells microesb importer to use file **service_classes.py**
and import *implementation classes* Class1, Class2 and Class3 into global namespace
so the classes are usable by ClassMapper and ServiceMapper internal processing.

.. code-block:: python

    import_classes = {
       'service_classes': [
          'Class1',
          'Class1',
          'Class3'
       ]
    }

.. note::

    The implementation classes python module also must be present inside project
    folder.

5. Class Mapper
===============

The ClassMapper class is responsible to hierarchical map / connect the desired
*implementation classes*.

The ClassMapper class must be invoked at initialization / before ServiceMapper.
It takes the following config dictionaries as input parameter.

- Class Reference Dictionary (see "Configuration / :ref:`class-reference-config`")
- Class Mapping Dictionary (see "Configuration / :ref:`class-mapping-config`")
- Service Properties Dictionary (see "Configuration / :ref:`service-properties-config`")

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

The ServiceMapper class maps / fills the existing class instances created by
ClassMapper with given *service call metadata*.

It needs the following config dictionaries as input parameter.

- ClassMapper reference
- Service Call Metadata Dictionary (see "Configuration / :ref:`service-call-metadata-config`")

.. code-block:: python

    service_metadata = { ... }

    res = microesb.ServiceMapper(
       class_mapper=class_mapper,
       service_data=service_metadata
    )
