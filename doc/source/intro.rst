.. intro

==========================
Intro / Module Description
==========================

The **microesb** Python Module provides basic features to build a centralized, structured
Enterprise Service BUS / SOA architecture.

.. note::
    The **microesb** module helps building a clean OOP based Service Model to Python Class
    Mapping, see details at Examples subsection.

1. Basic Install
================

.. code-block:: bash

    pip3 install microesb

2. Dependencies
===============

Using the microesb module in general does not require **psycopg2** PostgreSQL Python Module.

.. warning::
    Running example code does!

.. code-block:: bash

    # install psycopg2
    apt-get install python3-psycopg2

3. Build Dependencies
=====================

On current Debian 12 / Ubuntu 22.04.3, 24.04.1 install the following additional packages (Documentation Rendering & Testing).

.. code-block:: bash

    # install base packages
    apt-get install python3-pip python3-sphinx python3-sphinx-rtd-theme

    # install pytest for running unit and integration tests
    apt-get install python3-pytest python3-pytest-pep8

4. Tests
========

To run all tests (unit and integration) after pip package installation.

.. code-block:: bash

    # run pytest
    cd ./ && pytest

5. Current Features
===================

- JSON Service Metadata to Python Internal Class / Object Mapping

6. Planned Features
===================

- Database Abstraction on "top" of Service Model
