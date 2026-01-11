.. design

======
Design
======

1. Overview
===========

The following diagram illustrates the *Base Layout / Model* of a **scalable SOA / ESB Infrastructure**:

- Load Balancing Layer (1)
- Transport Layer Security Layer (1)
- AAA (Authentication, Authorization, Accounting) Layer (2)
- Service Control Plane / Provisioning Layer (3)
- Service Mapping / (Python) OOP Abstraction Layer (4)

.. image:: images/microesb-overview.png
   :alt: image - microesb overview

.. note::

    The **microesb** module focuses on the "Service Mapping / Abstraction Layer" (4).

2. Centralized Service Management
=================================

As IT infrastructures grow larger, it becomes increasingly important to establish a generic, centralized Service-Oriented Architecture (SOA).

.. image:: images/microesb-centralized-service-mm.png
   :alt: image - microesb centralized service management

2.1. Implementation Workflow
*****************************

The typical workflow in a CI-driven, iterative, and agile development process is as follows:

1. Build Infrastructure
2. Build Application
3. Test
4. Deploy
5. Maintain

2.2. Standards / Generic Approach
**********************************

The goal should be to minimize the effort required for point 1 (infrastructure) and the resulting periodic recurring costs.

The better *Standards / Infrastructure Templates* are organized, the more developers can focus on the *Development Process*. In large, agile development teams, it is crucial to adapt the IP infrastructure to constantly changing needs without unnecessary (and sometimes bureaucratic) effort.

A well-designed, documented, automatically updated, centralized, and generic **Service Registry** component within the SOA can significantly reduce complexity and help developers avoid many challenges.

.. note::

    Achieving this requires substantial RFC / standardization work.

2.3. External Service Integration
*********************************

It is also important to consider the numerous external (rented) services that need to be managed at various levels within the organization, such as:

- Metrics / Statistics
- Authentication
- Monitoring

.. note::

    *Wrapping* these external services into a centralized SOA could also be a beneficial approach.

3. Service Mapping
==================

The primary focus of the Python **microesb** module is to map a clean JSON metadata service schema to internal OOP-based Python class instances and methods.

.. image:: images/microesb-service-mapping.png
   :alt: image - microesb service mapping / abstraction layer

.. note::

    For a detailed example that includes transactional database access, refer to Example 1.

4. Platform As A Service
========================

In summary, the points outlined above represent the **basic requirements** for running a Platform as a Service (PaaS) infrastructure **efficiently**.
