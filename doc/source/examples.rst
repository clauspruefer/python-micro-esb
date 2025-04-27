.. examples

.. _examples-global:

========
Examples
========

.. _example-number1:

1. Hosting Use Case
===================

In this example, assume our "virtual" company runs a **Hosting Business**.

The company's customer data, including a) Internet Domains and b) DNS Hostnames, should be manageable by different subsystems.

.. note::

    Example number 1 will only cover Local Service Mapping **without**
    *Python Application Server* / *Multi-Tier* abstraction.

.. note::

    In example number 4, we will explore these aspects further, including *Service Scaling* and *Load Balancing*.

1.1. Basic OOP Relations
*************************

The hosting service allows customers to buy (add, delete) domains and manage the domains' DNS host entries (add, update, delete).

.. code-block:: bash

    - Customer
      + Domain(s)
        + Hostname(s)

- Customer has a 1:n relation to Domain.
- Domain has a 1:n relation to Host.

1.2. Relations Diagram
**********************

.. image:: images/microesb-example1-object-relations.png
    :alt: image - microesb example1, relations
    :width: 694px

1.3. Encapsulation / Domain Data
*********************************

A common design approach is to encapsulate each logical segment into a single, separate "flat" service endpoint.

1. Separated (parametrized) `insertDomain`
2. Separated (parametrized) `updateDomain`
3. Separated (parametrized) `deleteDomain`
4. Separated (parametrized) `insertHost`
5. Separated (parametrized) `updateHost`
6. Separated (parametrized) `deleteHost`

Think of this as simple, parametrized function calls—"flat," non-hierarchical.

1.4. Encapsulation: The Better Way
**********************************

We can simplify this process, preserve (database) transactions, and reduce administrative overhead.

By processing structured hierarchical metadata in the service input, these endpoints can be reduced to:

1. Separated (hierarchical metadata) `insertUserDomain`
2. Separated (hierarchical metadata) `updateUserDomain`
3. Separated (hierarchical metadata) `deleteUserDomain`

.. note::

    The microESB service processing can handle multiple (list-based) user requests containing domain/host data in a single web service call.

.. note::

    Example number 1 only covers `insertUserDomain`.

1.5. Example Call Metadata
***************************

This example service call metadata instructs the backend to perform the following tasks using the configuration in section :ref:`backend-config` and code from section :ref:`python-implementation`:

1. Loop on User ["testuser1"].
2. Start a database transaction.
3. Get the user ID by username.
4. Insert the domain "testdomain1.com" if it does not exist.
5. Insert a Hostname (MX type) with value "mx01.mailserver.com" and priority 1.
6. Insert a Hostname (A type) with value "mx01.mailserver.com" and TTL of 36,000 seconds.
7. Commit on success or rollback the database transaction on failure.

.. literalinclude:: ../../example/01-hosting-use-case/service_call_metadata.py
    :linenos:

1.6. Database Tables (PostgreSQL)
*********************************

The following database tables are used in this example:

- `sys_core."user"`
- `sys_core."domain"`
- `sys_dns."dnsrecord"`

Below is an excerpt of the SQL script for creating these tables:

.. literalinclude:: ../../example/01-hosting-use-case/02-create-table.sql
    :linenos:

.. _backend-config:

1.7. Backend Config / Service Mapping
*************************************

The following dictionary describes how to configure the **microESB's** backend to run this example.

1.7.1. Service Property Mapping
-------------------------------

.. literalinclude:: ../../example/01-hosting-use-case/service_properties.py
    :linenos:

1.7.2. Hierarchical Class Reference
-----------------------------------

.. literalinclude:: ../../example/01-hosting-use-case/class_reference.py
    :linenos:

1.7.3. Class Mapping
--------------------

.. literalinclude:: ../../example/01-hosting-use-case/class_mapping.py
    :linenos:

.. _python-implementation:

1.8. Python Implementation
**************************

The following Python code demonstrates the implementation.

1.8.1. Class Definition
-----------------------

.. literalinclude:: ../../example/01-hosting-use-case/service_implementation.py
    :linenos:

1.8.2. Main / Service Call
--------------------------

.. literalinclude:: ../../example/01-hosting-use-case/main.py
    :linenos:

1.8.3. Passing Parameters
-------------------------

To enable database transactions (disabled autocommit), open the database connection in `main.py` and pass it into the implementation code.

In `service_properties.py` (lines 10–15), define the property with ID `dbcon` to pass the database connection.

.. code-block:: python

    'dbcon': {
        'type': 'classref',
        'default': None,
        'required': True,
        'description': 'Database Connection Ref'
    }

In `main.py` (line 24), set the `dbcon` value in the service call metadata dictionary.

.. code-block:: python

    service_metadata['data'][0]['User']['dbcon'] = dbcon

1.8.4. Execute Example
----------------------

Navigate to the example directory and execute the `main.py` file.

.. code-block:: bash

    python3 ./main.py

1.8.5. Post-Execution
---------------------

After execution, the newly created domain will be in the `sys_core."domain"` table, with two related host records in the `sys_dns."dnsrecord"` table.

.. note::

    There are no unique constraints preventing duplicate DNS entries. Running the script multiple times will duplicate records.

---

This is a partial improvement and correction for the `examples.rst` file. Would you like me to continue with other sections, or focus on specific areas? Let me know!
