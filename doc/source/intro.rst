.. intro

==========================
Intro / Module Description
==========================

The **microesb** Python Module provides basic features to build a centralized,
structured Enterprise Service BUS / SOA architecture.

Its main feature is a clean OOP based **Service Model to Python Class Mapping**.

Docker example container can be downloaded here:
https://docker.webcodex.de/microesb-examples-latest.tar.

1. Basic System Install
=======================

.. code-block:: bash

    # install system wide package
    pip3 install --break-system-packages microesb

2. Virtual Environment Install
==============================

.. code-block:: bash

    # install into virtual environment
    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install --upgrade pip
    pip3 install microesb

3. Dependencies
===============

Using the **microesb** module in general does not require **psycopg2** PostgreSQL
Python Module.

.. warning::
    Running example code does!

.. code-block:: bash

    # install psycopg2
    apt-get install python3-psycopg2

4. Build Dependencies
=====================

On current Debian 12 / Ubuntu 22.04.3, 24.04.1 install the following additional packages (Documentation Rendering & Testing).

.. code-block:: bash

    # install base packages
    apt-get install python3-pip python3-sphinx python3-sphinx-rtd-theme

    # install pytest for running unit and integration tests
    apt-get install python3-pytest python3-pytest-pep8

5. Build Local Package
======================

To build and install local package (also for testing), do the following.

.. code-block:: bash

    # build source distribution
    python3 setup.py sdist

    # install systemwide
    pip3 install --break-system-packages ./dist/microesb-1.0rc1.tar.gz

6. Tests
========

To run all tests (unit and integration) after pip systemwide package installation.

.. code-block:: bash

    # run pytest
    cd ./ && pytest

7. Current Features
===================

- JSON Service Metadata to Python Internal Class / Object Mapping

8. Planned Features
===================

- Database Abstraction on "top" of Object Mapping Model
