# Local Control Plane

In each local agent, the control plane is responsible for programmability, i.e., changing the behaviour of the data plane at run-time.

---

- [Local Control Plane](#local-control-plane)
  - [Guide](#guide)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Display help](#display-help)
    - [Execute](#execute)
  - [Extra](#extra)

---

## Guide

See the [Swagger Schema](api/swagger.yml, api/swagger.json) and the relative [documentation](REST endpoint: /api/doc) for more details about the REST endpoints and relative formats and requirements of request and response.

## Installation

1. Prerequisite

   - python3
   - pip3

2. Clone the repository.

   ```bash
   git clone https://gitlab.com/astrid-repositories/lcp.git
   cd lcp
   ```

3. Install the dependencies.

   ```bash
   pip3 install -r requirements.txt
   ```

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
