.. _routing:

=======
Routing
=======

The **microesb** module provides flexible routing capabilities to direct service calls to appropriate backend implementations. This enables data aggregation (routing) to multiple data-sources like traditional relational databases or modern NoSQL platforms.

1. Simple Routing
=================

Simple Routing allows **direct**, **unencapsulated** routing of service calls to user-defined functions. This approach is suitable for straightforward use cases where service calls map directly to backend operations without complex orchestration requirements.

**Encapsulated Routing** is a methodology to abstract / handle each single service entity as an external callable service, encapsulated inside a network-callable container (e.g. application server) with scaling and AAA functionality like using "Kubernetes / NginX / https" or "FalconAS / NLAMP".

1.1. Overview
*************

Simple routing uses the ``ServiceRouter`` class to dynamically invoke functions defined in a ``user_routing.py`` module. Each routing function receives metadata from the service call and returns the result of the backend operation.

1.2. Implementation
*******************

To implement simple routing, create a ``user_routing.py`` module in your project with functions that match the routing identifiers used in your service calls (see next chapter).

Example from ``/example/02-pki-management/user_routing.py``:

.. literalinclude:: ../../example/02-pki-management/user_routing.py
    :linenos:

1.3. Implementation
*******************

Simply insert

self._ServiceRouter.send(
'CertGetById', metadata=self.id)` inside the service_implementation.py class definitions.

1.4. Common Use Cases
*********************

Simple routing should be used for net-internal trusted operations / systems where no authentication security is required.

1.5. Error Handling
*******************

The ``ServiceRouter`` class provides no error handling, the user is responsible implementing error / exception handling by himself.

2. Encapsulated Routing
=======================

Encapsulated Routing provides a more sophisticated approach with service registry integration,
authentication, authorization, and load balancing capabilities.

.. note::

    Encapsulated Routing will be integrated in a future release and will include:
    
    - Service Registry integration for dynamic service discovery
    - Built-in Authentication and Authorization (AAA) mechanisms
    - Load balancing across multiple service instances
    - Service versioning and compatibility management
    - Centralized logging and monitoring
    - Circuit breaker patterns for fault tolerance

2.1. Planned Features
*********************

The encapsulated routing implementation will provide:

**Service Registry:**
  Centralized registry for service endpoint discovery and metadata management.

**AAA Integration:**
  Authentication, Authorization, and Accounting for secure service access control.

**Load Balancing:**
  Distribute service calls across multiple backend instances for scalability.

**Service Mesh:**
  Advanced service-to-service communication with retry logic, timeouts, and fallbacks.

2.2. Migration Path
*******************

Applications using Simple Routing will be able to migrate to Encapsulated Routing with minimal
code changes. The routing interface will remain backwards compatible while providing optional
advanced features through configuration.
