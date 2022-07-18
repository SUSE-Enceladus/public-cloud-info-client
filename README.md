[![Build Status](https://travis-ci.com/SUSE-Enceladus/public-cloud-info-client.svg?branch=master)](https://travis-ci.com/SUSE-Enceladus/public-cloud-info-client)

# Introduction

pint (Public Cloud INformation Tracker) is a command line client to access
the REST API provided by the SUSE Public Cloud Information Service. The
information service provides data about the images SUSE publishes in various
public cloud frameworks (Amazon, Google, Microsoft) as well as the
servers that make up the SUSE maintained and operated update infrastructure
in those frameworks.

## Quick Start

There are various ways to install the Pint Client:

### Install On openSUSE systems 

```bash
  # Add the relevant repo if not enabled
  $ sudo zypper addrepo https://build.opensuse.org/project/show/Cloud:Tools <alias>  

  $ sudo zypper in python3-susepubliccloudinfo
```

### Install on SLE systems

```bash
  # Activate the sle-module-public-cloud if not activated
  # On a SLE system already registerd with SCC, to get the cmd to activate, run
  $ sudo SUSEConnect --list-extension

  # Once Public Cloud Module is activated, execute
  $ sudo zypper in python3-susepubliccloudinfo
```

### Install using pip on non-SUSE distros, e.g. Debian/Ubuntu or RHEL/CentOS. 

```bash   
  # Clone the repo
  $ git clone https://github.com/SUSE-Enceladus/public-cloud-info-client
  $ cd public-cloud-info-client

  # create the virtual environment.
  $ virtualenv pint_venv --python=python3
  
  # activate the virtual environment for interactive bash session 
  $ source pint_venv/bin/activate

  # install with pip
  $ pip install susepubliccloudinfo

  # Show help on various options
  $ pint -h | --help
```

### Install from Source

```bash
  # Clone the repo
  $ git clone https://github.com/SUSE-Enceladus/public-cloud-info-client
  $ cd public-cloud-info-client

  # create the virtual environment.
  $ virtualenv dev_venv --python=python3

  # activate the virtual environment for interactive bash session
  $ source dev_venv/bin/activate

  # There is 2 ways you can install
    1. Install latest sources in developer mode
       $ pip install -e .[dev]

    2. Install latest version normally
       $ pip install .[dev]

  # Show help on various options
  $ pint -h | --help
```

## Running Unit Tests

```bash
  # Clone the repo
  $ git clone https://github.com/SUSE-Enceladus/public-cloud-info-client
  $ cd public-cloud-info-client

  # create the Python 3.6  virtual environment.
  $ virtualenv test_venv --python=python3

  # activate the virtual environment for interactive bash session
  $ source test_venv/bin/activate

  # Install dependencies 
  $ pip install -e .[dev] 

  # Run Unit Tests
  $ nosetests --with-coverage --cover-erase --cover-package=lib.susepubliccloudinfoclient --cover-xml
```

