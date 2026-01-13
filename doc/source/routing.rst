.. _routing:

=======
Routing
=======

The **microesb** module provides flexible routing capabilities to direct service calls to appropriate backend implementations. This enables data aggregation (esb terminology calls this *routing*) to multiple data-sources like traditional relational databases, modern NoSQL platforms or similar.

1. Simple Routing
=================

Simple Routing allows **direct**, **unencapsulated** routing of service calls to user-defined functions. This approach is suitable for straightforward use cases where service calls map directly to backend operations without complex orchestration requirements.

**Encapsulated Routing** is a methodology to abstract / handle each single service entity as an external callable service, encapsulated inside a network-callable container (e.g. application server) with scaling and AAA functionality like using "Kubernetes / NginX / https" or "FalconAS / NLAMP".

The **Encapsulated Routing** concept is described under 2.x more detailed.

1.1. Overview
*************

Simple routing uses the ``ServiceRouter`` class to dynamically invoke functions defined in a ``user_routing.py`` module. Each routing function receives metadata from the service call and is able to return user modified results (as any type) of the backend operation.

1.2. Implementation
*******************

To implement simple routing, create a ``user_routing.py`` module in your project with functions that match the routing identifiers used in your service calls (see next chapter).

Example from ``/example/02-pki-management/user_routing.py``:

.. literalinclude:: ../../example/02-pki-management/user_routing.py
    :linenos:

1.3. Service Calls
******************

A service call must be placed inside the *service implementation*. The micro-esb's ServiceRouter class places a reference there (self._ServiceRouter), so it is easily callable like this:

``self._ServiceRouter.send('MethodId', metadata=metadata)`.

A good approach is to pass metadata as a dictionary type into the routing function (JSON serializable) and also expect a dictionary type as result (JSON serializable) to be conform to modern software development practices.

1.4. Common Use Cases
*********************

Simple routing is suitable for example:

- to aggregate data from internal systems (centralized DB with NoSQL data sources)
- to route / propagate service calls (e.g. certificate generation) to network-attached sub-systems

> [!WARNING]
> Authenticaton, Accouting and Load-Balancing has to be implemented by the user itself.

1.5. Error Handling / Logging
*****************************

The ``ServiceRouter`` class provides no error handling nor logging, the user is responsible implementing error / exception handling / logging by himself.

2. Encapsulated Routing
=======================

**Encapsulated Routing** is a mechanism to host ESB API services securely inside an network-accesible entity which provides the following:

- Load Balancing / Scaling
- AAA (Authentication, Authorization, Accounting)
- Service (API) Registration / Versioning
- Service (API) Discovery
- Service (API) Documentation
- Service Security / PKI Abstraction

Detailed documentation (including examples) starting from release version 1.3 upwards.

3. Operating Modes
==================

There are **no** strict configurable modes, the micro-esb's concept is to be extraordinary flexible in class abstraction / modeling from the users point of view; the *implementation mode* results from the users program code.

Nevertheless between two different **logical** modes can be distinguished:

- Native Routing Mode
- Non Native Routing Mode

**Native Routing** is the concept of decapsulate any service *calculations* (CPU) to external entities / application server; the ESB's service_implementation exclusively routes data to external services and **does not** process data internally which strongly enhances security.

**Non Native Routing** does not encapsulate data calls so data fetching is directly executed inside the ESB's service_implementation (e.g. direct MongoDB driver). This concept should not be adapted on high security requirements / non-reverse-proxied access.
