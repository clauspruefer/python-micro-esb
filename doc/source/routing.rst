.. _routing:

=======
Routing
=======

The **microesb** module provides flexible routing capabilities to direct service calls to appropriate backend implementations. This enables data aggregation (in ESB terminology, this is referred to as *routing*) from multiple data sources, including traditional relational databases, modern NoSQL platforms, and similar systems.

1. Simple Routing
=================

Simple Routing allows **direct**, **unencapsulated** routing of service calls to user-defined functions. This approach is suitable for straightforward use cases where service calls map directly to backend operations without complex orchestration requirements.

**Encapsulated Routing** is a methodology designed to abstract and handle each service entity as an externally callable service, encapsulated within a network-accessible container (e.g., application server) with scaling and AAA (Authentication, Authorization, Accounting) functionality, such as "Kubernetes / Nginx / HTTPS" or "FalconAS / NLAMP".

The **Encapsulated Routing** concept is described in greater detail in section 2.

1.1. Overview
*************

Simple routing uses the ``ServiceRouter`` class to dynamically invoke functions defined in a ``user_routing.py`` module. Each routing function receives metadata from the service call and can return user-modified results (of any type) representing the outcome of the backend operation.

1.2. Implementation
*******************

To implement simple routing, create a ``user_routing.py`` module in your project with functions that match the routing identifiers used in your service calls (see next chapter).

Example from ``/example/02-pki-management/user_routing.py``:

.. literalinclude:: ../../example/02-pki-management/user_routing.py
    :linenos:

1.3. Service Calls
******************

A service call must be placed within the *service implementation*. The micro-esb's ServiceRouter class provides a reference there (self._ServiceRouter), making it easily callable as follows:

``self._ServiceRouter.send('MethodId', metadata=metadata)``.

A recommended approach is to pass metadata as a dictionary type (JSON serializable) into the routing function and expect a dictionary type as a result (JSON serializable), conforming to modern software development best practices.

1.4. Common Use Cases
*********************

Simple routing is particularly suitable for:

- Aggregating data from internal systems (e.g., centralized databases with NoSQL data sources)
- Routing and propagating service calls (e.g., certificate generation) to network-attached subsystems

.. warning::
   Authentication, accounting, and load balancing must be implemented by the user.

1.5. Error Handling and Logging
*******************************

The ``ServiceRouter`` class does not provide built-in error handling or logging. Users are responsible for implementing their own error and exception handling, as well as logging mechanisms.

2. Encapsulated Routing
=======================

**Encapsulated Routing** is a mechanism for hosting ESB API services securely within a network-accessible entity that provides the following features:

- Load balancing and scaling
- AAA (Authentication, Authorization, Accounting)
- Service (API) registration and versioning
- Service (API) discovery
- Service (API) documentation
- Service security and PKI abstraction

Detailed documentation (including examples) will be available starting from release version 1.3.

3. Operating Modes
==================

There are **no** strictly configurable modes. The micro-esb framework is designed to be extraordinarily flexible in class abstraction and modeling from the user's perspective; the *implementation mode* results from the user's program code.

Nevertheless, two different **logical** modes can be distinguished:

- Native Routing Mode
- Non-Native Routing Mode

**Native Routing** is the concept of delegating all service *computations* (CPU-intensive operations) to external entities or application servers. The ESB's service_implementation exclusively routes data to external services and **does not** process data internally, thereby strongly enhancing security.

**Non-Native Routing** does not encapsulate data calls, so data fetching is executed directly within the ESB's service_implementation (e.g., direct MongoDB driver usage). This approach should not be adopted in environments with high security requirements or non-reverse-proxied access.
