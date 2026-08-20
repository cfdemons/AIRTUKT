import argparse

from .environments import setup_environments
from .kernel import install_kernels
from .launcher import launch_notebooks


def main():
    parser = argparse.ArgumentParser(
        description="AIRTUK: ML tutorials for turbulence research"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Install command
    install_parser = subparsers.add_parser(
        "install",
        help="Install the AIRTUK environments and Jupyter kernels",
    )

    # Notebook command
    notebook_parser = subparsers.add_parser(
        "notebook",
        help="Launch the AIRTUK tutorials in JupyterLab",
    )

    args = parser.parse_args()

    if args.command == "install":

        print("\n===================================")
        print("       Installing AIRTUK")
        print("===================================\n")

        # Create environments and install requirements
        python_executables = setup_environments()

        airtuk_python = python_executables["airtuk"]
        airtuk2_python = python_executables["airtuk2"]

        # Install both Jupyter kernels
        install_kernels(
            airtuk_python,
            airtuk2_python,
        )

        print("\n===================================")
        print("       AIRTUK installation complete")
        print("===================================\n")

    elif args.command == "notebook":

        launch_notebooks()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
