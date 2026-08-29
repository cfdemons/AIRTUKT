# AIRTUKT: A Tutorial Collection for Machine Learning in Turbulence

AIRTUKT is a collection of tutorials demonstrating the application of machine learning (ML) and related techniques to turbulence and computational fluid dynamics (CFD), as part of [`AIRTUK`](https://www.ukturbulence.co.uk/ai-hub.html). The collection covers four key areas of ML applications in turbulence research: ML-assisted reduced-order and surrogate modelling, including graph neural network-based approaches; ML-based optimisation and uncertainty quantification, including Bayesian optimisation and multi-fidelity shape optimisation; generative modelling for turbulence; and data assimilation using physics-informed neural networks (PINNs) for sparse-data reconstruction.

Each of the five tutorials has a dedicated Jupyter Notebook (`*.ipynb`) located in `AIRTUKT/tutorial/$tut_name/*.ipynb`. These notebooks allow users to explore the underlying theory of the algorithms, run the code, and post-process the results.



## Requirements

AIRTUKT requires a Linux operating system (tested mainly on [`Ubuntu`](https://ubuntu.com/desktop)) and **Python 3.10**.

You do **not** need to install Python 3.10 manually. The AIRTUKTT installation script uses [`uv`](https://docs.astral.sh/uv/) to automatically install and manage the required Python 3.10 interpreter.

The installation script will also install `uv` automatically if it is not already available on your system.

MFM_BO tutorial requires [`OpenFOAM2312`](https://www.openfoam.com/news/main-news/openfoam-v2312) or above, which can be installed used the following:

```bash
sudo curl -s https://openfoam.com | sudo bash
sudo apt-get update
sudo apt-get install openfoam2312-default -y
```

---

## Installation

### 1. Download the package and navigate to the AIRTUKT directory

Open a terminal and download the AIRTUKT packages using `git clone`, then navigate to the directory containing the AIRTUKT package:

```bash
git clone https://github.com/daniaahmed1/AIRTUKT.git
cd AIRTUKT
```

### 2. Make the scripts executable

Run:

```bash
chmod u+x *.sh
```

> **Note:** `chmod u+x` gives the scripts execute permission.

### 3. Install AIRTUKT

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
6. Install the AIRTUKT package into `.buildenv`.
7. Run `AIRTUKT install`.
8. Create the AIRTUKT and AIRTUKT2 environments.
9. Install the required Python packages for each environment.
10. Register the AIRTUKT and AIRTUKT2 Jupyter kernels.

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
     ├── Install AIRTUKT into .buildenv
     │
     └── Run "AIRTUKT install"
              │
              ├── Create ~/.AIRTUKT/envs/AIRTUKT
              │       └── Install AIRTUKT_requirements.txt
              │
              ├── Create ~/.AIRTUKT/envs/AIRTUKT2
              │       └── Install AIRTUKT2_requirements.txt
              │
              ├── Register "AIRTUKT" kernel
              │       └── Uses ~/.AIRTUKT/envs/AIRTUKT/bin/python
              │
              └── Register "AIRTUKT2" kernel
                      └── Uses ~/.AIRTUKT/envs/AIRTUKT2/bin/python
```

### Python 3.10

Python 3.10 is managed by `uv` and does not need to be installed system-wide.

The Python interpreter used by AIRTUKT is located inside the `.buildenv` environment:

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

## 4. Launching the Tutorials

After the installation has completed, launch the AIRTUKT tutorials using:

```bash
./run_AIRTUKT.sh
```

The launch script uses the AIRTUKT Python environment directly and does not require you to manually activate the virtual environment.

It will launch Jupyter and provide access to the AIRTUKT tutorials.

The basic workflow is therefore:

```text
./install.sh
      │
      └── Install AIRTUKT
              │
              ▼
       ./run_AIRTUKT.sh
              │
              ▼
       Launch Jupyter
```

---

## 5. Uninstall AIRTUKT

To uninstall AIRTUKT, run:

```bash
./uninstall.sh
```

The uninstall script will remove:

* The AIRTUKT Python package.
* AIRTUKT build metadata.
* The AIRTUKT environments.
* The `.buildenv` virtual environment.

The `uv` installation and its managed Python versions are **not removed**, because they may be used by other projects on the system.

If you want to remove `uv` or its managed Python versions separately, consult the `uv` documentation.

---

## AIRTUKT Environments

AIRTUKT uses two separate Python environments because different tutorials require different sets of dependencies.

```text
                         AIRTUKT
                        Installer
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
      AIRTUKT environment        AIRTUKT2 environment
              │                         │
        Kernel: AIRTUKT             Kernel: AIRTUKT2
              │                         │
              │                         │
       All tutorials             MFM_BO tutorial
        except MFM_BO
```

### AIRTUKT environment

The `AIRTUKT` environment is used by all tutorials except the multi-fidelity Bayesian optimisation tutorial.

The corresponding Jupyter kernel is:

```text
AIRTUKT
kernel: AIRTUKT
```

### AIRTUKT2 environment

The `AIRTUKT2` environment is specifically used by the `MFM_BO` tutorial.

The corresponding Jupyter kernel is:

```text
AIRTUKT2
kernel: AIRTUKT2
```

---

## Package Structure

The AIRTUKT package has the following structure:

```text
AIRTUKT/
│
├── pyproject.toml
├── README.md
├── LICENSE
├── install.sh
├── uninstall.sh
├── run_AIRTUKT.sh
│
├── requirements/
│   ├── AIRTUKT_requirements.txt
│   └── AIRTUKT2_requirements.txt
│
├── src/
│   └── AIRTUKT/
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
cd /path/to/AIRTUKT

chmod u+x *.sh

./install.sh
```

The installer will automatically install `uv`, obtain Python 3.10, create the AIRTUKT environment, install the required packages, and register the Jupyter kernels.

Once the installation is complete, launch the tutorials with:

```bash
./run_AIRTUKT.sh
```

That's it! AIRTUKT will manage the required Python 3.10 environment and create the required AIRTUKT environments and Jupyter kernels automatically.


