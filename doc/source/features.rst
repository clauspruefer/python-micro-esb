.. features

========
Features
========

1. Clean OOP Abstraction / Models
=================================

Very clean OOP object abstraction, including database and exception handling.

- Clean hierarchical Implementation Code
- Clean hierarchical Service Call Metadata

Example Implementation Code.

.. literalinclude:: ../../example/02-pki-management/service_implementation.py
    :linenos:

Example Service Call Metadata.

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

Full example see :ref:`example-number2`.

2. Multi Object Abstraction
===========================

Process multiple hierarchical input metadata elements at once.

.. literalinclude:: ../../example/01-hosting-use-case/service_call_metadata.py
    :linenos:

Full example see :ref:`example-number1`.

3. Structured Service Call Metadata
===================================

Define structured service call properties.

.. literalinclude:: ../../example/02-pki-management/service_properties.py
    :linenos:

Full example see :ref:`example-number2`.

4. Planned Features
===================

- Service Registry
- Service Registry Management
- Service Based AAA (HSM / Smartcard)
- Automatic Service Interface Documentation Generation
- x0 JavaScript Framework Integration
