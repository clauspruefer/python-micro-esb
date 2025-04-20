.. intro

==========================
Intro / Module Description
==========================

The **microesb** Python module provides the foundational features to build a centralized,
structured Enterprise Service Bus (ESB) / SOA architecture.

Its primary feature is a clean, OOP-based **Service Model to Python Class Mapping**.

A Docker example container can be downloaded here:
`microesb-examples-latest.tar <https://docker.webcodex.de/microesb-examples-latest.tar>`_.

1. Basic System Installation
============================

.. code-block:: bash

    # install the module system-wide
    pip3 install --break-system-packages microesb

2. Virtual Environment Installation
===================================

.. code-block:: bash

    # install the module in a virtual environment
    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install --upgrade pip
    pip3 install microesb

3. Dependencies
===============

Using the **microesb** module generally does not require the **psycopg2** PostgreSQL
Python module.

.. warning::
    Running example code requires **psycopg2**.

.. code-block:: bash

    # install psycopg2
    apt-get install python3-psycopg2

4. Build Dependencies
=====================

On current Debian 12 / Ubuntu 22.04.3 or 24.04.1, install the following additional packages
(for documentation rendering and testing purposes).

.. code-block:: bash

    # install base packages
    apt-get install python3-pip python3-sphinx python3-sphinx-rtd-theme

    # install pytest for running unit and integration tests
    apt-get install python3-pytest python3-pytest-pep8

5. Build Local Package
======================

To build and install the local package (also for testing), follow these steps.

.. code-block:: bash

    # build source distribution
    python3 setup.py sdist

    # install system-wide
    pip3 install --break-system-packages ./dist/microesb-1.0rc1.tar.gz

6. Tests
========

To run all tests (unit and integration) after the system-wide package installation:

.. code-block:: bash

    # run pytest
    cd ./ && pytest

7. Current Features
===================

- JSON Service Metadata to Python Internal Class / Object Mapping

8. Planned Features
====================

- Database Abstraction on "top" of the Object Mapping Model
