.. design

======
Design
======

1. Overview
===========

The following diagram shows the *Base Layout / Model* of a scalable **ESB Infrastructure**.

- Loadbalancing Layer (1)
- Transport Layer Security Layer (1)
- AAA / Authentication, Authorization, Accounting Layer (2)
- Service Control Plane / Provisioning Layer (3)
- Service Mapping / (Python) OOP Abstraction Layer (4)

.. image:: images/microesb-overview.png
  :alt: Image - Micro-ESB Overview

.. note::
    The **microesb** module focuses on the "Service Mapping / Abstraction Layer" (4).

.. note::
    The "Loadbalancing Layer" and the "Transport Layer Security Layer" easily can be adapted
    using a Kubernetes Cluster / Ingress-nginX (see "Example #2").

2. Centralized Service Management
=================================

The larger the IT infrastructure, the more important it is to build a generic, centralized
Service Oriented Architecture.

.. image:: images/microesb-centralized-service-mm.png
  :alt: Image - Micro-ESB Centralized Service Management

2.1. Implementation Workflow
****************************

The common workflow in a CI driven, recurring, agile Devlopment Process.

1. Build
2. Test
3. Deploy
4. Maintain

2.2. Standards / Generic Aproach
********************************

The better standards / infrastructural templates are organized, the more developers can
focus on the Development Process. Especially in big Development Environments / Teams.

2.3. External Service Integration
*********************************

...

3. Service Mapping
==================

Service mapping between hierarchical JSON graph data and internal python classes. This is exactly
what the **microesb** python module is capable of.

.. image:: images/microesb-service-mapping.png
  :alt: Image - Micro-ESB Service Mapping / Abstraction Layer

.. note::
    A detailed example including transactional database access see "Example #1".

4. Platform As A Service
========================

...
