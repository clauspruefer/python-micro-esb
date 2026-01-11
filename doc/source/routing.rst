.. _routing:

=======
Routing
=======

The **microesb** module provides flexible routing capabilities to direct service calls to
appropriate backend implementations. This enables separation of concerns between service
orchestration and business logic implementation.

1. Simple Routing
=================

Simple Routing allows direct, unencapsulated routing of service calls to user-defined functions.
This approach is suitable for straightforward use cases where service calls map directly to
backend operations without complex orchestration requirements.

1.1. Overview
*************

Simple routing uses the ``ServiceRouter`` class to dynamically invoke functions defined in a
``user_routing.py`` module. Each routing function receives metadata from the service call and
returns the result of the backend operation.

1.2. Implementation
*******************

To implement simple routing, create a ``user_routing.py`` module in your project with functions
that match the routing identifiers used in your service calls.

Example from ``/example/02-pki-management/user_routing.py``:

.. literalinclude:: ../../example/02-pki-management/user_routing.py
    :linenos:

1.3. Usage Pattern
******************

The routing functions are invoked automatically by the framework when a service call specifies
a routing target. Each function receives the relevant metadata and can interact with databases,
external services, or other backend systems.

**Key characteristics:**

- Direct function mapping: Service routing IDs map to function names in ``user_routing.py``
- Flexible return values: Functions can return data structures that match service requirements
- Database integration: Common pattern for MongoDB, PostgreSQL, or other data stores
- Stateless operations: Each routing function operates independently

1.4. Common Use Cases
*********************

Simple routing is ideal for:

- Database CRUD operations (Create, Read, Update, Delete)
- External API integrations
- File system operations
- Cache management
- Message queue interactions

1.5. Error Handling
*******************

The ``ServiceRouter`` class provides basic error handling for missing routing targets. For
production deployments, implement appropriate error handling within your routing functions
to manage database connection failures, validation errors, and other exceptional conditions.

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
