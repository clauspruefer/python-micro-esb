.. examples

.. _examples-global:

========
Examples
========

.. _example-number1:

1. Hosting Use Case
===================

In this example number 1, assume our "virtual" company runs a
**Hosting Business**.

The companies customer data including a) Internet Domains and b) DNS Hostnames
should be manageable by different sub systems.

.. note::

    Example number 1 will only cover Local Service Mapping **without**
    *Python Application Server* / *Multi-Tier* abstraction.

.. note::

    In example number 4 we will dig a little deeper and include those aspects,
    even *Service Scaling* and *Load Balancing*.

1.1. Basic OOP Relations
************************

The hosting service offers the customer to buy (add, delete) domains and manage
the domains DNS host entries (add, update, delete).

.. code-block:: bash

    - Customer
      + Domain(s)
        + Hostname(s)

- Customer has 1:n relation to Domain
- Domain has 1:n relation to Host

1.2. Relations Diagram
**********************

.. image:: images/microesb-example1-object-relations.png
    :alt: image - microesb example1, relations
    :width: 694px

1.3. Encapsulation / Domain Data
********************************

It is a common design approach to encapsulate each logical segment into a
single, separated "flat" service endpoint.

1. Separated (parametrized) insertDomain
2. Separated (parametrized) updateDomain
3. Separated (parametrized) deleteDomain
4. Separated (parametrized) insertHost
5. Separated (parametrized) updatetHost
6. Separated (parametrized) deletetHost

Imagine this like a simple, parametrized function() call / "flat", non-hierachical.

1.4. Encapsulation The Better Way
*********************************

We could do this much easier, preserve (database) transactions and save a lot
of administrative / maintaining effort.

If we could already process structured hierachical metadata in the service input,
these endpoints would be reduced to the following.

1. Separated (hierachical metadata) insertUserDomain
2. Separated (hierachical metadata) updatetUserDomain
3. Separated (hierachical metadata) deleteUserDomain

.. note::

    Also the microesb`s service processing is able to handle multiple (list)
    user requests containing domain / host data in one single webservice call.

.. note::

    Example number 1 only covers 1. "insertUserDomain".

1.5. Example Call Meta-Data
***************************

The following example service call metadata will instruct the backend to do
the following tasks when using backend configuration from section
:ref:`backend-config` and code from section :ref:`python-implementation`.

1. Loop on User [ "testuser1" ]
2. Start database transaction
3. Get user id by user name
4. Insert Domain "testdomain1.com" if it does not exist
5. Insert Hostname (MX type) with value "mx01.mailserver.com" and priority 1
6. Insert Hostname (A type) with value "mx01.mailserver.com" and ttl 36000 seconds
7. Commit on success or rollback database transaction on failure

.. literalinclude:: ../../example/01-hosting-use-case/service_call_metadata.py
    :linenos:

1.6. Database Tables (PostgreSQL)
*********************************

The following database tables are used in this example.

- sys_core."user"
- sys_core."domain"
- sys_dns."dnsrecord"

The following SQL code is an excerpt (create tables) of the complete database creation
SQL script found in the example folder.

.. literalinclude:: ../../example/01-hosting-use-case/02-create-table.sql
    :linenos:

.. _backend-config:

1.7. Backend Config / Service Mapping
*************************************

The following dictionary data describes how to configure the **microesb`s**
backend to run this example.

1.7.1. Service Property Mapping
-------------------------------

.. literalinclude:: ../../example/01-hosting-use-case/service_properties.py
    :linenos:

1.7.2. Hierachical Class Reference
----------------------------------

.. literalinclude:: ../../example/01-hosting-use-case/class_reference.py
     :linenos:

1.7.3. Class Mapping
--------------------

.. literalinclude:: ../../example/01-hosting-use-case/class_mapping.py
    :linenos:

.. _python-implementation:

1.8. Python Implementation
**************************

The following code covers the implementation part.

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

To enable database transactions (disabled autocommit) inside main.py we have to
open the database connection inside main.py and pass it into the implementation
code.

Inside service_properties.py (line 10 - 15), we will define the property with id
'dbcon' which will be used to pass the database connection.

.. code-block:: python

    'dbcon': {
        'type': 'classref',
        'default': None,
        'required': True,
        'description': 'Database Connection Ref'
    }

Inside main.py (line 24) the service properties value can be set (decorated)
inside service call metadata dictionary.

.. code-block:: python

    service_metadata['data'][0]['User']['dbcon'] = dbcon

1.8.4. Execute Example
----------------------

Change to the example path and execute the main.py file.

.. code-block:: bash

    python3 ./main.py

1.8.5. Post Excecution
----------------------

After executing you will find the new created domain inside sys_core."domain"
table and two related host records inside sys_dns."dnsrecord" table.

