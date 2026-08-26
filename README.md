# AIRTUK: A Tutorial Collection for Machine Learning in Turbulence

AIRTUK is a collection of tutorials demonstrating the application of machine learning (ML) and related techniques to turbulence and computational fluid dynamics (CFD). The collection covers four key areas of ML applications in turbulence research: ML-assisted reduced-order and surrogate modelling, including graph neural network-based approaches; ML-based optimisation and uncertainty quantification, including Bayesian optimisation and multi-fidelity shape optimisation; generative modelling for turbulence; and data assimilation using physics-informed neural networks (PINNs) for sparse-data reconstruction.

Each of the five tutorials has a dedicated Jupyter Notebook (`*.ipynb`) located in `AIRTUK/tutorial/$tut_name/*.ipynb`. These notebooks allow users to explore the underlying theory of the algorithms, run the code, and post-process the results.



## Requirements

AIRTUK requires **Python 3.10**.

You do **not** need to install Python 3.10 manually. The AIRTUK installation script uses [`uv`](https://docs.astral.sh/uv/) to automatically install and manage the required Python 3.10 interpreter.

The installation script will also install `uv` automatically if it is not already available on your system.

MFM_BO tutorial requires [`OpenFOAM2312`](https://www.openfoam.com/news/main-news/openfoam-v2312) or above, which can be installed used the following:

```bash
sudo curl -s https://openfoam.com | sudo bash

sudo apt-get update

sudo apt-get install openfoam2312-default -y
```

---

## Installation

### 1. Download the package and navigate to the AIRTUK directory

Open a terminal and download the AIRTUK packages using `git clone`, then navigate to the directory containing the AIRTUK package:

```bash
git clone https://github.com/daniaahmed1/AIRTUK.git
cd AIRTUK
```

### 2. Make the scripts executable

Run:

```bash
chmod +x *.sh
```

> **Note:** `chmod +x` gives the scripts execute permission.

### 3. Install AIRTUK

Run:

```bash
./install.sh
```

The installation script will automatically:

1. Check whether `uv` is installed.
2. Install `uv` if it is not available.
3. Install Python 3.10 using `uv`.
4. Create a Python 3.10 virtual environment called `.buildenv`.
5. Install and upgrade the required Python packaging tools.
6. Install the AIRTUK package into `.buildenv`.
7. Run `airtuk install`.
8. Create the AIRTUK and AIRTUK2 environments.
9. Install the required Python packages for each environment.
10. Register the AIRTUK and AIRTUK2 Jupyter kernels.

The installation process is structured as follows:

```text
./install.sh
     │
     ├── Check for uv
     │       │
     │       └── Install uv if necessary
     │
     ├── Install Python 3.10 using uv
     │
     ├── Create .buildenv using Python 3.10
     │
     ├── Install AIRTUK into .buildenv
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

### Python 3.10

Python 3.10 is managed by `uv` and does not need to be installed system-wide.

The Python interpreter used by AIRTUK is located inside the `.buildenv` environment:

```text
.buildenv/bin/python
```

You can verify the Python version after installation with:

```bash
.buildenv/bin/python --version
```

You should see:

```text
Python 3.10.x
```

You can also check the installed `uv` version with:

```bash
uv --version
```

---

## Launching the Tutorials

After the installation has completed, launch the AIRTUK tutorials using:

```bash
./run_airtuk.sh
```

The launch script uses the AIRTUK Python environment directly and does not require you to manually activate the virtual environment.

It will launch Jupyter and provide access to the AIRTUK tutorials.

The basic workflow is therefore:

```text
./install.sh
      │
      └── Install AIRTUK
              │
              ▼
       ./run_airtuk.sh
              │
              ▼
       Launch Jupyter
```

---

## Uninstall AIRTUK

To uninstall AIRTUK, run:

```bash
./uninstall.sh
```

The uninstall script will remove:

* The AIRTUK Python package.
* AIRTUK build metadata.
* The AIRTUK environments.
* The `.buildenv` virtual environment.

The `uv` installation and its managed Python versions are **not removed**, because they may be used by other projects on the system.

If you want to remove `uv` or its managed Python versions separately, consult the `uv` documentation.

---

## AIRTUK Environments

AIRTUK uses two separate Python environments because different tutorials require different sets of dependencies.

```text
                         AIRTUK
                        Installer
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
      AIRTUK environment        AIRTUK2 environment
              │                         │
        Kernel: airtuk             Kernel: airtuk2
              │                         │
              │                         │
       All tutorials             MFM_BO tutorial
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
    ├── MFM_BO_Tutorial/
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

The installer will automatically install `uv`, obtain Python 3.10, create the AIRTUK environment, install the required packages, and register the Jupyter kernels.

Once the installation is complete, launch the tutorials with:

```bash
./run_airtuk.sh
```

That's it! AIRTUK will manage the required Python 3.10 environment and create the required AIRTUK environments and Jupyter kernels automatically.


