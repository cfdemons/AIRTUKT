# AIRTUK: A Tutorial Collection for Machine Learning in Turbulence

AIRTUK is a collection of tutorials demonstrating the application of machine learning and related techniques to turbulence and computational fluid dynamics (CFD).

## Requirements

AIRTUK requires **Python 3.10**.

Before starting, make sure that Python 3.10 is installed and available as:

```bash
python3.10
```

You can check this with:

```bash
python3.10 --version
```

---

## Installation

### 1. Navigate to the AIRTUK directory

Open a terminal and navigate to the directory containing the AIRTUK package:

```bash
cd /path/to/AIRTUK
```

### 2. Make the scripts executable

Run:

```bash
chmod +x *.sh
```

> **Note:** `chmod +x` option gives the scripts execute permission.


### 3. Install AIRTUK

Run:

```bash
./install.sh
```

The installation script will automatically:

1. Check that Python 3.10 is available.
2. Create a Python virtual environment called `.buildenv`.
3. Activate the virtual environment.
4. Upgrade `pip`.
5. Install the AIRTUK package.
6. Create the AIRTUK and AIRTUK2 environments.
7. Install the required Python packages for each environment.
8. Register the AIRTUK and AIRTUK2 Jupyter kernels.

The installation process is structured as follows:

```text
./install.sh
     │
     ├── Check for Python 3.10
     │
     ├── Create .buildenv
     │
     ├── Activate .buildenv
     │
     ├── Install AIRTUK
     │
     └── Run "airtuk install"
              │
              ├── Create ~/.airtuk/envs/airtuk
              │       └── Install airtuk_requirements.txt
              │
              ├── Create ~/.airtuk/envs/airtuk2
              │       └── Install airtuk2_requirements.txt
              │
              ├── Register "AIRTUK" kernel
              │       └── Uses ~/.airtuk/envs/airtuk/bin/python
              │
              └── Register "AIRTUK2" kernel
                      └── Uses ~/.airtuk/envs/airtuk2/bin/python
```

If Python 3.10 is not found, the installation will stop and display:

```text
ERROR: AIRTUK requires Python 3.10
```

---

## Launching the Tutorials

After the installation has completed, launch the AIRTUK tutorials using:

```bash
./run_airtuk.sh
```

This will launch Jupyter and provide access to the AIRTUK tutorials.

---

## Uninstall AIRTUK

to uninstall AIRTUK use:

```bash
./uninstall.sh
```

This will unisntall both the dependencies and the enviroment.

---

## AIRTUK Environments

AIRTUK uses two separate Python environments because different tutorials require different sets of dependencies.

```text
                    AIRTUK
                   Installer
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
     AIRTUK environment   AIRTUK2 environment
             │                 │
       Kernel: airtuk     Kernel: airtuk2
             │                 │
             │                 │
     All tutorials       MFM_BO tutorial
       except MFM_BO
```

### AIRTUK environment

The `airtuk` environment is used by all tutorials except the multi-fidelity Bayesian optimisation tutorial.

The corresponding Jupyter kernel is:

```text
AIRTUK
kernel: airtuk
```

### AIRTUK2 environment

The `airtuk2` environment is specifically used by the `MFM_BO` tutorial.

The corresponding Jupyter kernel is:

```text
AIRTUK2
kernel: airtuk2
```

---

## Package Structure

The AIRTUK package has the following structure:

```text
AIRTUK/
│
├── pyproject.toml
├── README.md
├── LICENSE
├── install.sh
├── uninstall.sh
├── run_airtuk.sh
│
├── requirements/
│   ├── airtuk_requirements.txt
│   └── airtuk2_requirements.txt
│
├── src/
│   └── airtuk/
│       ├── __init__.py
│       ├── cli.py
│       ├── environments.py
│       ├── kernel.py
│       └── launcher.py
│
└── tutorials/
    │
    ├── BO_Tutorial/
    │   ├── *.ipynb
    │   └── ...
    │
    ├── GNN_Tutorial/
    │   ├── *.ipynb
    │   └── ...
    │
    ├── MFM_BO/
    │   ├── *.ipynb
    │   └── ...
    │
    ├── PINN_Tutorial/
    │   ├── *.ipynb
    │   └── ...
    │
    └── DDPM_Tutorial/
        ├── *.ipynb
        └── ...
```

---

## Quick Start

For a quick installation, simply run:

```bash
cd /path/to/AIRTUK

chmod +x *.sh

./install.sh
```

Once the installation is complete, launch the tutorials with:

```bash
./run_airtuk.sh
```

That's it! AIRTUK will create the required environments and Jupyter kernels automatically.

