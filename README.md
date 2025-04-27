# Python Micro-Enterprise-Service-Bus Module

![push main](https://github.com/clauspruefer/python-micro-esb/actions/workflows/pylint.yaml/badge.svg)
[![PyPI version](https://badge.fury.io/py/microesb.svg)](https://badge.fury.io/py/microesb)
[![codecov](https://codecov.io/gh/clauspruefer/python-xml-microparser/graph/badge.svg?token=KZBQACTCOO)](https://codecov.io/gh/clauspruefer/python-xml-microparser)

## 1. Abstract / Preface

*Enterprise Service Bus* is still a pretty vague term, first introduced in the Gartner Report of 2002.

It is essential for running a large SOA infrastructure.

## 2. Features

Our interpretation of what an ESB should consist of:

- Service Abstraction / Metadata Definition
- Centralized Service / API Registry containing clean XML, JSON Model
- Centralized Service AAA (Authentication / Authorization / Accounting)
- Internal Service XML / (Python) Class Mapping
- OOP Relational Database Mapper
- Service Model Documentation / API (Auto)-Generation

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

## 4. Platform As A Service (PaaS)

Building web applications on PaaS infrastructure also relies on a clean Service Abstraction Model.

> **Note**
> The Python **micro-esb** module will help.

## 5. Current Features

- Service Abstraction / Metadata Definition
- Internal Code (Python) Class / Service Properties Mapping
- Graph-Based / Recursive JSON Result Abstraction

### 5.1. In Progress

- OOP Relational Database Mapper
- Service Documentation (Auto)-Generation

## 6. Documentation / Examples

Documentation, including detailed examples, can be found either in the `./doc` directory or at:
[https://pythondocs.webcodex.de/micro-esb](https://pythondocs.webcodex.de/micro-esb)

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
