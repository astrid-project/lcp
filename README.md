Local Control Plane
===================

[![MIT License](https://img.shields.io/github/license/astrid-project/lcp)](https://github.com/astrid-project/lcp/-/blob/master/LICENSE)

[![GitHub Code Size](https://img.shields.io/github/languages/code-size/astrid-project/lcp?color=red&logo=github)](https://github.com/astrid-project/lcp)

[![GitHub Repository Size](https://img.shields.io/github/repo-size/astrid-project/lcp?color=red&logo=github)](https://github.com/astrid-project/lcp)

[![GitJHub Release](https://img.shields.io/github/v/tag/astrid-project/lcp?label=release&logo=github)](https://github.com/astrid-project/lcp/releases)

[![CII Progress](https://img.shields.io/cii/summary/4096)](https://bestpractices.coreinfrastructure.org/en/projects/4096)

[![Readthedocs](https://readthedocs.org/projects/lcp/badge/?version=latest)](https://lcp.readthedocs.io)

[![PyUP](https://pyup.io/repos/github/astrid-project/lcp/shield.svg)](https://pyup.io/repos/github/astrid-project/lcp/)

In each local agent, the control plane is responsible for
programmability, i.e., changing the behaviour of the data plane at
run-time.

Guide
-----

See the Swagger Schema ([\|YAML\|](api/swagger.yaml),
[\|JSON\|](api/swagger.json)) and the relative **documentation**
(`REST (Representational State Transfer)`{.interpreted-text role="abbr"}
endpoint `/api/doc </api/doc>`) more details about the
`REST (Representational State Transfer)`{.interpreted-text role="abbr"}
endpoints and relative formats and requirements of request and response.

Installation
------------

1.  Prerequisite
    -   python (version \>= 3.5)
    -   pip (for python 3)
2.  Clone the repository.

``` {.sourceCode .console}
git clone https://gitlab.com/astrid-repositories/lcp.git
cd lcp
```

3.  Install the dependencies.

``` {.sourceCode .console}
pip3 install -r requirements.txt
```

Configuration
-------------

The configurations are stored in the [config.ini](config.ini) file.

+------------+---------+-----------+----------------------------------+
| Section    | Setting | Default   | Note                             |
|            |         | value     |                                  |
+============+=========+===========+==================================+
| local-cont | > host  | > 0.0.0.0 | > `IP (Internet Protocol)`{.inte |
| rol-plane  |         |           | rpreted-text                     |
|            | \-\-\-\ | \-\-\-\-\ | > role="abbr"} address to accept |
| :   -      | -\-\-\- | -\-\-\-\- | > requests.                      |
|            | \-\-\-\ | \-\-\-\-\ |                                  |
|            | -\-\-\- | -\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|            | \-\--+  | \--+      | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|            |         |           | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|            | :   por | :   5000  | \-\-\-\-\-\-\-\-\-\--+           |
|            | t       |           |                                  |
|            |         |           | :   `TCP (Transmission Control P |
|            |         |           | rotocol)`{.interpreted-text      |
|            |         |           |     role="abbr"} Port of the     |
|            |         |           |     `REST (Representational Stat |
|            |         |           | e Transfer)`{.interpreted-text   |
|            |         |           |     role="abbr"} Server.         |
+------------+---------+-----------+----------------------------------+
| auth       | max-ttl | 10min     | Maximum                          |
|            |         |           | `TTL (Time To Live)`{.interprete |
|            |         |           | d-text                           |
|            |         |           | role="abbr"} of the              |
|            |         |           | authorization with the           |
|            |         |           | `CB (Context Broker)`{.interpret |
|            |         |           | ed-text                          |
|            |         |           | role="abbr"}-Manager.            |
+------------+---------+-----------+----------------------------------+
| polycube   | > host  | > localho | > `IP (Internet Protocol)`{.inte |
|            |         | st        | rpreted-text                     |
| :   -   -  | \-\-\-\ |           | > role="abbr"} address to        |
|            | -\-\-\- | \-\-\-\-\ | > contact the polycube           |
|            | \-\-\-\ | -\-\-\-\- | > installation.                  |
|            | -\-\-\- | \-\-\-\-\ |                                  |
|            | \-\--+  | -\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|            |         | \--+      | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|            | :   por |           | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|            | t       | :   9000  | \-\-\-\-\-\-\-\-\-\--+           |
|            |         |           |                                  |
|            | \-\-\-\ | \-\-\-\-\ | :   Port address to contact the  |
|            | -\-\-\- | -\-\-\-\- |     polycube installation.       |
|            | \-\-\-\ | \-\-\-\-\ |                                  |
|            | -\-\-\- | -\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|            | \-\--+  | \--+      | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|            |         |           | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|            | :   tim | :   20s   | \-\-\-\-\-\-\-\-\-\--+           |
|            | eout    |           |                                  |
|            |         |           | :   Timeout for the connection   |
|            |         |           |     to polycube.                 |
+------------+---------+-----------+----------------------------------+
| dev        | > usern | > elastic | > Username for                   |
|            | ame     | search:92 | > `HTTP (HyperText Transfer Prot |
| :   -      |         | 00        | ocol)`{.interpreted-text         |
|            | \-\-\-\ |           | > role="abbr"} authentication    |
|            | -\-\-\- | \-\-\-\-\ | > (for developer use).           |
|            | \-\-\-\ | -\-\-\-\- |                                  |
|            | -\-\-\- | \-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|            | \-\--+  | -\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|            |         | \--+      | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|            | :   pas | \| 20s    | \-\-\-\-\-\-\-\-\-\--+           |
|            | sword   |           |                                  |
|            |         |           | :   Password for                 |
|            |         |           |     `HTTP (HyperText Transfer Pr |
|            |         |           | otocol)`{.interpreted-text       |
|            |         |           |     role="abbr"} authentication  |
|            |         |           |     (for developer use).         |
+------------+---------+-----------+----------------------------------+

Usage
-----

### Display help

`` `bash python3 main.py -h ``\`

::: {.glossary}

ACL

:   Access Control Lis

API

:   Application Program Interface

BA

:   Basic Authentication

BPF

:   Berkeley Packet Filter

CB

:   Context Broker

CRUD

:   Create - Read - Update - Delete

DB

:   Database

eBPF

:   extended BPF

ELK

:   Elastic - LogStash - Kibana

Exec\_Env

:   Execution Environment

gRPC

:   Google RPC

HOBA

:   HTTP Origin-Bound Authentication

HTTP

:   Hyper Text Transfer Protocol

ID

:   Identification

IP

:   Internet Protocol

JSON

:   Java Object Notation

LCP

:   Local Control Plane

LDAP

:   Lightweight Directory Access Protocol

RBAC

:   Role-Based Access Control

regex

:   regular expression

REST

:   Representational State Transfer

RFC

:   Request For Comments

RPC

:   Remote Procedure Call

SCM

:   Security Context Model

SLA

:   Service Level Agreements

SQL

:   Structured Query Language

TCP

:   Transmission Control Protocol

TTL

:   Time To Live

VNF

:   Virtual Network Function

YANG

:   Yet Another Next Generation

YAML

:   YAML Ain\'t Markup Language
:::
