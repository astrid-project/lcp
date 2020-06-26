Local Control Plane
===================

.. image:: https://img.shields.io/github/license/astrid-project/lcp
    :target: https://github.com/astrid-project/lcp/-/blob/master/LICENSE
    :alt: MIT License

.. image:: https://img.shields.io/github/languages/code-size/astrid-project/lcp?color=red&logo=github
    :target: https://github.com/astrid-project/lcp
    :alt: GitHub Code Size

.. image:: https://img.shields.io/github/repo-size/astrid-project/lcp?color=red&logo=github
    :target: https://github.com/astrid-project/lcp
    :alt: GitHub Repository Size

.. image:: https://img.shields.io/github/v/tag/astrid-project/lcp?label=release&logo=github
    :target: https://github.com/astrid-project/lcp/releases
    :alt: GitJHub Release

.. image:: https://img.shields.io/cii/summary/4096
    :target: https://bestpractices.coreinfrastructure.org/en/projects/4096
    :alt: CII Progress

.. image:: https://readthedocs.org/projects/lcp/badge/?version=latest
    :target: https://lcp.readthedocs.io
    :alt: Readthedocs

.. image:: https://pyup.io/repos/github/astrid-project/lcp/shield.svg
    :target: https://pyup.io/repos/github/astrid-project/lcp/
    :alt: PyUP

.. image:: https://pyup.io/repos/github/astrid-project/lcp/python-3-shield.svg
     :target: https://pyup.io/repos/github/astrid-project/lcp/
     :alt: Python 3


In each local agent, the control plane is responsible for programmability, i.e., changing the behaviour of the data plane at run-time.


Guide
-----

See the Swagger Schema (`|YAML| <api/swagger.yaml>`_, `|JSON| <api/swagger.json>`_) and the relative **documentation** (|REST|
endpoint ``/api/doc </api/doc>``) more details about the |REST| endpoints and relative formats and
requirements of request and response.


Installation
------------

1. Prerequisite

   - python (version >= 3.5)
   - pip (for python 3)

2. Clone the repository.

.. code-block:: console

  git clone https://gitlab.com/astrid-repositories/lcp.git
  cd lcp

3. Install the dependencies.

.. code-block:: console

  pip3 install -r requirements.txt


Configuration
-------------

The configurations are stored in the `config.ini <config.ini>`_ file.

+---------------------+-----------------+--------------------+-----------------------------------------------------------+
| Section             | Setting         | Default value      | Note                                                      |
+=====================+=================+====================+===========================================================+
| local-control-plane | host            | 0.0.0.0            | |IP| address to accept requests.                          |
|                     +-----------------+--------------------+-----------------------------------------------------------+
|                     | port            | 5000               | |TCP| Port of the |REST| Server.                          |
+---------------------+-----------------+--------------------+-----------------------------------------------------------+
| auth                | max-ttl         | 10min              | Maximum |TTL| of the authorization with the |CB|-Manager. |
+---------------------+-----------------+--------------------+-----------------------------------------------------------+
| polycube            | host            | localhost          | |IP| address to contact the polycube installation.        |
|                     +-----------------+--------------------+-----------------------------------------------------------+
|                     | port            | 9000               | Port address to contact the polycube installation.        |
|                     +-----------------+--------------------+-----------------------------------------------------------+
|                     | timeout         | 20s                | Timeout for the connection to polycube.                   |
+---------------------+-----------------+--------------------+-----------------------------------------------------------+
| dev                 | username        | elasticsearch:9200 | Username for |HTTP| authentication (for developer use).   |
|                     +-----------------+--------------------+-----------------------------------------------------------+
|                     | password         | 20s               | Password for |HTTP| authentication (for developer use).   |
+---------------------+-----------------+--------------------+-----------------------------------------------------------+


Usage
-----

Display help
^^^^^^^^^^^^

```bash
python3 main.py -h
```


.. include:: docs/glossary.rst


.. |API| replace:: :abbr:`APIs (Application Program Interface)`
.. |APIs| replace:: :abbr:`APIs (Application Program Interfaces)`
.. |ASTRID| replace:: :abbr:`ASTRID (AddreSsing ThReats for virtualIseD services)`
.. |CB| replace:: :abbr:`CB (Context Broker)`
.. |CII| replace:: :abbr:`CII (Core Infrastructure Initiative)`
.. |DB| replace:: :abbr:`DB (DataBase)`
.. |eBPF| replace:: :abbr:`eBPF (extended Berkeley Packet Filter)`
.. |HTTP| replace:: :abbr:`HTTP (HyperText Transfer Protocol)`
.. |IP| replace:: :abbr:`IP (Internet Protocol)`
.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |LCP| replace:: :abbr:`LCP (Local Control Plane)`
.. |MIT| replace:: :abbr:`MIT (Massachusetts Institute of Technology)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
.. |TCP| replace:: :abbr:`TCP (Transmission Control Protocol)`
.. |TTL| replace:: :abbr:`TTL (Time To Live)`
.. |YAML| replace:: :abbr:`YAML (YAML Ain't Markup Language )`
