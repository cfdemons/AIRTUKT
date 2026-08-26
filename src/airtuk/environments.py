from pathlib import Path
import subprocess
import sys


# AIRTUKT installation directory
AIRTUKT_HOME = Path.home() / ".AIRTUKT"


# Virtual environments
ENVIRONMENTS = {
    "AIRTUKT": AIRTUKT_HOME / "envs" / "AIRTUKT",
    "AIRTUKT2": AIRTUKT_HOME / "envs" / "AIRTUKT2",
}


# Requirements files
PACKAGE_ROOT = Path(__file__).resolve().parents[2]

REQUIREMENTS = {
    "AIRTUKT": PACKAGE_ROOT / "requirements" / "AIRTUKT_requirements.txt",
    "AIRTUKT2": PACKAGE_ROOT / "requirements" / "AIRTUKT2_requirements.txt",
}


def create_environment(name):
    """Create a virtual environment."""

    if name not in ENVIRONMENTS:
        raise ValueError(f"Unknown environment: {name}")

    env_path = ENVIRONMENTS[name]

    if env_path.exists():
        print(f"{name} environment already exists.")
    else:
        print(f"Creating {name} environment...")

        subprocess.run(
            [
                sys.executable,
                "-m",
                "venv",
                str(env_path),
            ],
            check=True,
        )

        print(f"Created: {env_path}")

    return env_path


def get_python_executable(name):
    """Return the Python executable for an AIRTUKT environment."""

    env_path = ENVIRONMENTS[name]

    if sys.platform == "win32":
        return env_path / "Scripts" / "python.exe"

    return env_path / "bin" / "python"


def install_requirements(name):
    """Install the requirements for an AIRTUKT environment."""

    if name not in REQUIREMENTS:
        raise ValueError(f"Unknown environment: {name}")

    env_path = create_environment(name)
    python_executable = get_python_executable(name)
    requirements_file = REQUIREMENTS[name]

    if not requirements_file.exists():
        raise FileNotFoundError(
            f"Requirements file not found: {requirements_file}"
        )

    print(f"\nInstalling requirements for {name}...")
    print(f"Requirements: {requirements_file}")

    subprocess.run(
        [
            str(python_executable),
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
        ],
        check=True,
    )
    
    print(f"\nInstalling ipykernel in {name}...")

    subprocess.run(
        [
            str(python_executable),
            "-m",
            "pip",
            "install",
            "ipykernel",
        ],
        check=True,
    )

    subprocess.run(
        [
            str(python_executable),
            "-m",
            "pip",
            "install",
            "-r",
            str(requirements_file),
        ],
        check=True,
    )

    # Install PyTorch Geometric CUDA extensions
    if name == "AIRTUKT":
        print("\nInstalling PyTorch Geometric CUDA extensions...")

        subprocess.run(
	    [
		str(python_executable),
		"-m",
		"pip",
		"install",
		"torch==2.5.1",
		"torchvision==0.20.1",
		"torchaudio==2.5.1",
		"--index-url",
		"https://download.pytorch.org/whl/cu121",
	    ],
	    check=True,
	)

    print(f"{name} requirements installed successfully.")

    return python_executable


def setup_environments():
    """Create and configure both AIRTUKT environments."""

    print("\n=== Setting up AIRTUKT environments ===\n")

    AIRTUKT_python = install_requirements("AIRTUKT")
    AIRTUKT2_python = install_requirements("AIRTUKT2")

    print("\n=== Environment setup complete ===\n")

    return {
        "AIRTUKT": AIRTUKT_python,
        "AIRTUKT2": AIRTUKT2_python,
    }