.. note::

    There are no unique constraints which forbid multiple dns entry inserts,
    calling the script multiple times duplicates dns records.

.. _example-number2:

2. PKI Provisioning / Class Types
=================================

Example number 1 only covers a "plain" database model without local (e.g. bash)
or remote (webservice) invocations.

.. note::

    Example number 2 is a stripped-down excerpt from PKI management to show
    how *virtual class types* and *clean OOP model setup* are working.

2.1. CA Cert Relations
**********************

.. image:: images/microesb-example2-object-relations-ca.png
    :alt: image - microesb example2, relations ca
    :width: 694px

- CA == *Certificate Authority*
- HSM == *Hardware Security Module / Smartcard*

1. A CA is the root of a PKI (Public Key Infrastructure)
2. A functioning CA needs a *CA Certificate* signed by unique Private Key (on protected HSM or software generated)

If no Smartcard / SmartcardContainer reference will be given, the Private Key
used for the CA certificate will be generated by OpenSSL (marked **optional**
in the diagram).

.. note::

    A CA also can be setup in a hierarchical way (chain), this is called **Intermediate CA**.
    Our example only covers *root CA* processing without chaining.

2.2. Server Cert Relations
**************************

.. image:: images/microesb-example2-object-relations-server.png
    :alt: image - microesb example2, relations server
    :width: 694px

When a *Server Certificate* will be generated, a CA Certificate and its Private
Key are required to guarantee that the *Server Certifiate* has been issued by
the correct CA.

To run a TLS based server the *Server Certificate* (including *Public Key*), the
Server Certificates Private Key and the *CA Cert* or *CA Cert Chain* (if
Intermediate CA) is required.

.. note::

    A Certificates X.509 v3 Extension(s) (OIDs) define the exact Certificates
    usage (e.g. Email Encryption, Transport Layer Encryption or similar).

2.3. Client Cert Relations
**************************

.. image:: images/microesb-example2-object-relations-client.png
    :alt: image - microesb example2, relations client
    :width: 694px

To generate a *Client Certificate*, additionally to the CA Certificate and
its Private Key the relevant Server Certificate and its Private Key is
required.

2.4. Service Workflow
*********************

The implemented example Service Workflow provides Certificate Generation for
*CertCA*, *CertServer* and *CertClient* Certificates.

For all Certificate Types it will be checked, if a Smartcard reference has been
provided. If yes, the keypair will be generated on card, if not the Private Key
will be generated by openssl.

If a Smartcard is referenced inside *Service Call Metadata*, related data will
be selected from database.

Also after successful Certificate Generation, relevant data will be stored
inside database.

.. note::

    To emphasize the presentation of the workflow only dummy routines / methods
    and print() statements have been used for illustration.

2.5. Implementation
*******************

.. literalinclude:: ../../example/02-pki-management/service_implementation.py
    :linenos:

2.6. Clean OOP Model
********************

To get a clean OOP model inside the implementation class hierarchy, the following
design aspects have been selected.

.. note::

    *Virtual Class Types* require a Base Class iheriting microesb.ClassHandler
    and minimal 1 *Child Class* inheriting the *Base Class*.

.. code-block:: python

    class Cert(microesb.ClassHandler):

        __metaclass__ = abc.ABCMeta

        def __init__(self):
            super().__init__()

.. code-block:: python

    class CertCA(Cert):

        def __init__(self):
            self.type = 'ca'
            super().__init__()

2.6.1. Abstract Methods
-----------------------

The "Cert" base class provides 3 private abstract methods because the processing
logic differs for each *Certificate Type*.

- _load_ref_cert_data()
- _gen_openssl_cert()
- _insert_cert_db_data()

.. code-block:: python

    class CertCA(Cert):

    def _load_ref_cert_data(self):
        pass

.. code-block:: python

    class CertServer(Cert):

    def _load_ref_cert_data(self):
        self.CertCA._get_cert_dbdata_by_id()

.. code-block:: python

    class CertClient(Cert):

    def _load_ref_cert_data(self):
        self.CertCA._get_cert_dbdata_by_id()
        self.CertServer._get_cert_dbdata_by_id()

2.6.2. Generic Template Methods
-------------------------------

The following methods are generic template methods to be inherited to each
*Child Class*.

- _gen_openssl_privkey()
- _get_cert_dbdata_by_id()
- _hsm_gen_keypair()

2.7. Accessing Properties
*************************

The clean OOP model makes accessing hierarchical *Class Instance Properties* very
easy.

All *Virtual Imlementation Class Instances* are able to do the following to access
its own (self) Smartcard Containers Label.

.. code-block:: python

    self.Smartcard.SmartcardContainer.label

