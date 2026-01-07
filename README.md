# Python Micro-Enterprise-Service-Bus Module

![push main](https://github.com/clauspruefer/python-micro-esb/actions/workflows/pylint.yaml/badge.svg)
[![PyPI version](https://badge.fury.io/py/microesb.svg)](https://badge.fury.io/py/microesb)
[![codecov](https://codecov.io/gh/clauspruefer/python-micro-esb/graph/badge.svg?token=03VPTCG8YI)](https://codecov.io/gh/clauspruefer/python-micro-esb)

## 1. Abstract / Preface

*Enterprise Service Bus* is still a pretty vague term, first introduced in the Gartner Report of 2002.

It is essential for maintaining large SOA infrastructures.

## 2. Features

Our interpretation of what an ESB should consist of:

- ✅ Service Abstraction / Declarative Metadata Modeling
- ✅ Centralized Service / API Registry providing clean XML, JSON Models
- ✅ Centralized Service AAA (Authentication / Authorization / Accounting)
- ✅ Service Metadata XML, JSON / Internal (Python) Class Abstraction
- ✅ Relational Backend OOP / ORM / ODM Mapper
- ✅ Service Model Documentation / API (Auto)-Generation

## 3. Install

```bash
# setup virtual-env
python3 -m venv .micro-esb

# activate virtual-env
source .micro-esb/bin/activate

# upgrade pip
python3 -m pip install --upgrade pip

# install microesb module
pip3 install microesb

# install dependencies
pip3 install pytest pytest-pep8
```

## 4. Platform As A Service (PaaS) / Microservices

The NoSQL conform JSON abstraction / data transformation capabilities make the micro-esb
suitable for modern, scalable Next-Level applications.

## 5. Current Features

- ✅ Service Abstraction / Metadata Definition
- ✅ Internal Code (Python) Class / Service Properties Mapping
- ✅ Graph-Based / Recursive JSON Result Abstraction
- ✅ OOP Relational ODM Mapper / MongoDB Integration

### 5.1. In Progress

- :hourglass: Service Documentation (Auto)-Generation
- :hourglass: Service Registry / Encapsulated Service Routing
- :hourglass: YANG Model Export / Transformation
- :hourglass: Web-Interface / Dashboard

## 6. Documentation / Examples

Documentation, including detailed examples, can be found either in the `./doc` directory or at:
[https://pythondocs.webcodex.de/micro-esb](https://pythondocs.webcodex.de/micro-esb)

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
