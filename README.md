# Local Control Plane

[![License](https://img.shields.io/github/license/astrid-project/lcp)](https://github.com/astrid-project/lcp/blob/master/LICENSE)
[![Code size](https://img.shields.io/github/languages/code-size/astrid-project/lcp?color=red&logo=github)](https://github.com/astrid-project/lcp)
[![Repository Size](https://img.shields.io/github/repo-size/astrid-project/lcp?color=red&logo=github)](https://github.com/astrid-project/lcp)
[![Release](https://img.shields.io/github/v/tag/astrid-project/lcp?label=release&logo=github)](https://github.com/astrid-project/lcp/releases)
[![Docker image](https://img.shields.io/docker/image-size/astridproject/lcp?label=image&logo=docker)](https://hub.docker.com/repository/docker/astridproject/lcp)
[![Docs](https://readthedocs.org/projects/astrid-lcp/badge/?version=latest)](https://astrid-lcp.readthedocs.io)

In each local agent, the control plane is responsible for programmability, i.e., changing the behaviour of the data plane at run-time.

---

- [Local Control Plane](#local-control-plane)
  - [Guide](#guide)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [Display help](#display-help)
    - [Execute](#execute)
  - [Extra](#extra)

---

## Guide

See the [Swagger Schema](swagger/schema.yaml) for more details about the REST endpoints and relative formats and requirements of request and response.

## Installation

1. Prerequisite

   - python3
   - pip3

2. Clone the repository.

   ```bash
   git clone https://gitlab.com/astrid-repositories/lcp.git
   cd lcp
   ```

3. Install the dependencies (optional).

   ```bash
   pip3 install -r requirements.txt
   ```

## Configuration

The configurations are stored in the [config.ini](config.ini) file.

Section             | Setting   | Default value   | Note
--------------------|-----------|-----------------|---------------------------
local-control-plane | host      | 0.0.0.0         | IP address to accept requests.
local-control-plane | port      | 4000            | TCP port to accept requests.
auth                | max-ttl   | 10min           | Maximum TTL of the authorization with the CB-Manager.
polycube            | host      | localhost       | IP address to contact the polycube installation.
polycube            | port      | 9000            | Port address to contact the polycube installation.
polycube            | timeout   | 20s             | Timeout for the connection to polycube.
dev                 | username  | lcp             | Username for HTTP authentication (for developer use).
dev                 | password  |                 | Password for HTTP authentication (for developer use).

## Usage

### Display help

```bash
python3 main.py -h
```

### Execute

```bash
python3 main.py
```

## Extra

See the **Issues** for *features* in development.