In *CertClient* and *CertServer* it is also possible to access the CertCA
Smartcard Properties (*Referenced Classes* in *Class Reference Config*) to fill
with data drom database inside _get_cert_dbdata_by_id().

.. code-block:: python

    self.CertCA.Smartcard.SmartcardContainer.label

2.8. Class Import
*****************

The *Class Import Config* **must** include all *Implementation Classes* except
the *Base Class(es)*.

.. literalinclude:: ../../example/02-pki-management/esbconfig.py
    :linenos:

2.9. Service Execution
**********************

Currently, the *Service Registry* feature is unimplemented. Excecution is only
possible as a single service foreach *Certificate Type*.

2.9.1. CertCA Type
------------------

.. literalinclude:: ../../example/02-pki-management/main-ca.py
    :linenos:

Output must look like this after executing.

.. code-block:: bash

    python3 ./main-ca.py

    Gen keypair on smartcard:smartcard_ca_card with keypair label:keypair_ca1
    Gen openssl cert type:ca.
    Insert cert data type:ca into db.

2.9.2. CertServer Type
----------------------

.. literalinclude:: ../../example/02-pki-management/main-server.py
    :linenos:

Output must look like this after executing.

.. code-block:: bash

    python3 ./main-server.py

    Get cert data from db. Type: ca.
    Smartcard container label:testserver1_keypair
    Gen keypair on smartcard:smartcard_customer1 with keypair label:testserver1_keypair
    Gen openssl cert type:server, rel to CA.
    Insert cert data type:server into db.

2.9.3. CertClient Type
----------------------

.. literalinclude:: ../../example/02-pki-management/main-client.py
    :linenos:

Output must look like this after executing.

.. code-block:: bash

    python3 ./main-client.py

    Get cert data from db. Type: ca.
    Get cert data from db. Type: server.
    Smartcard container label:testserver1_client1_keypair
    Gen keypair on smartcard:smartcard_customer1 with keypair label:testserver1_client1_keypair
    Gen openssl cert type:client, rel to cCA and cServer.
    Insert cert data type:client into db.

2.10. Class Reference
*********************

The root classes "CertCA", "CertServer" and "CertClient" must have property_ref
point to 'Cert' properties defined in *Service Properties Config*.

The following requirements must be met for successful referencing.

- *Class Reference* mapping (property_ref) always **must** map to *Base Class* (Cert)
- Base Class (Cert) **must** exist in *Implementation*
- Base Class (Cert) **must** be inherited by *Virtual Class(es)* (CertCA ...) in *Implementation*
- Properties inside *Service Property Config* **must** be defined for given *Base Class* (Cert)
- *Class Mapping Config* must include *Virtual Class(es)* (CertCA ...)
- *Virtual Class(es)* (CertCA ...) **must** be referenced in *Import Configuration*

The following *Class Reference Config* contains all three *Cert Types*
(CA, Server and Client).

.. literalinclude:: ../../example/02-pki-management/class_reference.py
    :linenos:

2.11. Class Mapping
*******************

The *Class Mapping Config*.

.. literalinclude:: ../../example/02-pki-management/class_mapping.py
    :linenos:

.. note::
    All *Virtual Class Types* classes always must reference themselves.
    Only *Alias Class Mapping* uses non-self-mapping (see :ref:`example-number3`).

2.12. Service Properties
************************

The *Service Property Config*.

.. literalinclude:: ../../example/02-pki-management/service_properties.py
    :linenos:

2.13. Service Call Metadata
***************************

The *Service Call Metadata* for all *Cert Types*.

.. literalinclude:: ../../example/02-pki-management/service_call_metadata.py
    :linenos:

.. _example-number3:

3. Alias Class Mapping
======================

Alias Class Mapping **must** be used if you want to setup multiple *Child Class
Instances*.

3.1. Requirements
*****************

The *Alias Definition* must exist in *Class Maping Config* and map to an existing
*Implementation Class*.

Children to classes defined inside *Class Reference Config* must map to the
*Alias Class(es)*.

The *Alias Class* **property_ref** property in *Class Reference Config* always
must reference an existing *Implementation Class*.

3.2. Example
************

.. code-block:: python

    config = {
        'class_mapping': {
            'Test': 'Test',
            'Test2Ref1': 'Test2',
            'Test2Ref2': 'Test2'
        },
        'class_reference': {
            'Test': {
                'property_ref': 'Test',
                'children': {
                    'Test2Ref1': {
                        'property_ref': 'Test2'
                    },
                    'Test2Ref1': {
                        'property_ref': 'Test2'
                    }
                }
            }
        }
    }

.. _example-number4:

4. SOA on Kubernetes
====================

Example including working docker container(s) / Kubernetes Minikube setup
on the way (right after FalconAS milestone "HTTP1/1 implementation" has been adapted).

See: https://github.com/WEBcodeX1/http-1.2.
