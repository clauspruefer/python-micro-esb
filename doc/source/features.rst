.. features

========
Features
========

1. Clean OOP Abstraction / Models
=================================

The framework features a clean Object-Oriented Programming (OOP) abstraction, including comprehensive database and exception handling support.

- Clean hierarchical implementation code
- Clean hierarchical service call metadata

**Example Implementation Code:**

.. literalinclude:: ../../example/02-pki-management/service_implementation.py
    :linenos:

2. Structured Service Call Metadata
===================================

The service call metadata is well-structured, as demonstrated in the following example:

.. code-block:: python

    call_JSON = {
        'SYSServiceID': 'generateCertClient',
        'data': [
            {
                'CertClient': {
                    'id': 'test-client1',
                    'CertCA': {
                        'id': 'test-ca1'
                    },
                    'CertServer': {
                        'id': 'test-server1'
                    },
                    'Smartcard': {
                        'label': 'smartcard_customer1',
                        'user_pin': 'pin2',
                        'SmartcardContainer': {
                            'label': 'testserver1_client1_keypair'
                        }
                    },
                    'country': 'DE',
                    'state': 'Berlin',
                    'locality': 'Berlin',
                    'org': 'WEBcodeX',
                    'org_unit': 'Security',
                    'common_name': 'testclient1@domain.com',
                    'email': 'pki@webcodex.de',
                    'valid_days': 365
                }
            }
        ]
    }

For the full example, see :ref:`example-number2`.

3. Multi-Object Abstraction
===========================

Process multiple hierarchical input metadata elements simultaneously.

**Example Service Call Metadata:**

.. literalinclude:: ../../example/01-hosting-use-case/service_call_metadata.py
    :linenos:

For the full example, see :ref:`example-number1`.

4. Structured Service Property Definition
=========================================

Define structured service call properties easily and efficiently.

**Example Service Property Definition:**

.. literalinclude:: ../../example/02-pki-management/service_properties.py
    :linenos:

For the full example, see :ref:`example-number2`.

5. Planned Features
====================

Planned for upcoming releases:

- Service Registry / API Server
- Service Registry / YANG Model Export
- Service Registry / Web Interface
- Service API / Auto Documentation
- Extended "Encapsulated" Service Routing
- Mincepy Integration / Metadata Mapping
