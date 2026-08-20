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


def install_kernels(airtuk_python, airtuk2_python):
    """Install both AIRTUK Jupyter kernels."""

    install_kernel(
        kernel_name="airtuk",
        display_name="AIRTUK",
        python_executable=airtuk_python,
    )

    install_kernel(
        kernel_name="airtuk2",
        display_name="AIRTUK2",
        python_executable=airtuk2_python,
    )
