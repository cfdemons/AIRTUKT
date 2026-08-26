import subprocess
import sys


def install_kernel(kernel_name, display_name, python_executable):
    """Install one Jupyter kernel."""

    subprocess.run(
        [
            python_executable,
            "-m",
            "ipykernel",
            "install",
            "--user",
            "--name",
            kernel_name,
            "--display-name",
            display_name,
        ],
        check=True,
    )


def install_kernels(airtukt_python, airtukt2_python):
    """Install both AIRTUKT Jupyter kernels."""

    install_kernel(
        kernel_name="airtukt",
        display_name="AIRTUKT",
        python_executable=airtuk_python,
    )

    install_kernel(
        kernel_name="airtukt2",
        display_name="AIRTUKT2",
        python_executable=airtuk2_python,
    )
